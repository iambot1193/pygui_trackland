import pyautogui as pa
import time
import keyboard
from playsound import playsound
import sonsperso
import pyperclip

#configs
pa.FAILSAFE = False
pa.PAUSE = 0.1
keyboard.block_key("f1")
keyboard.block_key("esc")
keyboard.block_key("f2")
keyboard.block_key("f3")
#configs



                               #################funções##########################
def close_program():
        if keyboard.is_pressed('esc'):
            exit()
            
def find_color():
            mouse_x, mouse_y = pa.position()
            pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
            pixel_color = pixel_image.getpixel((0, 0))
            return pixel_color

def check_loading():
        pa.moveTo(201, 94)################## MUDAR
        pa.moveTo(209, 113) ######### MUDAR
        currentColor = find_color()
        while(currentColor!=(51, 52, 62)): 
            close_program()

            time.sleep(0.1)
            currentColor = find_color() 
            
def mouse_info():
    time.sleep(0.01) 
    mouse_x, mouse_y = pa.position()
    pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
    pixel_color = pixel_image.getpixel((0, 0))
    print(f"        Posição: ({mouse_x}, {mouse_y}) \n Cor: {pixel_color}")
    
def click():
    pa.leftClick()
    
def move(x ,y):
    pa.moveTo(x ,y)
    
                               #################funções##########################
                               
while(True):
    time.sleep(0.1)
    close_program()
    
    if keyboard.is_pressed("f1"):
        mouse_info()
        time.sleep(0.3)
        
    if keyboard.is_pressed("f2"):
        
        sonsperso.tocar_som() #somrandom
        
        n1 = 1
        n2 = 1
        n3 = 1
        
        

        ##### variaveis padrão #########################
        number_vehicles = 10
        sheets_y = 270
        ssx_x = 95
        ##### variaveis padrão #############################
        
        if (n1):
            
            for numero in range (0, number_vehicles):
                close_program()

                move(ssx_x , 15)
                click()
                move(-1350, sheets_y) 
                click()
                pa.hotkey("ctrl", "c")
                check_loading()
                move(1212, 115)
                click()   
                move(1135, 172)
                click()
                pa.hotkey("ctrl", "v")
                move(1324, 171)
                click()
                
                ########################## esperar carregmento
                move(965, 285)
                current_color = find_color()
                contador = 0
                while current_color != (255, 182, 99):

                    close_program()
                    
                    time.sleep(0.1)
                    current_color = find_color()
                    contador += 1
                    if contador >= 10:
                        move(1142, 174)
                        click()
                        pa.hotkey("ctrl", "a")
                        pa.hotkey("ctrl", "v")
                        move(1323, 172)
                        click()
                        move(965, 285)
                        current_color = find_color()
                        contador = 0
                        
                        
                ########verificar se tem mais de um rastreador
                
                move(980, 437)
                current_color = find_color()
                if current_color != (255, 255, 255):
                    btn = 0
                    while btn == 0:

                        close_program()
                        
                        playsound(r"C:\Users\jenni\Downloads\programs\SCIUTPS\Simples\sons\not.mp3")
                        time.sleep(0.3)
                        if keyboard.is_pressed("f1"):
                            btn = 1    
                            
                            
                else:
                    move(966, 285) 
                    click()   
                #################    verificar se tem mais de um rastreador
                
                
                ### adicionando para ir para o proximo 
                sheets_y += 30
                ssx_x += 105
                numero +=1
            
        if (n2):     
                    
            ssx_x = 95
            
            for numero in range (0, number_vehicles):
                close_program()

                move(ssx_x, 20)
                click()
                check_loading()
                move(45, 548) 
                click()
                move(202, 232)
                click()
                
                ssx_x += 105
                numero +=1
        
        if (n3):    
                
            ssx_x = 95
            
            for numero in range (0, number_vehicles):
                close_program()

                move(ssx_x, 20)
                click()
                check_loading()
                move(575, 440)
                click()
                move(570, 473) 
                time.sleep(0.3)
                current_color = find_color
                contador = 0
                btn = 0
                while current_color != (51, 52, 62) and btn == 0:
                    current_color = find_color()
                    close_program()
                    
                    if keyboard.is_pressed("f1"):
                        btn = 1
                    time.sleep(0.1)
                    current_color = find_color()
                    contador +=1
                    if contador >= 10:
                        contador = 0
                        move(575, 440)
                        click()
                        move(570, 473)
                move(237, 475) 
                if btn != 1:
                    pa.PAUSE = 0.05
                    for i in range (0 , 10):
                        close_program()

                        click()
                    pa.PAUSE = 0.1
                    time.sleep(0.2)
                    move(282, 550) 
                    pa.mouseDown()
                    move(2, 5530.3) 
                    pa.mouseUp()
                    move(570, 473) 
                    time.sleep(0.3)
                    click()
                
                ssx_x += 105
                numero +=1
            
            sonsperso.tocar_som()
            
            #playsound(r"C:\Users\jenni\Downloads\programs\SCIUTPS\Simples\sons\tafarco.mp3")
                
    if keyboard.is_pressed("f3"):
    
        pa.moveTo(269, 97)
        pa.click()
        pa.hotkey("left")
        pyperclip.copy("RELATÓRIO ")
        pa.hotkey("ctrl", "v")
        pa.hotkey("ctrl", "a")        
        pa.hotkey("right")
        for i in range (0, 5):
            pa.hotkey("left")
        pa.write(" 17-10-2025")
                    
                