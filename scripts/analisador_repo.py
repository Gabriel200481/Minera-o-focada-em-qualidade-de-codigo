import os
import requests
import zipfile
import shutil
import pandas as pd
import subprocess
import numpy as np

# --- [CONFIGURAÇÃO OBRIGATÓRIA] ---
# Aponte este caminho para o executável java.exe dentro da pasta bin do JDK 11 que você instalou.
# Use o formato r"..." (raw string) para evitar problemas com barras invertidas no Windows.
JAVA11_EXECUTABLE_PATH = r"C:\\Program Files\\Eclipse Adoptium\\jdk-11.0.22.7-hotspot\\bin\\java.exe"

# --- FUNÇÕES AUXILIARES ("PRIVADAS") ---

def _find_java_source_directories(root_path: str) -> list[str]:
    """Varre e retorna uma lista de todos os diretórios com código-fonte Java."""
    print("  Buscando diretórios com código-fonte .java...")
    source_dirs = []
    for dirpath, _, filenames in os.walk(root_path):
        path_parts = dirpath.lower().replace("\\", "/").split('/')
        if 'test' in path_parts or any(p.startswith('.') for p in path_parts):
            continue
        if any(fname.endswith('.java') for fname in filenames):
            source_dirs.append(dirpath)
    if source_dirs:
        print(f"  Encontrado(s) {len(source_dirs)} diretório(s) com código-fonte Java.")
    return source_dirs

def _download_and_unzip_repo(repo_info: dict, download_dir: str) -> str | None:
    """Baixa o repositório como um arquivo ZIP e o extrai."""
    repo_full_name = repo_info['repository']
    default_branch = repo_info['default_branch']
    zip_url = f"https://github.com/{repo_full_name}/archive/refs/heads/{default_branch}.zip"
    zip_path = os.path.join(download_dir, f"{repo_full_name.split('/')[1]}.zip")
    try:
        response = requests.get(zip_url, timeout=180)
        response.raise_for_status()
        with open(zip_path, 'wb') as f: f.write(response.content)
        print(f"  Extraindo arquivo ZIP...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(download_dir)
        extracted_folder_name = f"{repo_full_name.split('/')[1]}-{default_branch}"
        return os.path.join(download_dir, extracted_folder_name)
    except Exception as e:
        print(f"  ERRO no download/extração: {e}")
        return None
    finally:
        if os.path.exists(zip_path): os.remove(zip_path)

def _run_ck_analysis_on_module(ck_jar_path: str, module_path: str, ck_output_path: str) -> bool:
    """Executa o CK para um módulo específico, usando a versão correta do Java."""
    print(f"    -> Analisando módulo: {os.path.basename(module_path)}")
    os.makedirs(ck_output_path, exist_ok=True)
    
    if not os.path.exists(JAVA11_EXECUTABLE_PATH):
        print(f"  ERRO CRÍTICO: O executável do Java 11 não foi encontrado em '{JAVA11_EXECUTABLE_PATH}'.")
        print("  Por favor, instale o JDK 11 e configure o caminho na variável JAVA11_EXECUTABLE_PATH.")
        return False

    command = [
        JAVA11_EXECUTABLE_PATH,
        "-jar",
        os.path.abspath(ck_jar_path),
        os.path.abspath(module_path),
        "true", "0", "false",
        os.path.abspath(module_path)
    ]

    try:
        result = subprocess.run(
            command,
            cwd=os.path.abspath(ck_output_path),
            capture_output=True, text=True, check=False, encoding='utf-8'
        )
        if result.returncode != 0:
            print(f"    -> ERRO ao executar o CK (código de saída {result.returncode}).")
            if result.stderr: print(f"      {result.stderr.strip()}")
            return False
        if not os.path.exists(os.path.join(ck_output_path, "class.csv")):
             print(f"    -> AVISO: CK executou, mas 'class.csv' não foi gerado.")
             return False
        print(f"    -> SUCESSO: Métricas extraídas em {ck_output_path}")
        return True
    except Exception as e:
        print(f"  ERRO inesperado no subprocesso: {e}")
        return False

def _process_ck_results(ck_results_dir: str) -> dict | None:
    """Consolida os resultados de múltiplos arquivos class.csv de um repositório."""
    all_class_metrics = []
    for root, _, files in os.walk(ck_results_dir):
        if "class.csv" in files:
            try:
                df_module = pd.read_csv(os.path.join(root, "class.csv"))
                all_class_metrics.append(df_module)
            except Exception as e:
                print(f"  AVISO: Falha ao ler o arquivo class.csv em {root}. Erro: {e}")

    if not all_class_metrics:
        print("  AVISO: Nenhum arquivo class.csv foi gerado ou lido com sucesso.")
        return None
        
    print(f"  Processando resultados de {len(all_class_metrics)} módulo(s)...")
    df_repo = pd.concat(all_class_metrics, ignore_index=True)
    
    quality_metrics = ['cbo', 'dit', 'lcom']
    summary_stats = {}
    for metric in quality_metrics:
        if metric in df_repo.columns and pd.to_numeric(df_repo[metric], errors='coerce').notna().any():
            numeric_series = pd.to_numeric(df_repo[metric], errors='coerce').dropna()
            summary_stats[f'{metric}_mean'] = numeric_series.mean()
            summary_stats[f'{metric}_median'] = numeric_series.median()
            summary_stats[f'{metric}_std'] = numeric_series.std()
            
    return summary_stats

def _cleanup(path: str):
    """Remove um diretório e seu conteúdo."""
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

# --- FUNÇÃO PRINCIPAL DO MÓDULO ---

def analisar_repositorio(repo_info: dict, base_repos_dir: str, base_ck_results_dir: str, ck_jar_path: str) -> dict | None:
    """Orquestra a análise de um único repositório."""
    repo_name_only = repo_info['repository'].split('/')[1]
    repo_ck_output_path = os.path.join(base_ck_results_dir, repo_name_only)
    
    extracted_repo_root_path = None
    try:
        extracted_repo_root_path = _download_and_unzip_repo(repo_info, base_repos_dir)
        if not extracted_repo_root_path: return None

        java_source_dirs = _find_java_source_directories(extracted_repo_root_path)
        if not java_source_dirs:
            print("  AVISO: Nenhum diretório com código-fonte .java foi encontrado.")
            return None
        
        print(f"  Analisando {len(java_source_dirs)} módulo(s) Java...")
        _cleanup(repo_ck_output_path)
        os.makedirs(repo_ck_output_path, exist_ok=True)
        
        for i, module_path in enumerate(java_source_dirs):
            module_output_path = os.path.join(repo_ck_output_path, f"module_{i}")
            _run_ck_analysis_on_module(ck_jar_path, module_path, module_output_path)
        
        return _process_ck_results(repo_ck_output_path)
        
    finally:
        if extracted_repo_root_path:
            _cleanup(extracted_repo_root_path)
