import pyautogui as pa
import time
import keyboard
import threading
pa.FAILSAFE = False
import random

tempo = 0

rodando = True

def close_program():
    global rodando
    while True:
        if keyboard.is_pressed('esc'):
            exit()
                
def pos_info():
    while rodando: 
        
        time.sleep(0.1) 
        mouse_x, mouse_y = pa.position()
        pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
        pixel_color = pixel_image.getpixel((0, 0))
        print(f"Posição: ({mouse_x}, {mouse_y})  |||  Cor: {pixel_color}")
        
def counter(tempo):
    while rodando:
            
        time.sleep(1)
        tempo +=1
        print(f"Tempo ${tempo}")
        
def move_until100():
    while rodando:
        
        time.sleep(0.5)
        pa.moveTo(random.randint(300,400), random.randint(300,400), 0.3)
        


while True:
    t1 = threading.Thread(target=move_until100, daemon=True)
    t2 = threading.Thread(target=pos_info, daemon=True)
    t3 = threading.Thread(target=counter, args=(tempo,), daemon=True)
    t4 = threading.Thread(target=close_program, daemon=True)
    
    
    time.sleep(0.1)
        
    if keyboard.is_pressed('f2'):
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        

        
        
