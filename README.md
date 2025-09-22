# Análise de Qualidade em Repositórios Java Populares (LAB02)

<p align="center">
  <img src="https://img.shields.io/badge/Linguagem-Java-orange" alt="Linguagem Java">
  <img src="https://img.shields.io/badge/Ferramenta-CK-blue" alt="Ferramenta de Análise CK">
  <img src="https://img.shields.io/badge/API-GitHub%20API-lightgrey" alt="API GitHub">
</p>

## 📖 Descrição do Projeto

Este repositório contém os scripts e artefatos desenvolvidos como parte do **LAB02** da disciplina *Laboratório de Experimentação de Software*.

O objetivo principal do estudo é analisar a relação entre características do processo de desenvolvimento e métricas de qualidade de código em projetos open-source. Para isso, foram coletados dados dos **1.000 repositórios Java mais populares do GitHub**. As métricas de processo (popularidade, maturidade, atividade e tamanho) foram extraídas via API do GitHub, enquanto as métricas de qualidade de código (**CBO, DIT e LCOM**) foram calculadas através da ferramenta de análise estática **CK**.

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
-   Análise estatística com o teste de correlação de **Spearman** para validar as relações observadas.

---

## 🧾 Colunas do CSV Final (`final_dataset.csv`)

-   **repository_name**: Nome do repositório.
-   **stars**: Número de estrelas (Popularidade).
-   **age_years**: Idade do repositório em anos (Maturidade).
-   **releases**: Número total de releases (Atividade).
-   **loc**: Linhas de código (Tamanho).
-   **loc_comments**: Linhas de comentários (Tamanho).
-   **cbo_median**: Mediana do *Coupling Between Objects* para as classes do repositório.
-   **dit_median**: Mediana do *Depth of Inheritance Tree* para as classes do repositório.
-   **lcom_median**: Mediana do *Lack of Cohesion of Methods* para as classes do repositório.

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
    -   Execute o pipeline completo através do script principal. Ele irá chamar os outros scripts na ordem correta.
    ```bash
    python scripts/github_collector.py
    bash scripts/ck_runner.sh
    python scripts/data_merger.py
    ```
    -   Ao final, o ficheiro `final_dataset.csv` e os gráficos serão gerados nos seus respectivos diretórios.

---

## 📈 Relatório Técnico (Resumo dos Resultados)

A análise dos dados, baseada no coeficiente de correlação de **Spearman**, revelou os seguintes insights sobre a relação entre as características dos repositórios e a sua qualidade de código.

| Questão de Pesquisa (RQ) | Relação Analisada | Coeficiente (ρ) | Hipótese e Resultado |
| :--- | :--- | :---: | :--- |
| **RQ 01: Popularidade** | `stars` vs. Qualidade (`CBO`/`LCOM` ↓) | **~ -0.25** | **Hipótese Confirmada (fraca)**: Repositórios mais populares tendem a ter uma qualidade de código *ligeiramente* melhor (menor acoplamento e maior coesão), possivelmente devido a maior revisão pela comunidade. |
| **RQ 02: Maturidade** | `age_years` vs. Qualidade (`CBO`/`LCOM` ↓) | **~ +0.15** | **Hipótese Refutada**: Projetos mais antigos, por si sós, tendem a acumular débitos técnicos, mostrando uma qualidade *ligeiramente* inferior. A manutenção ativa é um fator mais decisivo que a idade. |
| **RQ 03: Atividade** | `releases` vs. Qualidade (`CBO`/`LCOM` ↓) | **~ -0.30** | **Hipótese Confirmada (fraca)**: Uma maior frequência de releases correlaciona-se com melhor qualidade, sugerindo que processos de CI/CD maduros e entregas incrementais favorecem a manutenibilidade. |
| **RQ 04: Tamanho** | `loc` vs. Qualidade (`CBO`/`LCOM` ↑) | **~ +0.65** | **Hipótese Confirmada (forte)**: O tamanho do repositório é o preditor mais forte de baixa qualidade. Quanto maior a base de código (LOC), maior o acoplamento (CBO) e a falta de coesão (LCOM). |

> **Nota**: A análise de correlação não implica causalidade. Os resultados completos e os gráficos de dispersão estão detalhados no `RelatorioFinal.pdf`.

---

## ⚖️ Licença

Este projeto está sob a licença **MIT**. Veja o ficheiro `LICENSE.md` para mais detalhes.

---

## 👥 Autores

* Gabriel Afonso Infante Vieira

* Rafael de Paiva Gomes

* Rafaella Cristina de Sousa Sacramento

---

<p align="center"><em>Projeto desenvolvido para a disciplina de Laboratório de Experimentação de Software</em></p>
