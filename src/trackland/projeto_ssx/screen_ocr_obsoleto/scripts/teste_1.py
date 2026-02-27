import pyautogui as pa
from screeninfo import get_monitors

pa.FAILSAFE = True

MONITOR = 1 #monitor secndario 
get_info = get_monitors() #getmontiro
m_info = get_info[MONITOR] #guardando ifnormaoes em variavel especifica
regiao = (m_info.x, m_info.y, m_info.width, m_info.height) #gardando infoma~ços especificar em regiao
print(regiao)

TEMPLATE = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\settings.png"
alvo = pa.locateCenterOnScreen(TEMPLATE, confidence= 0.7, grayscale=True)
    
if alvo:
    pa.moveTo(alvo)
else:
    print("nao encontrado")
