import os
from github import Github, Auth
from dotenv import load_dotenv
from scripts.coletor_github import coletar_dados_processo
from scripts.analisador_repo import analisar_repositorio
from scripts.agregador_dados import salvar_resultados_csv

# --- CONFIGURAÇÃO ---
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    GITHUB_TOKEN = input("Digite seu GITHUB_TOKEN: ")

# Caminho para a ferramenta CK. Garanta que o arquivo ck.jar esteja na raiz do projeto.
CK_JAR_PATH = "ck.jar"

# Diretórios do projeto
OUTPUT_DIR = "output"
REPOS_DIR = "repos_extraidos"
CK_RESULTS_DIR = "resultados_ck" # Diretório para resultados do CK
FINAL_CSV_PATH = os.path.join(OUTPUT_DIR, "repositorios_metricas_ck.csv")

# Quantidade de repositórios a analisar
LIMIT = 1 # Altere para a quantidade desejada

def setup_environment():
    """Cria os diretórios necessários para a execução do script."""
    print("Configurando o ambiente...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(REPOS_DIR, exist_ok=True)
    os.makedirs(CK_RESULTS_DIR, exist_ok=True)

def main():
    """Função principal que orquestra todo o processo."""
    if not GITHUB_TOKEN:
        print("ERRO: Token do GitHub não encontrado. Verifique seu arquivo .env.")
        return
        
    setup_environment()
    
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    repos_data = coletar_dados_processo(g, limit=LIMIT)
    
    if not repos_data:
        print("Coleta de dados do GitHub não retornou repositórios. Encerrando.")
        return

    all_repo_results = []
    
    for repo_info in repos_data:
        print(f"\n--- Processando: {repo_info['repository']} ---")
        
        quality_metrics = analisar_repositorio(repo_info, REPOS_DIR, CK_RESULTS_DIR, CK_JAR_PATH)
        
        final_data = {**repo_info}
        if 'default_branch' in final_data:
            del final_data['default_branch']

        if quality_metrics:
            final_data.update(quality_metrics)
            print(f"--- Análise de {repo_info['repository']} concluída com SUCESSO! ---")
        else:
            metric_keys = ['cbo_mean', 'cbo_median', 'cbo_std', 'dit_mean', 'dit_median', 'dit_std', 'lcom_mean', 'lcom_median', 'lcom_std']
            for key in metric_keys:
                final_data[key] = None
            print(f"--- Falha na análise de {repo_info['repository']}. Registrando com métricas nulas. ---")

        all_repo_results.append(final_data)

    final_df = salvar_resultados_csv(all_repo_results, FINAL_CSV_PATH)
    if final_df is not None:
        print("\n--- Resultado Final ---")
        print(final_df)

if __name__ == "__main__":
    main()
