# obter_coordenada

Script em Python para **processar planilhas `.xlsx`**, ler a coluna `lst_localizacao` (latitude/longitude) e gerar um arquivo com **endereço (reverse geocoding)** usando **Nominatim (OpenStreetMap)**.  
Inclui **cache em CSV** para evitar requisições repetidas.

## O que ele faz
- Lê todos os arquivos `*.xlsx` da pasta de entrada
- Extrai coordenadas da coluna `lst_localizacao`
- Normaliza formatos (ex.: `-18.5,-53.1`, `[-18.5,-53.1]`)
- Faz reverse geocoding (lat/lon → endereço)
- Salva:
  - `output/enderecos_convertidos.csv` (saída final)
  - `cache/cache_enderecos.csv` (cache persistente)

## Requisitos
- Python 3.11+
- Dependências instaladas a partir do `requirements.txt` do repositório

## Instalação (Windows / PowerShell)
Na raiz do repositório:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt