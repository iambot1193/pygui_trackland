import pyautogui as pa
from screeninfo import get_monitors
import keyboard
import time
#pa.useImageNotFoundException(False) usavel em casos que eu nao queira retonar imagemNotFoundExceptione e queira 
#retornar none no lugar     
pa.FAILSAFE = False
MONITOR = [1, 2]
keyboard.block_key("f1")
keyboard.block_key("f2")
keyboard.block_key("esc")


def close_program():
    if keyboard.is_pressed("esc"):
        exit(1) 
    
def check_loading(reference_point):
    try:
        check = pa.locateCenterOnScreen(reference_point, confidence=0.7, grayscale=True)
    except pa.ImageNotFoundException:
        check = None
        
    while check is None:
        try:
            time.sleep(0.2)
            close_program()
            check = pa.locateCenterOnScreen(reference_point, confidence=0.7, grayscale=True)
        except pa.ImageNotFoundException:
            check = None
            
    return check

def page_ready(reference_point):
    try:
        check = pa.locateCenterOnScreen(reference_point, confidence=0.7, grayscale=True, )
    except pa.ImageNotFoundException:
        check = None
        
    while check is None:
        try:
            time.sleep(0.2)
            close_program()
            check = pa.locateCenterOnScreen(reference_point, confidence=0.7, grayscale=True)
        except pa.ImageNotFoundException:
            check = None
            
    return check

def click_image(reference):
    pa.click(pa.locateCenterOnScreen(reference, confidence=0.7, grayscale=True))

def mouse_info():
    time.sleep(0.01) 
    mouse_x, mouse_y = pa.position()
    pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
    pixel_color = pixel_image.getpixel((0, 0))
    print(f"        Posição: ({mouse_x}, {mouse_y}) \n Cor: {pixel_color}")

        

while(1):
    time.sleep(0.1)
    
    if keyboard.is_pressed("f1"):
        mouse_info()
        time.sleep(0.3)
    
    
    if keyboard.is_pressed("f2"):
        close_program()
        page_ready = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\settings.png"
        page_ready2 = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\settings.png"
        ssx = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\ssx.png"
        ssx_pos = pa.locateCenterOnScreen(ssx, confidence= 0.8, grayscale=True)
        x, y = ssx_pos
        ssx_pos = x +50, y
                    
        n1 = 1
        n2 = 0
        n3 = 0
        veiculos = 9
        
        
        #parte de pesquisar placas tera que ser feita na mao pois o programa apenas reconhece o monitor 
        #principal para pesquisar imagens ou cores
        
        if n1:
            search = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\search.png" 
            search2 = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\search2.png" 
            veiculos = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\veiculos.png"
            
            
            pa.click(ssx_pos)
            check_loading(page_ready)
            contador_veiculos = 0
            sheets_inicial = 269
            
            pa.click(-1369, 268)
            pa.hotkey("ctrl", "c")
            check_loading(search)
            click_image(search)
            time.sleep(0.3)
            check_loading(search2)
            search2pos = pa.locateAllOnScreen(search2, confidence=0.7, grayscale=True)
            pa.moveTo(search2pos)
            pa.move(-100, 0)
            pa.click()
            pa.hotkey("ctrl", "v")
            pa.hotkey("enter")
            check_loading(veiculos)
            rastreador = 0
            
            for _ in pa.locateAllOnScreen(veiculos, confidence=0.9, grayscale=True):
                rastreador+= 1
                
                
                #caso de apenas um rastrador
            if rastreador == 1:
                veiculospos = pa.locateAllOnScreen(veiculos, confidence=0.9, grayscale=True)
                pa.click(veiculospos)
            else:  #caso tenha mais de 1 rastreador esperar usuario abrir manualmente a rota 
                btn = 0
                while btn == 0:
                    close_program()
                    time.sleep(0.3)
                    if keyboard.is_pressed("f1"):
                        btn = 1  
                
            
            sheets_inicial += 105
            ssx_pos = (ssx_pos[0] + 110, y)
            contador_veiculos += 1
        
        if n2:   
            open_hist1png = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\openhistory1.png"
            open_hist2png = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\openhistory2.png"    
            
            pa.click(ssx_pos)
            contador_veiculos = 0
            
            while contador_veiculos <= veiculos:
                close_program()
                
                pa.click(ssx_pos)
                check_loading(page_ready)
                
                
                check_loading(open_hist1png)
                hist1 = pa.locateCenterOnScreen(open_hist1png, confidence=0.7, grayscale=True)
                time.sleep(0.3)
                pa.click(hist1.x+12, hist1.y)
                check_loading(open_hist2png)
                click_image(open_hist2png)
                
                ssx_pos = (ssx_pos[0] + 110, y)
                contador_veiculos += 1
        
        if n3:
            filter = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\filter.png"
            minus = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\minus.png"
            pull = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\pull.png"
            ok = r"C:\Users\jenni\Downloads\programs\Scripts\pygui_trackland\src\Track\Projeto_SSX\Nocord\assets\ok.png"
            
            pa.click(ssx_pos)
            contador_veiculos = 0
            
            while contador_veiculos <= veiculos:
                

                
                check_loading(page_ready)
                
                check_loading(filter)
                click_image(filter)
                time.sleep(0.5)
                check_loading(minus)
                minuspos = pa.locateCenterOnScreen(minus, confidence=0.9, grayscale=True)
                pa.click(minuspos) #expandindo data
                pa.click(clicks=9, interval=0.1)#valor -1 por conta do click image
                pullpos = pa.locateCenterOnScreen(pull, confidence=1, grayscale=True)
                pa.moveTo(pullpos)
                pa.mouseDown()
                pa.move(-9999, 0, 0.3)
                pa.mouseUp()
                okpos = pa.locateCenterOnScreen(ok, confidence=0.9, grayscale=True)
                pa.click(okpos)
                time.sleep(0.1)
                
                ssx_pos = (ssx_pos[0] + 110, y)
                pa.click(ssx_pos)
                contador_veiculos += 1
                
                
                
                
                
                
                
                
                
                