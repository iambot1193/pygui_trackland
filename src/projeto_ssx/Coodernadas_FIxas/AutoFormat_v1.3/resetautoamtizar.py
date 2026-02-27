import pyautogui as pa
import time
import keyboard
from playsound import playsound
import sonsperso
import pyperclip
import lembrete_Auto
import threading


# ================= CONFIGURAÇÕES ============================
pa.FAILSAFE = False
pa.PAUSE = 0.1

keyboard.block_key("f1")
keyboard.block_key("esc")
keyboard.block_key("f2")
keyboard.block_key("f3")
keyboard.block_key("f4")
keyboard.block_key("f6")
keyboard.block_key("f7")
keyboard.block_key("f8")
# ============================================================

################# FUNÇÕES BASE ###############################

def close_program():
    if keyboard.is_pressed("esc"):
        exit()

def find_color():
    x, y = pa.position()
    img = pa.screenshot(region=(x, y, 1, 1))
    return img.getpixel((0, 0))

def check_loading():
    pa.moveTo(263, 117)
    pa.moveTo(261, 150)
    cor = find_color()
    while cor != (51, 52, 62):
        close_program()
        time.sleep(0.1)
        cor = find_color()

def mouse_info():
    time.sleep(0.01) 
    mouse_x, mouse_y = pa.position()
    pixel_image = pa.screenshot(region=(mouse_x, mouse_y, 1, 1))
    pixel_color = pixel_image.getpixel((0, 0))
    print(f"  pa.moveTo({mouse_x}, {mouse_y})")
    print(f"  cor: {pixel_color}\n\n")

def move(x, y):
    pa.moveTo(x, y)
    
def click():
    pa.click()

while True:
    time.sleep(0.1)
    close_program()
    ui_aberto = 0

    if keyboard.is_pressed("f1"):
        mouse_info()
        time.sleep(0.3)

    # ============================ F2 ============================
    if keyboard.is_pressed("f2"):

        # ===== PLACAS VINDO DO CTRL+C =====
        texto = pyperclip.paste()

        PLACAS = [
            linha.strip()
            for linha in texto.splitlines()
            if linha.strip()
        ][:1000]


        if not PLACAS:
            print("Nenhuma placa válida no clipboard.")
            time.sleep(0.5)
            continue

        total = len(PLACAS)

        n1=1
        n2=1
        
        for placa in PLACAS:
                
            if n1: 
                # ===========================
                # N1 — PESQUISA (POR PLACA)
                # ===========================

                inicial = 118

            
                close_program()

                move(inicial, 19)
                click()

                pyperclip.copy(placa)

                pa.moveTo(1728, 150) 
                pa.click()
                time.sleep(0.3)

                pa.moveTo(1365, 197)
                cor = find_color()
                tentativas = 0
                
                while cor != (255, 182, 99):
                    close_program()
                    time.sleep(0.1)
                    tentativas += 1
                    cor = find_color()

                    if tentativas >= 20:
                        pa.moveTo(1728, 150) 
                        pa.click()
                        move(1365, 184)
                        tentativas = 0

                move(1644, 212)
                click()
                pa.hotkey("ctrl", "a")
                pa.hotkey("ctrl", "v")
                pa.hotkey("enter")
                
                
                move(1436, 349)
                cor = find_color()
                tentativas = 0

                while cor != (245, 245, 245):
                    close_program()
                    time.sleep(0.1)
                    cor = find_color()
                    tentativas += 1

                    if tentativas >= 15:
                        move(1644, 212)
                        click()
                        pa.hotkey("ctrl", "a")
                        pa.hotkey("ctrl", "v")
                        pa.hotkey("enter")
                        move(1436, 349)
                        tentativas = 0

                move(1437, 544)
                if find_color() != (255, 255, 255):
                    while not keyboard.is_pressed("f1"):
                        close_program()
                        time.sleep(0.3)
                else:
                    move(1419, 359)
                    click()

            if n2: 
                # ===========================
                # N2 — EXECUTA PELO TOTAL
                # ===========================

                inicial = 118

                
                
                move(inicial, 19)
                click()

                close_program()
                check_loading()
                pa.moveTo(58,745)
                pa.click()
                pa.moveTo(247, 570)
                pa.click()
                pa.moveTo(397, 252)
                current_color = find_color()
                while current_color!= (255,182,99):
                    current_color = find_color()
                    time.sleep(0.1)
                    close_program()
                pa.moveTo(853, 305)
                pa.click()
                keyboard.write("reset")
                pa.moveTo(906, 332)
                current_color = find_color()
                while(current_color!= (96,96,96)):
                    close_program()
                    current_color = find_color()
                    time.sleep(0.1)
                pa.click()
                pa.moveTo(1340, 852)
                current_color = find_color()
                while(current_color!=(46,47,51)):
                    close_program()
                    current_color = find_color()
                    time.sleep(0.1)
                pa.click()
                pa.moveTo(1531, 201)
                current_color = find_color()
                while(current_color!=(239,239,239)):
                    close_program()
                    current_color = find_color()
                    time.sleep(0.1)
                pa.click()
                check_loading()
                

                
                