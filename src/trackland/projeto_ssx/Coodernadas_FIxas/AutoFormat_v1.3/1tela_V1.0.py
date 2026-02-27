import pyautogui as pa
import time
import keyboard
from playsound import playsound
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

################# SITUAÇÕES ##################################

def colar(texto):
    pyperclip.copy(texto)
    pa.hotkey("ctrl", "v")

def situ_substituir(numero):
    match numero:
        case 1: #S COMUNICAÇÃO
            colar("Sem comunicação.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Contatar cliente.")
            pa.hotkey("tab")
            colar("SEM COMUNICAÇÃO.")
            return
        case 2: #RESET
            colar("Veículo apresenta pequenos saltos e travamentos durante a rota.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Enviar reset.")
            pa.hotkey("tab")
            colar("PEQUENOS SALTOS E TRAVAMENTOS.")
            return
        case 3: #BUZZER VIOLADO
            colar("Veículo apresenta possível violação de buzzer, faz maior parte da rota sem identificação de motorista.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 4: #SALTOS
            colar("Veículo apresenta saltos e travamentos durante a rota.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("SALTOS E TRAVAMENTOS.")
            return
        case 5: #IGNIÇÃO VIOLADA
            colar("Veículo apresenta sensor de ignição violado durante a rota.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 6: #MAL CONTATO BACKUP
            colar("Bateria backup apresenta mal contato durante a rota.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 7: #BACKUP NUNCA TEM CARGA
            colar("Bateria backup nunca tem carga, mesmo com ignição ligada.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 8: #S DADOS O SUFICIENTE
            colar("Veículo não apresentou dados o suficiente. Aguardar próxima análise.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Em observação.")
            pa.hotkey("tab")
            colar("")
            return
        case 9: #POSIÇÃO IG OFF
            colar("Veículo apresentou posição com a ignição desligada.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 10: #BATERIA VIOLADA PORTAL
            colar("Veículo apresentou violação de bateria indicado pelo portal SSX.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 11: #SALTOS IG OFF
            colar("Veículo apresentou saltos e travamentos com a ignição desligada durante a rota.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 12: #GPS TRAVADO
            colar("Veículo apresenta gps travado durante a rota.")
            for i in range (0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("GPS TRAVADO.")
            return
        case _:
            return
    



                               #################funções##########################

################# LOOP PRINCIPAL #############################

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
        ][:10]


        if not PLACAS:
            print("Nenhuma placa válida no clipboard.")
            time.sleep(0.5)
            continue

        total = len(PLACAS)

        n1=1
        n2=1
        n3=1
        

        if n1: 
            # ===========================
            # N1 — PESQUISA (POR PLACA)
            # ===========================

            inicial = 118

            for placa in PLACAS:
                close_program()

                move(inicial, 19)
                click()

                pyperclip.copy(placa)

                pa.moveTo(1728, 150) 
                pa.click()
                time.sleep(0.3)
    
                pa.moveTo(1365, 184)
                cor = find_color()
                tentativas = 0
                
                while cor != (255, 182, 99):
                    close_program()
                    time.sleep(0.1)
                    tentativas += 1
                    cor = find_color()

                    if tentativas >= 7:
                        pa.moveTo(1728, 150) 
                        pa.click()
                        move(1365, 184)

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

                    if tentativas >= 7:
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

                inicial += 165

        if n2: 
            # ===========================
            # N2 — EXECUTA PELO TOTAL
            # ===========================

            inicial = 118
            for _ in range(total):

                
                
                move(inicial, 19)
                click()

                close_program()
                check_loading()
                move(58, 744)
                click()
                move(245, 411)
                click()
                inicial += 165
        if n3: 
            # ===========================
            # N3 — EXECUTA PELO TOTAL
            # ===========================
            inicial = 118

            for _ in range(total):
                close_program()

                move(inicial, 19)
                click()

                close_program()
                check_loading()

                move(720, 608)
                click()
                close_program()

                move(711, 654)
                current_color = find_color()
                contador = 0
                tentativas_totais = 0
                tentativas_max = 100  # <<< LIMITE REAL

                while current_color != (51, 52, 62):
                    close_program()
                    current_color = find_color()
                    contador += 1
                    tentativas_totais += 1
                    time.sleep(0.1)

                    if tentativas_totais >= tentativas_max:
                        print("N3 ignorado: timeout de carregamento")
                        break

                    if contador >= 10:
                        move(720, 608)
                        click()
                        move(711, 654)
                        contador = 0


                close_program()
                pa.moveTo(298, 653)
                pa.click(clicks=10)

                time.sleep(0.5)

                pa.moveTo(355, 747)
                pa.mouseDown()
                pa.moveTo(5, 747)
                pa.mouseUp()

                move(711, 654)
                pa.click()  

                click()

                time.sleep(0.3)

                inicial += 165
            
            move(82, 19)
            click()

           # sonsperso.tocar_som()

    # ============================ F7 ============================
    if keyboard.is_pressed("f7"):
        pa.moveTo(661, 360)
        pa.click()
        while True:
            close_program()
            pa.hotkey("ctrl", "c")
            try:
                situ = int(pyperclip.paste())
                print(repr(int(pyperclip.paste())))
            except:
                break
                
            situ_substituir(situ)

            for _ in range(5):
                pa.hotkey("left")
            pa.hotkey("down")
    # ============================ F4 ============================
    if keyboard.is_pressed("f4"):      
        if ui_aberto == 0:
            threading.Thread(target= lembrete_Auto.executar, daemon=True).start()
            time.sleep(0.3)
            ui_aberto = 1    
        elif lembrete_Auto.get_state() == "withdrawn":
            lembrete_Auto._abrir()
        else: 
            WindowsError("janela já aberta")
        
        
        
        
        
        