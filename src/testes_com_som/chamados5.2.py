import pyautogui as pa
import time
import keyboard
pa.FAILSAFE = False
pa.PAUSE = 0.01

def findcolor():    
    mouse_x, mouse_y = pa.position()
    pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
    pixel_color = pixel_image.getpixel((0, 0))
    return pixel_color

def close_progam():
    if keyboard.is_pressed('esc'):
        exit()
        
        
        
        #################
fone = 1073, 117
monitor = 837, 225
x_close_calls = 880
y_close_calls = 225
#####################################
    

while(1):
    if keyboard.is_pressed('f2'):
        close_progam()
        print("f2")
        
        pa.moveTo(fone) # chamados, laranja
        call = findcolor()
        print(call)
        while call == (217, 123, 76):
            print("teste")
            close_progam()
            
            time.sleep(0.1)
            pa.leftClick()
            pa.moveTo(monitor) #verificando se chamados foi aberto
            time_try = 0
            checkload = findcolor()
            while checkload != (51, 51, 51):
                close_progam()
                
                time.sleep(0.1)
                checkload = findcolor()
                time_try +=1
                if time_try >= 20:
                    pa.moveTo(fone) # re abrindo chamados
                    pa.leftClick()
                    pa.moveTo(monitor)
                    time_try = 0
                checkload = findcolor()
                
            
            while checkload == (51, 51, 51):
                close_progam()
                
                pa.moveTo(x_close_calls, y_close_calls) #chamado 1
                pa.leftClick()
                pa.moveTo(monitor)
                checkload = findcolor()
                y_close_calls += 45
                if y_close_calls > 635:
                    break
                
                
            time.sleep(1)
            pa.moveTo(fone)
            y_close_calls = 225
            
        
        