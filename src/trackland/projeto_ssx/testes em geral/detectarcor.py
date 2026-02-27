import pyautogui
import time



while 1:
    time.sleep(1) 
    
    
    mouse_x, mouse_y = pyautogui.position()

    
    pixel_image = pyautogui.screenshot(region=(mouse_x, mouse_y, 1, 1))


    pixel_color = pixel_image.getpixel((0, 0))

    print(f"Color at ({mouse_x}, {mouse_y}): {pixel_color}")
    

