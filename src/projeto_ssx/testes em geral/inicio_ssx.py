import pyautogui as pa
import keyboard
import time 

keyboard.block_key("esc")
keyboard.block_key("f2")
keyboard.block_key("f1")

def close_program():
    if keyboard.is_pressed("esc"):
        exit(1)
        
def pos_mouse():
    return pa.position()

while (1):
    time.sleep(0.2)
    close_program()
    
    if keyboard.is_pressed("f2"):
        mouse_x, mouse_y = pos_mouse()
        pa.leftClick()
        print(f'pa.moveTo{mouse_x, mouse_y}')
        print("pa.leftClick()")