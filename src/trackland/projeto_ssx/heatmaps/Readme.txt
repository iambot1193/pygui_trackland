# heatmaps_kepler

Script em Python que processa um arquivo `.txt` com linhas no formato `CIDADE valor` e gera um `.csv` contendo **latitude/longitude (geocoding)** via **Nominatim (OpenStreetMap)**.  
O CSV gerado é **pronto para importação no Kepler.gl**, usando o campo `valor` como **peso/intensidade** para facilitar a visualização de **manutenções de placas com problemas**.

## O que ele faz
- Lê **um** arquivo `*.txt` na pasta `data/` *(mantenha apenas 1 arquivo por execução)*  
- Interpreta cada linha no formato `CIDADE valor` (ex.: `Campo Grande 12`)
- Realiza geocodificação (cidade → `lat/lon`)
- Gera e salva:
  - `output/<nome_do_txt>.csv` — arquivo final para uso no Kepler.gl
  - `output/geocache.json` — cache local para evitar requisições repetidas e acelerar execuções futuras

## Requisitos
- Python 3.x  
- Dependências via `requirements.txt` do repositório *(ou instalação manual de `geopy`)*