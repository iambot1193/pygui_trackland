import random 
import pygame as pyg
from pathlib import Path

def tocar_som():
    
    #iniciadores e configuração
    pyg.mixer.init()
    VOLUME_PADRAO = 0.3
    PASTA_SONS = r"C:\Users\jenni\Downloads\programs\SCIUTPS\Simples\sons"
    EXTENSAO = ".mp3"
    #iniciadores e configuração

    sons = [
    ("bonk_BEtiM8g.mp3", 90),
    ("chance baixa.mp3", 1),
    ("clash-royale-prince-charge.mp3", 90),
    ("cursed-spongebob-ambatakam.mp3", 5),
    ("evolution-mega-knight.mp3", 90),
    ("fbi-open-up-sfx.mp3", 90),
    ("gta-san-andreas-ah-shit-here-we-go-again_BWv0Gvc.mp3", 90),
    ("he-he-he-ha-clash-royale-deep-fried.mp3", 90),
    ("michael-dont-leave-me-here.mp3", 242),
    ("mini-peka.mp3", 90),
    ("star-platinum-za-warudo.mp3", 90),
    ("super-mario-coin-sound.mp3", 90),
    ("wet-fart_1.mp3", 90)
    ]
    

    arquivos, pesos = zip(*sons)
    escolhido = random.choices(arquivos, weights=pesos, k=1)[0]
    if escolhido == "chance baixa.mp3":
        VOLUME_PADRAO = 1
    print(f"Tocando: {escolhido}")
            
            
    caminho = Path(PASTA_SONS) / escolhido
    som = pyg.mixer.Sound(str(caminho))
    som.set_volume(VOLUME_PADRAO)
    som.play()

    # Espera terminar
    while pyg.mixer.get_busy():
        pass

    pyg.mixer.quit()
                
if __name__ == "__main__":
        tocar_som()
