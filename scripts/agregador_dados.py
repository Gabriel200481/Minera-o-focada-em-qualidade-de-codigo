import os
import pandas as pd
from typing import List, Dict, Any

def salvar_resultados_csv(resultados: List[Dict[str, Any]], caminho_arquivo: str) -> pd.DataFrame | None:
    """Recebe uma lista de dicionários com os resultados, consolida em um
    DataFrame do Pandas, e salva como um arquivo CSV."""
    if not resultados:
        print("\nNenhum resultado para salvar. O arquivo CSV não será gerado.")
        return None
        
    print(f"\nConsolidando {len(resultados)} resultado(s). Gerando arquivo CSV em {caminho_arquivo}...")
    
    final_df = pd.DataFrame(resultados)
    
    # Define a ordem exata das colunas para o arquivo final com métricas do CK
    column_order = [
        'repository', 'stars', 'age_years', 'releases',
        'cbo_mean', 'cbo_median', 'cbo_std',
        'dit_mean', 'dit_median', 'dit_std',
        'lcom_mean', 'lcom_median', 'lcom_std'
    ]
    
    final_df = final_df.reindex(columns=column_order)
    
    try:
        output_dir = os.path.dirname(caminho_arquivo)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_df.to_csv(caminho_arquivo, index=False)
        print(f"✅ Arquivo salvo com sucesso em: {caminho_arquivo}")
        return final_df
    except Exception as e:
        print(f"ERRO ao salvar o arquivo CSV: {e}")
        return None
