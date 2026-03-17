import keyboard
import time
import pyautogui as pa
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
import json
import os
import sys

# -*- coding: utf-8 -*-
"""
Registrador de Coordenadas SSX
Autor(a): Felipe Gonçalves Lopes
Criado em: 2026-03-16
Versão: 1.1.0
"""

# ================= CONFIGURAÇÕES DE CAMINHO =================
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, compatível com PyInstaller e script .py """
    try:
        # Caminho temporário do PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Define onde o JSON será salvo (sempre ao lado do executável final)
BASE_EXE = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
ARQ = BASE_EXE / "coordsFechamento.json"

# Define as imagens usando a função de recurso (para funcionar dentro do EXE)
IMAGENS_NOMES = ["fone.png", "monitor.png", "ok1.png", "ok2.png", "ok3.png", "ok4.png"]
IMAGENS = [resource_path(os.path.join("imagens", img)) for img in IMAGENS_NOMES]

# ============================================================

keyboard.block_key("esc")

# Carregamento robusto do JSON
if ARQ.exists():
    with ARQ.open("r", encoding="utf-8") as f:
        try:
            conteudo = f.read().strip()
            coords_salvas = json.loads(conteudo) if conteudo else {}
        except json.JSONDecodeError:
            coords_salvas = {}
else:
    coords_salvas = {}

def mouse_info():
    time.sleep(0.01)
    mouse_x, mouse_y = pa.position()
    print(f"  ({mouse_x}, {mouse_y})")
    return {"x": mouse_x, "y": mouse_y}

messagebox.showwarning("Atenção!", "ABRA UMA PAGINA DA SSX ANTES DE CONTINUAR!")
time.sleep(0.2)
messagebox.showwarning("Atenção!", "Deixe o mouse na mesma posição relativa a sua ssx, e siga as instuções")
time.sleep(0.2)

class Viewer(tk.Tk):
    def __init__(self, imagens):
        super().__init__()
        self.coords = dict(coords_salvas)
        self.imagens = imagens
        self.idx = 0
        self.attributes("-topmost", True)
        self.lbl = tk.Label(self, bg="black")
        self.lbl.pack(fill="both", expand=True)
        self.info = tk.Label(self, text="APERTE F1 PARA AVANÇAR", font=("Segoe UI", 11, "bold"))
        self.info.pack(fill="x")
        self._foto = None
        keyboard.on_press_key("f1", self._on_f1)
        self._bring_to_front()
        self.mostrar()

    def _bring_to_front(self):
        self.lift()
        self.deiconify()
        self.focus_force()

    def _on_f1(self, e=None):
        if self.focus_displayof() is None:
            self.after(0, self._bring_to_front)
            self.after(30, self.proximo)
            return
        self.after(0, self.proximo)

    def mostrar(self):
        if self.idx >= len(self.imagens):
            self.lbl.config(image="", text="FINALIZADO!", fg="white", font=("Segoe UI", 28, "bold"))
            self.info.config(text="")
            return
        img = Image.open(self.imagens[self.idx])
        self._foto = ImageTk.PhotoImage(img)
        self.lbl.config(image=self._foto, text="")
        self.info.config(text=f"PASSO {self.idx+1}/{len(self.imagens)} — F1 PARA PRÓXIMO")

    def proximo(self, event=None):
        if self.idx < len(self.imagens):
            chave = Path(self.imagens[self.idx]).name
            pos = mouse_info()
            self.coords[chave] = pos

        self.idx += 1
        self.mostrar()

        if self.idx >= len(self.imagens):
            with ARQ.open("w", encoding="utf-8") as f:
                json.dump(self.coords, f, ensure_ascii=False, indent=2)
            print("COORDENADAS SALVAS:", self.coords)
            print("SALVO EM:", ARQ)

if __name__ == "__main__":
    Viewer(IMAGENS).mainloop()