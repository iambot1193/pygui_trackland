import keyboard
import time
import pyautogui as pa
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
import json

# -*- coding: utf-8 -*-
"""
Registrador de Coordenadas SSX
Autor(a): Felipe Gonçalves Lopes
Criado em: 2026-01-16
Versão: 1.0.0
Direitos: (c) 2026 Felipe Gonçalves Lopes. Todos os direitos reservados.
"""


# ===========================
keyboard.block_key("esc")
# ===========================

BASE = Path(__file__).resolve().parent  # BASE = .../scripts
  # sobe 1 nível, sai de /imagens
IMAGENS = [
    BASE / "imagens" / "imagem_menu1.png",
    BASE / "imagens" / "imagem_menu2.png",
    BASE / "imagens" / "inicialx, inicialy.png",
    BASE / "imagens" / "pag2.png",
    BASE / "imagens" / "pag3.png",
    BASE / "imagens" / "icone_lupa.png",
    BASE / "imagens" / "esquerda_laranja_abrir_busca.png",
    BASE / "imagens" / "campo_2_busca_placa.png",
    BASE / "imagens" / "meio_detectar_placa.png",
    BASE / "imagens" / "meio_detectar_duas_placas.png",
    BASE / "imagens" / "abrir_chamado_placa.png",
    BASE / "imagens" / "seta_historico_unidade_rastrada.png",
    BASE / "imagens" / "abrir_historico_unidade.png",
    BASE / "imagens" / "abrir_historico.png",
    BASE / "imagens" / "botao_ok_parte_preta.png",
    BASE / "imagens" / "botao_menos.png",
    BASE / "imagens" / "data_parte_esquerda.png",
    BASE / "imagens" / "maximo_esquerda_na_tela.png",
]

import sys
from pathlib import Path

BASE = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
ARQ = BASE / "coords.json"

if ARQ.exists():
    with ARQ.open("r", encoding="utf-8") as f:
        coords_salvas = json.load(f)
else:
    coords_salvas = {}

if "inicialx, inicialy.png" in coords_salvas:
    coords_salvas.setdefault(
        "inicialx.png",
        {"x": coords_salvas["inicialx, inicialy.png"].get("x")},
    )
    coords_salvas.setdefault(
        "inicialy.png",
        {"y": coords_salvas["inicialx, inicialy.png"].get("y")},
    )


def mouse_info():
    time.sleep(0.01)
    mouse_x, mouse_y = pa.position()
    print(f"  ({mouse_x}, {mouse_y})")
    return {"x": mouse_x, "y": mouse_y}


messagebox.showwarning(
    "Atenção!", "ABRA UMA NOVA GUIA DE 10 PAGINAS DA SSX ANTES DE CONTINUAR!"
)
time.sleep(0.2)

messagebox.showwarning(
    "Atenção!", "Deixe o mouse na mesma posição relativa a sua ssx, e siga as instuções"
)
time.sleep(0.2)


class Viewer(tk.Tk):
    def __init__(self, imagens):
        super().__init__()

        self.coords = dict(coords_salvas)
        self.imagens = imagens
        self.idx = 0

        # deixa sempre por cima, mas NÃO rouba foco sozinho
        self.attributes("-topmost", True)

        self.lbl = tk.Label(self, bg="black")
        self.lbl.pack(fill="both", expand=True)

        self.info = tk.Label(
            self, text="APERTE F1 PARA AVANÇAR", font=("Segoe UI", 11, "bold")
        )
        self.info.pack(fill="x")

        self._foto = None

        # F1 global: se estiver fora de foco, traz a janela e avança
        keyboard.on_press_key("f1", self._on_f1)

        self._bring_to_front()
        self.mostrar()

    def _bring_to_front(self):
        self.lift()
        self.deiconify()
        self.focus_force()

    def _on_f1(self, e=None):
        # se estiver fora de foco, puxa foco e avança logo depois
        if self.focus_displayof() is None:
            self.after(0, self._bring_to_front)
            self.after(30, self.proximo)
            return
        self.after(0, self.proximo)

    def mostrar(self):
        if self.idx >= len(self.imagens):
            self.lbl.config(
                image="",
                text="FINALIZADO!",
                fg="white",
                font=("Segoe UI", 28, "bold"),
            )
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

            if chave == "inicialx, inicialy.png":
                self.coords["inicialx.png"] = {"x": pos["x"]}
                self.coords["inicialy.png"] = {"y": pos["y"]}
            else:
                self.coords[chave] = pos

            if chave == "pag3.png":
                try:
                    inicial_x = self.coords["inicialx.png"]["x"]
                    pag2 = self.coords["pag2.png"]
                    pag3 = self.coords["pag3.png"]

                    somar_proximaguia = (
                        (pag2["x"] - inicial_x) + (pag3["x"] - pag2["x"])
                    ) / 2

                    prox_x = int(round(pag3["x"] + somar_proximaguia))
                    self.coords["somar_proximaguia"] = somar_proximaguia

                    print("SOMAR_PROXIMAGUIA:", somar_proximaguia)
                    print("VAI CLICAR NA PRÓXIMA GUIA EM X:", prox_x)

                    time.sleep(0.15)

                except KeyError as e:
                    print("ERRO: faltou coordenada para calcular somar_proximaguia:", e)

        self.idx += 1
        self.mostrar()

        if self.idx >= len(self.imagens):
            with ARQ.open("w", encoding="utf-8") as f:
                json.dump(self.coords, f, ensure_ascii=False, indent=2)

            print("COORDENADAS SALVAS:", self.coords)
            print("SALVO EM:", ARQ)


Viewer(IMAGENS).mainloop()
