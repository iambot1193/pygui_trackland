import tkinter as tk
from tkinter import ttk
import platform

def executar():
    # ===== CONFIGURAÇÕES =====
    TITULO_JANELA = ""
    LARGURA, ALTURA = 380, 280
    MARGEM_X, MARGEM_Y = 12, 12
    OPACIDADE = 0.98
    BORDA = False
    CLICK_THROUGH = False
    FONTE_LINHA = ("Segoe UI", 8)
    BTN_W = 8
    # ==========================

    # Itens (linhas)
    ITENS = [
        "S COMUNICAÇÃO.",
        "RESET.",
        "BUZZER VIOLADO.",
        "SALTOS.",
        "IGNIÇÃO VIOLADA.",
        "MAL CONTATO BACKUP.",
        "BACKUP NUNCA TEM CARGA.",
        "S DADOS O SUFICIENTE",
        "POSIÇÃO IG OFF.",
        "BATERIA VIOLADA PORTAL.",
        "SALTOS IG OFF.",
        "GPS TRAVADO."
    ]

    # Mapas (Situação / Ação / Motivo)
    MAPA = {
        "S COMUNICAÇÃO.": {
            "situacao": "Sem comunicação.",
            "acao": "Contatar cliente.",
            "motivo": "SEM COMUNICAÇÃO."
        },
        "RESET.": {
            "situacao": "Veículo apresenta pequenos saltos e travamentos durante a rota.",
            "acao": "Enviar reset.",
            "motivo": "PEQUENOS SALTOS E TRAVAMENTOS."
        },
        "BUZZER VIOLADO.": {
            "situacao": "Veículo apresenta possível violação de buzzer, faz maior parte da rota sem identificação de motorista.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "SALTOS.": {
            "situacao": "Veículo apresenta saltos e travamentos durante a rota.",
            "acao": "Agendar manutenção.",
            "motivo": "SALTOS E TRAVAMENTOS."
        },
        "IGNIÇÃO VIOLADA.": {
            "situacao": "Veículo apresenta sensor de ignição violado durante a rota.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "MAL CONTATO BACKUP.": {
            "situacao": "Bateria backup apresenta mal contato durante a rota.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "BACKUP NUNCA TEM CARGA.": {
            "situacao": "Bateria backup nunca tem carga, mesmo com ignição ligada.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "S DADOS O SUFICIENTE": {
            "situacao": "Veículo não apresentou dados o suficiente. Aguardar próxima análise.",
            "acao": "Em observação.",
            "motivo": None
        },
        "POSIÇÃO IG OFF.": {
            "situacao": "Veículo apresentou posição com a ignição desligada.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "BATERIA VIOLADA PORTAL.": {
            "situacao": "Veículo apresentou violação de bateria indicado pelo portal SSX.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "SALTOS IG OFF.": {
            "situacao": "Veículo apresentou saltos e travamentos com a ignição desligada durante a rota.",
            "acao": "Agendar manutenção.",
            "motivo": "POSSÍVEL VIOLAÇÃO."
        },
        "GPS TRAVADO.": {
            "situacao": "Veículo apresenta gps travado durante a rota.",
            "acao": "Agendar manutenção.",
            "motivo": "GPS TRAVADO."
        },
    }

    # pyperclip (opcional)
    try:
        import pyperclip
        _HAS_PYPERCLIP = True
    except Exception:
        pyperclip = None
        _HAS_PYPERCLIP = False

    class Overlay(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title(TITULO_JANELA)
            if BORDA:
                self.overrideredirect(True)
            self.attributes("-topmost", True)
            self.attributes("-alpha", OPACIDADE)
            self.configure(bg="#000000")

            # Posição da janela
            self.geometry(f"{LARGURA}x{ALTURA}+0+0")
            self.update_idletasks()
            sw = self.winfo_screenwidth()
            x = sw - LARGURA - MARGEM_X
            y = MARGEM_Y
            self.geometry(f"{LARGURA}x{ALTURA}+{x}+{y}")

            # Container principal
            cont = tk.Frame(self, bg="#000000")
            cont.pack(fill="both", expand=True, padx=6, pady=6)

            # Área rolável
            canvas = tk.Canvas(cont, bg="#000000", highlightthickness=0)
            scroll_y = ttk.Scrollbar(cont, orient="vertical", command=canvas.yview)
            frame_rows = tk.Frame(canvas, bg="#000000")
            frame_rows.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=frame_rows, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)
            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")

            # Estilo dos botões
            style = ttk.Style()
            try:
                style.theme_use("clam")
            except Exception:
                pass
            style.configure("TL.TButton", padding=(4, 1))

            # Criação das linhas
            for i, item in enumerate(ITENS, start=1):
                # alternar entre preto e branco
                bg_color = "#000000" if i % 2 == 0 else "#ffffff"
                fg_color = "#ffffff" if bg_color == "#000000" else "#000000"

                row = tk.Frame(frame_rows, bg=bg_color)
                row.grid(row=i, column=0, sticky="ew", pady=0)
                row.columnconfigure(0, weight=1)

                lbl = tk.Label(row, text=item, bg=bg_color, fg=fg_color,
                               font=FONTE_LINHA, anchor="w")
                lbl.grid(row=0, column=0, sticky="w")

                btns = tk.Frame(row, bg=bg_color)
                btns.grid(row=0, column=1, sticky="e")

                m = MAPA.get(item) or MAPA.get("S COMUNICAÇÃO.")

                ttk.Button(
                    btns, text="Situação", style="TL.TButton", width=BTN_W,
                    command=lambda t=m["situacao"]: self._copy(t, "Situação copiada!")
                ).pack(side="left", padx=(0, 4))

                ttk.Button(
                    btns, text="Ação", style="TL.TButton", width=BTN_W,
                    command=lambda t=m["acao"]: self._copy(t, "Ação copiada!")
                ).pack(side="left", padx=(0, 4))

                if m.get("motivo"):
                    ttk.Button(
                        btns, text="Motivo", style="TL.TButton", width=BTN_W,
                        command=lambda t=m["motivo"]: self._copy(t, "Motivo copiado!")
                    ).pack(side="left")
                else:
                    ttk.Button(
                        btns, text="Motivo", style="TL.TButton", width=BTN_W,
                        state="disabled", takefocus=0
                    ).pack(side="left")

            # Status inferior
            self.status = tk.Label(cont,
                                   text="ESC fecha • Clique em Situação/Ação/Motivo para copiar",
                                   bg="#000000", fg="#bbbbbb", anchor="w", font=("Segoe UI", 7))
            self.status.pack(fill="x", pady=(4, 0))

            # Tecla ESC fecha
            self.bind("<Escape>", lambda e: self.destroy())
            self.protocol("WM_DELETE_WINDOW", self.destroy)

            # Arrastar quando sem borda
            if BORDA:
                for w in (self, cont, canvas, frame_rows):
                    w.bind("<Button-1>", self._start_move)
                    w.bind("<B1-Motion>", self._on_move)

            # Click-through opcional
            if CLICK_THROUGH and platform.system() == "Windows":
                self.after(100, self._enable_click_through_windows)

            # Scroll do mouse
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        def _copy(self, text, ok_msg):
            try:
                if _HAS_PYPERCLIP:
                    pyperclip.copy(text)
                else:
                    self.clipboard_clear()
                    self.clipboard_append(text)
            except Exception as e:
                self.status.config(text=f"Erro ao copiar: {e}")
                return
            self.status.config(text=ok_msg)
            self.after(800, lambda: self.status.config(
                text="ESC fecha • Clique em Situação/Ação/Motivo para copiar"))

        def _start_move(self, e):
            self._ox, self._oy = e.x, e.y

        def _on_move(self, e):
            self.geometry(f"+{self.winfo_x() + (e.x - self._ox)}+{self.winfo_y() + (e.y - self._oy)}")

        def _enable_click_through_windows(self):
            import ctypes
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            hwnd = self.winfo_id()
            user32 = ctypes.windll.user32
            get = user32.GetWindowLongW
            set_ = user32.SetWindowLongW
            style = get(hwnd, GWL_EXSTYLE)
            set_(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

    Overlay().mainloop()

if __name__ == "__main__":
    executar()
