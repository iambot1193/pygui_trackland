# Excel Splitter & Reports (openpyxl)

Automação em Python para processar planilhas do Excel e gerar relatórios automaticamente, preservando formatação (cores, fonte, bordas) usando **openpyxl**.

## O que este projeto faz

### ✅ Script principal (`main.py`)
- Lê todos os arquivos `.xlsx`/`.xlsm` da pasta `data/`
- Agrupa as linhas pelo campo **CLIENTE**
- Gera **um arquivo por cliente** em `output/`
- Nomeia o arquivo com a **maior data encontrada** na coluna **DATA ULTIMA POSICAO**
  - Ex.: `SED AMAMBAI (27-02-2026).xlsx`
- Preserva estilos das células (cores, bordas, fontes)

### ✅ Variante (`variants/relatorio_nexxus.py`)
- Lê todos os arquivos `.xlsx`/`.xlsm` da pasta `data/`
- Filtra apenas linhas cujo **CLIENTE** contenha `"NEX"` (NEXXUS / NEXUS / NEX)
- Gera um relatório consolidado em:
  - `output/RELATORIO_NEXXUS.xlsx`
- Mantém formatação e aplica padronização visual no final

---

## Estrutura do projeto

```text
.
├─ main.py
├─ data/                # coloque aqui os arquivos de entrada
├─ output/              # arquivos gerados (saída)
└─ variants/
   └─ relatorio_nexxus.py