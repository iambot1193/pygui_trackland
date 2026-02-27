import time
import pyautogui as pag
from screeninfo import get_monitors

pag.FAILSAFE = True

#para cada monitor, enumerar (pegar monitores)
for i, monitor in enumerate(get_monitors()):
    #criar uma tupla que recebe as informações sobre o monitor
    regiao = (monitor.x, monitor.y, monitor.width, monitor.height)
    #mostrar as caracteristicas do monitor em específico 
    print(f"{i}: {regiao}")
