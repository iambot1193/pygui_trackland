import pandas as pd
import os
import glob 
import keyboard
import math

# Função Haversine para distância em km
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    raio_terra = 6371  # km
    return c * raio_terra


pd.set_option('display.max_rows', None)
keyboard.block_key('f2')
pastafonte = r"C:\Users\jenni\Downloads\TESTES_PLANILHAS"

while True:
    
    if keyboard.is_pressed('f2'):
        print("f2")

        arquivos_xlsx = glob.glob(os.path.join(pastafonte, "*xlsx"))

        for arquivo in arquivos_xlsx:
            
            nome_arquivo = os.path.basename(arquivo)          # pega só o nome com extensão
            nome_sem_ext = os.path.splitext(nome_arquivo)[0]  # remove a extensão
            

            try:
                df = pd.read_excel(arquivo, usecols=["Data do evento", "Latitude", "Longitude"])
                
                contador_saltos = 0  # contador de saltos >1 km

                # percorre linhas consecutivas
                for i in range(1, len(df)):
                    lat1, lon1 = df.loc[i-1, "Latitude"], df.loc[i-1, "Longitude"]
                    lat2, lon2 = df.loc[i, "Latitude"], df.loc[i, "Longitude"]
                    
                    distancia = haversine(lat1, lon1, lat2, lon2)
                    
                    if distancia > 2:  # se salto > 1 km
                        contador_saltos += 1

                print(f"[{nome_sem_ext}] Quantidade de saltos >1 km: {contador_saltos}")

            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")