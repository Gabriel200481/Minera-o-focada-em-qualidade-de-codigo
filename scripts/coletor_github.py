# scripts/coletor_github.py

from typing import List, Dict, Any

def coletar_dados_processo(github_client, limit=1000) -> List[Dict[str, Any]]:
    resultados = []
    query = 'language:Java sort:stars'
    repos = github_client.search_repositories(query=query)
    count = 0
    for repo in repos:
        if count >= limit:
            break
        try:
            releases = repo.get_releases().totalCount
        except Exception:
            releases = 0
        try:
            created = repo.created_at
            age_years = (github_client.get_user().created_at - created).days / 365.25
        except Exception:
            age_years = 0.0
        resultados.append({
            'repository': repo.full_name,
            'stars': repo.stargazers_count,
            'age_years': age_years,
            'releases': releases,
            'default_branch': repo.default_branch
        })
        count += 1
    return resultados
