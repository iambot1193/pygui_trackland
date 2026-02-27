import pyautogui as pa
import time
import keyboard
import threading
pa.FAILSAFE = False
import random

cor_detectada = threading.Event()

def close_program():
    global rodando
    
    while True:
        if keyboard.is_pressed('esc'):
            exit()
            
                
def verificar():
    while rodando:
    
        mouse_x, mouse_y = pa.position()
        pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
        pixel_color = pixel_image.getpixel((0, 0))
        
        cor_detectada = pixel_image.getpixel((0, 0))
        while pixel_color != (255, 182, 99):
            cor_detectada.set()
            cor_detectada = pixel_image.getpixel((0, 0))
            
        
def mover():
    while rodando:
        
        pa.moveTo(967, 230)
        pa.moveTo(967, 300, 1)
        time.sleep(0.1)
        

rodando = True


while True:
    if keyboard.is_pressed('f2'):
        t1 = threading.Thread(target=mover, daemon=True)
        t2 = threading.Thread(target=verificar, daemon=True)
        t3 = threading.Thread(target=close_program)
        
        t1.start()
        t2.start()
        t3.start()
        
        time.sleep(2)
        
    if cor_detectada.is_set():
        print("detecado")
        rodando = False
        t1.join()
        t2.join()
        t3.join()
        time.sleep(10)
    time.sleep(1)

        