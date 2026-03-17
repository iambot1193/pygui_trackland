import pyautogui as pa
import time
import keyboard
import pyperclip
import json
from pathlib import Path
import os
from tkinter import messagebox
import sys

# -*- coding: utf-8 -*-
"""
Fechador de Chamados SSX
Autor(a): Felipe Gonçalves Lopes
Adaptado para: Script .py e Executável .exe
"""

# ================= CONFIGURAÇÕES DE RECURSOS =================
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, compatível com PyInstaller e script .py """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Local do JSON: Sempre ao lado do executável/script principal
BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
ARQ = BASE_DIR / "coordsFechamento.json"

# Configurações do PyAutoGUI
pa.PAUSE = 0.05

# Bloqueio de teclas de sistema
teclas_bloqueio = ["f1", "esc", "f2", "f3", "f4", "f6", "f7", "f8"]
for tecla in teclas_bloqueio:
    keyboard.block_key(tecla)

# =================== LER COORDS DO JSON =====================
if not ARQ.exists():
    print(f"ERRO: O arquivo {ARQ.name} não foi encontrado!")
    time.sleep(5)
    sys.exit()

with ARQ.open("r", encoding="utf-8") as f:
    C = json.load(f)

def XY(nome: str):
    d = C[nome]
    return (d["x"], d["y"])

# Carregamento das coordenadas registradas
fone = XY("fone.png")
monitor = XY("monitor.png")
ok1 = XY("ok1.png")
ok2 = XY("ok2.png")
ok3 = XY("ok3.png")
ok4 = XY("ok4.png")

# Lógica de posicionamento e incremento
x_close_calls = ok1[0]
# Calcula a distância média entre as linhas de chamados
y_close_calls_sum = ((ok2[1] - ok1[1]) + (ok3[1] - ok2[1]) + (ok4[1] - ok3[1])) / 3
y_close_calls = ok1[1]

# Debug no console
print(f"Distância entre chamados (Y): {y_close_calls_sum:.2f}")
print(f"Iniciando em Y: {y_close_calls}")

# ===================== FUNÇÕES BASE =========================
def close_program():
    if keyboard.is_pressed("esc"):
        print("Saindo...")
        sys.exit()

def find_color():
    x, y = pa.position()
    # Screenshot de 1 pixel para verificação de cor
    img = pa.screenshot(region=(x, y, 1, 1))
    return img.getpixel((0, 0))

# =================== LOOP PRINCIPAL =========================
while True:
    time.sleep(0.1)
    close_program()    
        
    # Acionamento da automação via F2
    if keyboard.is_pressed('f2'):
        
        messagebox.showwarning("Atenção!", "O SCRIPT ESTÁ EM ANDAMENTO, PRESSIONE ESC QUANDO OS CHAMADOS ACABAREM!")
        time.sleep(0.2)

        print("F2 Pressionado - Iniciando Processo...")
        
        # Move para o ícone do telefone (Chamados)
        pa.moveTo(fone)
        call_color = find_color()
        
        # Enquanto o ícone estiver na cor laranja (notificação de chamados)
        while call_color == (217, 123, 76):
            close_program()
            
            time.sleep(0.1)
            pa.leftClick()
            
            # Move para o ponto de monitoramento para checar se o menu abriu
            pa.moveTo(monitor)
            time_try = 0
            checkload = find_color()
            
            # Aguarda o menu carregar (Cinza escuro)
            while checkload != (51, 51, 51):
                close_program()
                time.sleep(0.1)
                checkload = find_color()
                time_try += 1
                
                if time_try >= 20: # Timeout: tenta clicar no fone de novo
                    pa.moveTo(fone)
                    pa.leftClick()
                    pa.moveTo(monitor)
                    time_try = 0
            
            # Uma vez aberto, clica nos chamados em sequência
            while checkload == (51, 51, 51):
                close_program()
                
                pa.moveTo(x_close_calls, y_close_calls)
                pa.leftClick()
                
                # Re-checa se o menu ainda está ativo
                pa.moveTo(monitor)
                time.sleep(0.1)
                checkload = find_color()
                
                # Incrementa para o próximo chamado abaixo
                y_close_calls += y_close_calls_sum
                
                # Limite de segurança baseado no registro inicial (evita clicar fora da lista)
                if y_close_calls > (ok1[1] + (y_close_calls_sum * 10)): 
                    break
            
            # Finalizou a rodada ou fechou o menu
            time.sleep(1)
            pa.moveTo(fone)
            y_close_calls = ok1[1] # Reseta a posição vertical
            call_color = find_color() # Checa se ainda há chamados laranja