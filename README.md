# Análise de Qualidade em Repositórios Java Populares (LAB02)

<p align="center">
  <img src="https://img.shields.io/badge/Linguagem-Java-orange" alt="Linguagem Java">
  <img src="https://img.shields.io/badge/Ferramenta-CK-blue" alt="Ferramenta de Análise CK">
  <img src="https://img.shields.io/badge/API-GitHub%20API-lightgrey" alt="API GitHub">
</p>

## 📖 Descrição do Projeto

Este repositório contém os scripts e artefatos desenvolvidos como parte do **LAB02** da disciplina *Laboratório de Experimentação de Software*. 

O objetivo principal do estudo é analisar a relação entre características do processo de desenvolvimento (popularidade, maturidade, atividade e tamanho) e métricas de qualidade de código em projetos open-source. [cite: 11, 12] [cite_start]Para isso, foram coletados e analisados dados dos **1.000 repositórios Java mais populares do GitHub**, utilizando a ferramenta de análise estática **CK** para obter as métricas de qualidade. 

Este conjunto de arquivos permite tanto a **reprodução do estudo** quanto a **análise detalhada das métricas** obtidas.

---

## 🗂️ Estrutura do Repositório e Ficheiros

-   **scripts/**: Pasta contendo os scripts de automação.
    -   `github_collector.py`: Script para coletar dados dos 1.000 repositórios via API do GitHub.
    -   `ck_runner.sh`: Script para automatizar a clonagem dos repositórios e a execução da ferramenta CK em cada um.
    -   `data_merger.py`: Script para unificar os resultados da API do GitHub e da ferramenta CK.
-   **data/**: Pasta com os dados brutos e processados.
    -   `github_metrics.csv`: Ficheiro CSV com os dados brutos coletados do GitHub.
    -   `ck_metrics_raw/`: Diretório contendo os resultados brutos da ferramenta CK para cada repositório.
    -   `final_dataset.csv`: Ficheiro CSV final com os dados combinados e prontos para análise.
-   **RelatorioFinal.pdf**: Relatório final com a introdução, metodologia, análise completa, discussão dos resultados e conclusões do estudo.
-   **graficos/**: Pasta contendo as imagens dos gráficos de correlação gerados para cada questão de pesquisa.

---

## ✨ Funcionalidades

-   Coleta automatizada de métricas de processo (estrelas, idade, releases, etc.) via API do GitHub. 
-   Automação da clonagem de repositórios e execução da ferramenta de análise estática CK para extrair métricas de qualidade. 
-   Processamento e unificação dos dados de diferentes fontes em um único dataset.
-   Geração de gráficos de correlação (utilizando a biblioteca `seaborn` em Python) para visualização dos resultados.
-   Análise estatística para validar as relações observadas.

---

## 🧾 Colunas do CSV Final (`final_dataset.csv`)

-   **repository_name**: Nome do repositório.
-   **stars**: Número de estrelas (Popularidade).
-   **age_years**: Idade do repositório em anos (Maturidade). 
-   **releases**: Número total de releases (Atividade). 
-   **loc**: Linhas de código (Tamanho). 
-   **cbo_mean**: Média do *Coupling Between Objects* para as classes do repositório. 
-   **dit_mean**: Média do *Depth of Inheritance Tree* para as classes do repositório. 
-   **lcom_mean**: Média do *Lack of Cohesion of Methods* para as classes do repositório. 

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

-   [Java Development Kit (JDK)](https://www.oracle.com/java/technologies/downloads/) (versão 8 ou superior).
-   [Python 3](https://www.python.org/downloads/) com as bibliotecas `pandas`, `requests` e `seaborn`.
-   A ferramenta [CK](https://github.com/mauricioaniche/ck) (o ficheiro `.jar` deve estar no diretório raiz do projeto).
-   Um **Personal Access Token (PAT)** do GitHub com o escopo `public_repo`.

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DA_PASTA]
    ```

2.  **Instale as dependências Python:**
    ```bash
    pip install pandas requests seaborn
    ```

3.  **Insira o seu Token de Acesso:**
    -   Abra o ficheiro `scripts/github_collector.py`.
    -   Localize a linha:
        ```python
        token = "SEU_TOKEN_AQUI"
        ```
    -   Substitua `"SEU_TOKEN_AQUI"` pelo seu token do GitHub.

4.  **Execute a Coleta e Análise:**
    -   Execute o pipeline completo. Os scripts irão coletar os dados, executar a análise estática e unificar os resultados.
    ```bash
    python scripts/github_collector.py
    bash scripts/ck_runner.sh
    python scripts/data_merger.py
    ```
    -   Ao final, o ficheiro `final_dataset.csv` e os gráficos serão gerados nos seus respectivos diretórios.

---

## 📈 Relatório Técnico (Resumo dos Resultados)

A análise dos 1.000 repositórios Java mais populares revelou as seguintes conclusões, confirmando ou refutando as hipóteses iniciais do estudo.

| Questão de Pesquisa (RQ) | Relação Analisada | Resultado Qualitativo | Conclusão do Relatório |
| :--- | :--- | :---: | :--- |
| **RQ 01: Popularidade** | `Popularidade (estrelas) ↑` vs. `Qualidade ↑` | **Correlação Positiva** | **Hipótese Confirmada**. [cite_start]Repositórios mais populares (Quartil 4) apresentam menor acoplamento (CBO), menor profundidade de herança (DIT) e maior coesão (menor LCOM) em comparação com os menos populares (Quartil 1), sugerindo que o escrutínio da comunidade leva a melhorias contínuas. [cite: 53, 54, 55] |
| **RQ 02: Maturidade** | `Maturidade (idade) ↑` vs. `Qualidade ↑` | **Correlação Positiva** | **Hipótese Confirmada Parcialmente**. [cite_start]Projetos mais maduros e veteranos demonstram melhor qualidade de código (CBO e LCOM menores) do que projetos jovens, indicando que o processo evolutivo tende a refinar a qualidade ao longo do tempo. [cite: 60] |
| **RQ 03: Atividade** | `Atividade (releases) ↑` vs. `Qualidade ↑` | **Correlação Positiva Moderada** | **Hipótese Confirmada Parcialmente**. Um número maior de releases está associado a uma melhoria moderada nas métricas de qualidade. [cite_start]Projetos com atividade "Muito Alta" são consistentemente melhores que os de "Baixa" atividade, apoiando a ideia de que processos de desenvolvimento ativos incluem controle de qualidade. [cite: 65, 66] |
| **RQ 04: Tamanho** | `Tamanho (LOC) ↑` vs. `Qualidade ↓` | **Correlação Negativa Forte** | **Hipótese Confirmada**. O tamanho do código é o fator com o maior impacto negativo na qualidade. [cite_start]Repositórios "Muito Grandes" (>200K LOC) apresentam acoplamento (CBO) quase 90% maior e falta de coesão (LCOM) 45% maior que os "Pequenos" (<10K LOC), evidenciando os desafios de manutenção em larga escala. [cite: 71, 72, 75] |

> **Nota**: Os dados completos e a metodologia detalhada da análise podem ser encontrados no ficheiro `RelatorioFinal.pdf`. [cite: 1]

---

## ⚖️ Licença

Este projeto está sob a licença **MIT**.

---

## 👥 Autores

* Rafael de Paiva Gomes
* Raphaella Cristina Sacramento
* Gabriel Afonso Infante Vieira

---

<p align="center"><em>Projeto desenvolvido para a disciplina de Medição e Experimentação de Software [cite: 3]</em></p>

<p align="center"><em>Projeto desenvolvido para a disciplina de Laboratório de Experimentação de Software</em></p>
