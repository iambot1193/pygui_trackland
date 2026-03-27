import pyautogui as pa
import time
import keyboard
import pyperclip
import json
from pathlib import Path
import winsound
from tkinter import messagebox
import tkinter as tk
import sys
import threading


"""
Buscador de Placas SSX
Autor(a): Felipe Gonçalves Lopes
Criado em: 2026-01-16
Versão: 1.1
Direitos: (c) 2026 Felipe Gonçalves Lopes. Todos os direitos reservados.
"""

# ================= CONFIGURAÇÕES ============================
pa.PAUSE = 0.05 

keyboard.block_key("esc")
keyboard.block_key("f2")
keyboard.block_key("f1")
# ============================================================

# =================== LER COORDS DO JSON =====================


BASE = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
ARQ = BASE / "coords.json"



with ARQ.open("r", encoding="utf-8") as f:
    C = json.load(f)

######################################################################################
label_status = None
root_overlay = None

def iniciar_overlay():
    global label_status, root_overlay
    root_overlay = tk.Tk()
    
    # --- CONFIGURAÇÕES VISUAIS ---
    root_overlay.overrideredirect(True) # Remove bordas e botões de fechar
    root_overlay.attributes("-topmost", True) # Mantém no topo das outras janelas
    root_overlay.configure(bg="black")
    
    # --- POSICIONAMENTO NO CANTO INFERIOR ---
    largura, altura = 300, 40
    posX = 10
    # O winfo_screenheight pega a altura total. 
    # Subtraímos a altura da janela e +60px para ficar acima da barra de tarefas.
    posY = root_overlay.winfo_screenheight() - altura - 60 
    
    root_overlay.geometry(f"{largura}x{altura}+{posX}+{posY}")

    label_status = tk.Label(
        root_overlay, 
        text="AGUARDANDO...", 
        fg="red", 
        bg="black", 
        font=("Arial", 11, "bold")
    )
    label_status.pack(expand=True, fill='both')
    
    root_overlay.mainloop()

# Inicia a janela em uma via paralela para não travar o script
threading.Thread(target=iniciar_overlay, daemon=True).start()

def popup(estado):
    mensagens = {
        0: "script de busca pronto!",
        1: "buscando placas..",
        2: "Erro! Veículo com 2 placas!",
        3: "abrindo histórico..", # Estado final/reset
    }
    texto = mensagens.get(estado, "Status desconhecido")
    
    # Atualiza o texto na interface se ela já existir
    if label_status:
        label_status.config(text=texto.upper())
        # Se for erro (estado 2), podemos fazer piscar ou mudar cor
        if estado == 2:
            label_status.config(fg="yellow") 
        else:
            label_status.config(fg="red")

######################################################################################




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
    



################# LOOP PRINCIPAL #############################
t0 = time.time()

while True:
    
    popup(0)

    
    time.sleep(0.3)
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

    # ============================ F2 ============================
    if keyboard.is_pressed("f2"):
        popup(1)

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
                time.sleep(0.4)

                pa.moveTo(*esquerda_laranja_abrir_busca)
                cor = find_color()
                tentativas = 0

                while cor != (255, 182, 99):
                    close_program()
                    time.sleep(0.3)
                    cor = find_color()
                    if cor == (255,182,99):
                        break
                    tentativas += 9
                    if tentativas >= 7:
                        pa.moveTo(*icone_lupa)
                        pa.click()
                        pa.moveTo(*esquerda_laranja_abrir_busca)
                        tentativas = 0

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
                    popup(2)
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
                time.sleep(0.2)
                pa.click()

                pa.moveTo(*abrir_historico_unidade)
                pa.click()

                inicial += somar_proximaguia

        if n3:
            popup(3)
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
                pa.click(clicks=7)

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
            
            for _ in range(total):
                close_program()
                check_loading()
                
                pa.moveTo(inicial, inicialy)
                pa.click()
                inicial += somar_proximaguia
            
            inicial = inicialx
            pa.moveTo(inicial, inicialy)
            pa.click()