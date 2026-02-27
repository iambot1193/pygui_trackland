import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
import os

# ✅ CAMINHO REAL DO SEU ARQUIVO EXCEL
arquivo_excel = r"C:\Users\jenni\Downloads\pegarendereco\OWU54911.xlsx"
# ✅ CAMINHO DO ARQUIVO DE SAÍDA
arquivo_saida = r"C:\Users\jenni\Downloads\pegarendereco\enderecos_convertidos.csv"

# ⚠️ Verifique se o arquivo existe
if not os.path.exists(arquivo_excel):
    raise FileNotFoundError(f"❌ Arquivo não encontrado em:\n{arquivo_excel}")

# 📥 Lê o Excel
lst_localizacao = pd.read_excel(arquivo_excel)

# ⚠️ VERIFICAÇÃO DE COLUNAS
esperadas = {"latitude", "longitude"}
colunas = set(lst_localizacao.columns.str.lower())
if not esperadas.issubset(colunas):
    raise ValueError(f"❌ A planilha deve conter as colunas: {esperadas}. Colunas encontradas: {colunas}")

# ✅ Renomeia colunas se necessário
lst_localizacao.rename(columns=lambda x: x.lower(), inplace=True)

# Copia para trabalhar
df = lst_localizacao.copy()

# Configura geolocalizador
geolocator = Nominatim(user_agent="lovable_geocoder")

# Arredonda para 4 casas e cria chave
df["lat_round"] = df["latitude"].round(4)
df["lon_round"] = df["longitude"].round(4)
df["coord_chave"] = df["lat_round"].astype(str) + "," + df["lon_round"].astype(str)

# Obtém coordenadas únicas
coordenadas_unicas = df["coord_chave"].drop_duplicates().reset_index(drop=True)

# Faz geocodificação
enderecos = []
print(f"🔍 Buscando {len(coordenadas_unicas)} endereços únicos...\n")

for i, coord in enumerate(coordenadas_unicas):
    lat, lon = map(float, coord.split(','))
    try:
        location = geolocator.reverse((lat, lon), timeout=10)
        endereco = location.address if location else "Endereço não encontrado"
    except Exception as e:
        endereco = f"Erro: {e}"

    enderecos.append((coord, endereco))
    print(f"[{i+1}/{len(coordenadas_unicas)}] {coord} → {endereco[:60]}...")
    sleep(1.1)

# Junta resultados
df_enderecos = pd.DataFrame(enderecos, columns=["coord_chave", "endereco"])
df_final = df.merge(df_enderecos, on="coord_chave", how="left")

# Exporta para CSV
df_final[["latitude", "longitude", "endereco"]].to_csv(arquivo_saida, sep="|", index=False, encoding="utf-8")

print(f"\n✅ Endereços salvos com sucesso em:\n{arquivo_saida}")
