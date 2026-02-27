import pyautogui as pa
import time
import keyboard
import pyperclip
import json
from pathlib import Path
import winsound
import tkinter as tk
import sys




"""
Registrador de Coordenadas SSX
Autor(a): Felipe Gonçalves Lopes
Criado em: 2026-01-16
Versão: 1.0.0
Direitos: (c) 2026 Felipe Gonçalves Lopes. Todos os direitos reservados.
"""

# ================= CONFIGURAÇÕES ============================
pa.PAUSE = 0.15

keyboard.block_key("f1")
keyboard.block_key("esc")
keyboard.block_key("f2")
keyboard.block_key("f3")
keyboard.block_key("f4")
keyboard.block_key("f6")
keyboard.block_key("f7")
keyboard.block_key("f8")
# ============================================================

# =================== LER COORDS DO JSON =====================


BASE = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
ARQ = BASE / "coords.json"



with ARQ.open("r", encoding="utf-8") as f:
    C = json.load(f)

def XY(nome: str):
    d = C[nome]
    return (d["x"], d["y"])

# coords (nomes iguais ao seu json)
imagem_menu1 = XY("imagem_menu1.png")
imagem_menu2 = XY("imagem_menu2.png")

inicialx = C["inicialx.png"]["x"]
inicialy = C["inicialy.png"]["y"]

somar_proximaguia = C["somar_proximaguia"]

icone_lupa = XY("icone_lupa.png")
esquerda_laranja_abrir_busca = XY("esquerda_laranja_abrir_busca.png")
campo_2_busca_placa = XY("campo_2_busca_placa.png")
meio_detectar_placa = XY("meio_detectar_placa.png")
meio_detectar_duas_placas = XY("meio_detectar_duas_placas.png")
abrir_chamado_placa = XY("abrir_chamado_placa.png")

seta_historico_unidade_rastrada = XY("seta_historico_unidade_rastrada.png")
abrir_historico_unidade = XY("abrir_historico_unidade.png")
abrir_historico = XY("abrir_historico.png")

botao_ok_parte_preta = XY("botao_ok_parte_preta.png")
botao_menos = XY("botao_menos.png")
data_parte_esquerda = XY("data_parte_esquerda.png")
maximo_esquerda_na_tela = XY("maximo_esquerda_na_tela.png")
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
    # antes estava "imagem_menu1.png" como se fosse variável; agora é tupla (x,y)
    pa.moveTo(*imagem_menu1)
    pa.moveTo(*imagem_menu2)
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

################# SITUAÇÕES ##################################

def colar(texto):
    pyperclip.copy(texto)
    pa.hotkey("ctrl", "v")
    

