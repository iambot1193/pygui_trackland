import pyautogui as pa
import time
import keyboard
import pyperclip
pa.FAILSAFE = False

keyboard.block_key('f2')

def close_program():
        if keyboard.is_pressed('esc'):
            exit()

def find_color():
            mouse_x, mouse_y = pa.position()
            pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
            pixel_color = pixel_image.getpixel((0, 0))
            return pixel_color

def check_loading():
        pa.moveTo(203, 101)
        pa.moveTo(206, 99)
        currentColor = find_color()
        while(currentColor!=(51, 52, 62)):
            time.sleep(0.1)
            currentColor = find_color() 
     

while(1):
    time.sleep(0.1)
    
    if keyboard.is_pressed('f2'):
        print("f2")
        
        