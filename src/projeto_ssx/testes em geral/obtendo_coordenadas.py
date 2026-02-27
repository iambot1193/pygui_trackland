import pandas as pd
import os
import glob 
import keyboard

pd.set_option('display.max_rows', None)
keyboard.block_key('f2')
pastafonte = r"C:\Users\jenni\Downloads\TESTES_PLANILHAS"

while True:
    
    if keyboard.is_pressed('f2'):
        print("f2")

        arquivos_xlsx = glob.glob(os.path.join(pastafonte, "*xlsx"))

        for arquivo in arquivos_xlsx:
            print("dentro_loop")
            try: 
                
                df = pd.read_excel(arquivo, usecols=["Data do evento" , "Latitude" , "Longitude"])
                print(df.head(len(df)))
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")
            
            
            