import requests
import json
import time
import os

url =  "https://raw.githubusercontent.com/iambot1193/keys/main/teste_com_keys/key.json"
key_local_ativa = "activation.json"
bloquear_em_segundos = 5
os.path.exists(key_local_ativa) and os.remove(key_local_ativa)

def bloqueio_status():
    if not os.path.exists(key_local_ativa):
        return False
    else: 
        return True
    
def bloqueio_status_informar():
    if not os.path.exists(key_local_ativa):
        print("App Bloquado")
        return True
    else: 
        print("App Desbloquado")
        return False    
    
def desbloqueio(keylocal):
    for keys in data["keys"]:
        if keys["key"] == keylocal:
            if keys["valid"] == True:
                with open(key_local_ativa, "w") as f:
                    f.write("Key ativada")
                print("Key Válida")
            else:
                print("Key inválida")
            break
    else: 
        print("Key inexistente")
        
def bloquear_tempo(bloquear_em_segundos):
    if bloqueio_status() == True:
        tempo_ativacao = time.time()
        tempo_final = tempo_ativacao+bloquear_em_segundos
        while tempo_ativacao < tempo_final:
            
            print(f"O tempo restando é {int(tempo_final - tempo_ativacao)}s")
            time.sleep(0.9)
            tempo_ativacao = time.time()
        os.remove(key_local_ativa)
    else:  
        print("Bloqueio Ativado")




keylocal = input("Digite a key: ")

reposta = requests.get(url)
data = reposta.json()

desbloqueio(keylocal)
bloqueio_status_informar()
bloquear_tempo(bloquear_em_segundos)