def situ_substituir(numero):
    match numero:
        case 1:
            colar("Sem comunicação.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Contatar cliente.")
            pa.hotkey("tab")
            colar("SEM COMUNICAÇÃO.")
            return
        case 2:
            colar("Veículo apresenta pequenos saltos e travamentos durante a rota.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Enviar reset.")
            pa.hotkey("tab")
            colar("PEQUENOS SALTOS E TRAVAMENTOS.")
            return
        case 3:
            colar("Veículo apresenta possível violação de buzzer, faz maior parte da rota sem identificação de motorista.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 4:
            colar("Veículo apresenta saltos e travamentos durante a rota.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("SALTOS E TRAVAMENTOS.")
            return
        case 5:
            colar("Veículo apresenta sensor de ignição violado durante a rota.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 6:
            colar("Bateria backup apresenta mal contato durante a rota.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 7:
            colar("Bateria backup nunca tem carga, mesmo com ignição ligada.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 8:
            colar("Veículo não apresentou dados o suficiente. Aguardar próxima análise.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Em observação.")
            pa.hotkey("tab")
            colar("")
            return
        case 9:
            colar("Veículo apresentou posição com a ignição desligada.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 10:
            colar("Veículo apresentou violação de bateria indicado pelo portal SSX.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 11:
            colar("Veículo apresentou saltos e travamentos com a ignição desligada durante a rota.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("POSSÍVEL VIOLAÇÃO.")
            return
        case 12:
            colar("Veículo apresenta gps travado durante a rota.")
            for _ in range(0, 4):
                pa.hotkey("tab")
            colar("Agendar manutenção.")
            pa.hotkey("tab")
            colar("GPS TRAVADO.")
            return
        case _:
            return

################# LOOP PRINCIPAL #############################
t0 = time.time()

while True:

    
    time.sleep(0.1)
    close_program()
    

    if time.time() - t0 >= 60*60:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)  # alerta do Windows
        
        w = tk.Tk()
        w.overrideredirect(True)
        w.update_idletasks()
        w.geometry(f"+{w.winfo_screenwidth()//2 - w.winfo_width()//2}+{w.winfo_screenheight()//2 - w.winfo_height()//2}")
        tk.Label(w, text="Automação ainda está aberto (60 min), cuidado com o consumo de memória Ram!. Recomendavel reiniciar o exacutável por segurança (ESC e reabrir)", padx=12, pady=8).pack()

        w.after(1000, w.destroy)
        w.mainloop()
        
        t0 = time.time()
        
        
        
        
    if keyboard.is_pressed("f1"):
        mouse_info()
        time.sleep(0.2)

    # ============================ F2 ============================
    if keyboard.is_pressed("f2"):

        texto = pyperclip.paste()

        PLACAS = [
            linha.strip()
            for linha in texto.splitlines()
            if linha.strip()
        ][:10]

        if not PLACAS:
            print("Nenhuma placa válida.")
            time.sleep(0.5)
            continue

        total = len(PLACAS)

        n1 = 1
        n2 = 1
        n3 = 1

        # cursor atual na lista (x fixo, y fixo do inicialy)
        inicial = inicialx

        if n1:
            for placa in PLACAS:
                close_program()

                pa.moveTo(inicial, inicialy)
                pa.click()

                pyperclip.copy(placa)

                pa.moveTo(*icone_lupa)
                pa.click()
                time.sleep(0.3)

                pa.moveTo(*esquerda_laranja_abrir_busca)
                cor = find_color()
                tentativas = 0

                while cor != (255, 182, 99):
                    close_program()
                    time.sleep(0.1)
                    tentativas += 1
                    cor = find_color()

                    if tentativas >= 7:
                        pa.moveTo(*icone_lupa)
                        pa.click()
                        pa.moveTo(*esquerda_laranja_abrir_busca)

                pa.moveTo(*campo_2_busca_placa)
                pa.click()
                pa.hotkey("ctrl", "a")
                pa.hotkey("ctrl", "v")
                pa.hotkey("enter")

                pa.moveTo(*meio_detectar_placa)
                cor = find_color()
                tentativas = 0

                while cor != (245, 245, 245):
                    close_program()
                    time.sleep(0.1)
                    cor = find_color()
                    tentativas += 1

                    if tentativas >= 7:
                        pa.moveTo(*campo_2_busca_placa)
                        pa.click()
                        pa.hotkey("ctrl", "a")
                        pa.hotkey("ctrl", "v")
                        pa.hotkey("enter")
                        pa.moveTo(*meio_detectar_placa)
                        tentativas = 0

                pa.moveTo(*meio_detectar_duas_placas)
                if find_color() != (255, 255, 255):
                    while not keyboard.is_pressed("f1"):
                        close_program()
                        time.sleep(0.3)
                else:
                    pa.moveTo(*abrir_chamado_placa)
                    pa.click()

                inicial += somar_proximaguia

        if n2:
            inicial = inicialx

            
            for _ in range(total):
                pa.moveTo(inicial, inicialy)
                pa.click()

                close_program()
                check_loading()

                pa.moveTo(*seta_historico_unidade_rastrada)
                pa.click()

                pa.moveTo(*abrir_historico_unidade)
                pa.click()

                inicial += somar_proximaguia

        if n3:
            inicial = inicialx

            for _ in range(total):
                close_program()

                pa.moveTo(inicial, inicialy)
                pa.click()

                close_program()
                check_loading()

                pa.moveTo(*abrir_historico)
                pa.click()
                close_program()

                pa.moveTo(*botao_ok_parte_preta)
                current_color = find_color()
                contador = 0
                tentativas_totais = 0
                tentativas_max = 100

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
                        pa.moveTo(*abrir_historico)
                        pa.click()
                        pa.moveTo(*botao_ok_parte_preta)
                        contador = 0

                close_program()
                pa.moveTo(*botao_menos)
                pa.click(clicks=10)

                time.sleep(0.5)

                pa.moveTo(*data_parte_esquerda)
                pa.mouseDown()
                pa.moveTo(*maximo_esquerda_na_tela)
                pa.mouseUp()

                # aqui você tinha "botao_ok" sem variável no json; mantive o que existe:
                pa.moveTo(*botao_ok_parte_preta)
                pa.click()

                pa.click()
                time.sleep(0.3)

                inicial += somar_proximaguia
            
            inicial = inicialx
            pa.moveTo(inicial, inicialy)
            pa.click()
            