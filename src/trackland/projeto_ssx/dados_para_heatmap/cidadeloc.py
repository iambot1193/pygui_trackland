import csv
import pyperclip
from geopy.geocoders import Nominatim
import time

# Inicializa o geolocalizador
geolocator = Nominatim(user_agent="geo_municipios_msw")

# Lê dados da área de transferência
entrada_clip = pyperclip.paste()
linhas = [linha.strip() for linha in entrada_clip.splitlines() if linha.strip()]

# Cria CSV
with open("saida.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["lat", "lon", "valor"])
    
    for linha in linhas:
        partes = linha.rsplit(" ", 1)
        if len(partes) == 2:
            cidade, valor_str = partes
            cidade_full = f"{cidade}, Mato Grosso do Sul, Brasil"
            try:
                valor = int(valor_str)
            except ValueError:
                print(f"Valor inválido em '{linha}'")
                continue

            # Consulta coordenadas
            try:
                location = geolocator.geocode(cidade_full)
                if location:
                    writer.writerow([location.latitude, location.longitude, valor])
                else:
                    print(f"Não encontrado: {cidade}")
            except Exception as e:
                print(f"Erro consultando {cidade}: {e}")

            # Pausa pequena para não sobrecarregar o serviço
            time.sleep(1)
        else:
            print(f"Entrada inválida: {linha}")

print("CSV gerado com coordenadas reais: saida.csv")
