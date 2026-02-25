import tkinter as tk
from tkinter import font as tkfont
import random
import math

# ══════════════════════════════════════════════════════
#  COLORES Y ESTILOS
# ══════════════════════════════════════════════════════
BG          = "#060811"
PANEL       = "#0d1117"
BORDER      = "#1a2332"
X_COLOR     = "#00f5d4"
O_COLOR     = "#f72585"
NEUTRAL     = "#8892a4"
TEXT        = "#e0e8ff"
ACCENT      = "#7209b7"
WIN_BG      = "#0d1f17"

DIFF_COLORS = {
    "Fácil":     "#00f5d4",
    "Normal":    "#b069f8",
    "Difícil":   "#f72585",
    "Imposible": "#ff4444",
}

# ══════════════════════════════════════════════════════
#  LÓGICA DEL JUEGO (puro Python, sin JS)
# ══════════════════════════════════════════════════════
COMBINACIONES_GANADORAS = [
    [0,1,2],[3,4,5],[6,7,8],  # filas
    [0,3,6],[1,4,7],[2,5,8],  # columnas
    [0,4,8],[2,4,6],          # diagonales
]

def verificar_ganador(tablero):
    """Retorna (ganador, línea) o (None, None)."""
    for linea in COMBINACIONES_GANADORAS:
        a, b, c = linea
        if tablero[a] and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a], linea
    if all(tablero):
        return "empate", []
    return None, None

def celdas_vacias(tablero):
    return [i for i, v in enumerate(tablero) if not v]

def minimax(tablero, es_ia, profundidad, alfa, beta):
    """Minimax con poda alfa-beta."""
    ganador, _ = verificar_ganador(tablero)
    if ganador == "O": return 10 - profundidad
    if ganador == "X": return profundidad - 10
    if ganador == "empate": return 0

    vacias = celdas_vacias(tablero)
    if not vacias: return 0

    if es_ia:
        mejor = -math.inf
        for i in vacias:
            tablero[i] = "O"
            mejor = max(mejor, minimax(tablero, False, profundidad + 1, alfa, beta))
            tablero[i] = None
            alfa = max(alfa, mejor)
            if beta <= alfa: break
        return mejor
    else:
        mejor = math.inf
        for i in vacias:
            tablero[i] = "X"
            mejor = min(mejor, minimax(tablero, True, profundidad + 1, alfa, beta))
            tablero[i] = None
            beta = min(beta, mejor)
            if beta <= alfa: break
        return mejor

def mejor_jugada(tablero):
    """Encuentra la mejor jugada para la IA (minimax perfecto)."""
    mejor_puntaje = -math.inf
    movimiento = -1
    for i in celdas_vacias(tablero):
        tablero[i] = "O"
        puntaje = minimax(tablero, False, 0, -math.inf, math.inf)
        tablero[i] = None
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            movimiento = i
    return movimiento

def jugada_ia(tablero, dificultad):
    """Selecciona jugada según dificultad."""
    vacias = celdas_vacias(tablero)
    if not vacias: return -1
    rand = lambda: random.choice(vacias)

    if dificultad == "Fácil":
        return rand() if random.random() < 0.90 else mejor_jugada(tablero)
    elif dificultad == "Normal":
        return rand() if random.random() < 0.50 else mejor_jugada(tablero)
    elif dificultad == "Difícil":
        return rand() if random.random() < 0.15 else mejor_jugada(tablero)
    else:  # Imposible
        return mejor_jugada(tablero)


# ══════════════════════════════════════════════════════
#  INTERFAZ GRÁFICA (Tkinter)
# ══════════════════════════════════════════════════════
class Totito:
    def __init__(self, root):
        self.root = root
        self.root.title("TOTITO")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Estado
        self.tablero      = [None] * 9
        self.juego_activo = True
        self.turno_humano = True
        self.dificultad   = tk.StringVar(value="Fácil")
        self.puntajes     = {"X": 0, "empate": 0, "O": 0}

        self._construir_ui()
        self._centrar_ventana(500, 680)

    # ── Construcción de la UI ──────────────────────────────────────────────
    def _construir_ui(self):
        # Fuentes
        self.fuente_titulo   = tkfont.Font(family="Courier", size=28, weight="bold")
        self.fuente_subtitulo= tkfont.Font(family="Courier", size=9)
        self.fuente_celda    = tkfont.Font(family="Courier", size=52, weight="bold")
        self.fuente_score    = tkfont.Font(family="Courier", size=22, weight="bold")
        self.fuente_label    = tkfont.Font(family="Courier", size=8)
        self.fuente_status   = tkfont.Font(family="Courier", size=11, weight="bold")
        self.fuente_btn      = tkfont.Font(family="Courier", size=9, weight="bold")
        self.fuente_diff     = tkfont.Font(family="Courier", size=8, weight="bold")

        pad = {"padx": 20}

        # ── Título
        tk.Label(self.root, text="T O T I T O", font=self.fuente_titulo,
                 bg=BG, fg=X_COLOR).pack(pady=(24, 0))

        # ── Selector de dificultad
        diff_frame = tk.Frame(self.root, bg=PANEL, bd=0, highlightthickness=1,
                              highlightbackground=BORDER)
        diff_frame.pack(fill="x", **pad, pady=(0, 12))

        self.diff_buttons = {}
        dificultades = ["Fácil", "Normal", "Difícil", "Imposible"]
        emojis        = ["😊", "😐", "😤", "💀"]
        for diff, emoji in zip(dificultades, emojis):
            btn = tk.Button(
                diff_frame, text=f"{emoji} {diff}",
                font=self.fuente_diff, bg=PANEL, fg=NEUTRAL,
                relief="flat", bd=0, padx=8, pady=8, cursor="hand2",
                activebackground=PANEL,
                command=lambda d=diff: self._cambiar_dificultad(d)
            )
            btn.pack(side="left", expand=True, fill="x")
            self.diff_buttons[diff] = btn
        self._actualizar_botones_diff()

        # ── Marcador
        score_frame = tk.Frame(self.root, bg=BG)
        score_frame.pack(fill="x", **pad, pady=(0, 10))

        # Jugador X
        self.card_x = self._crear_score_card(score_frame, "TÚ", "X", X_COLOR)
        self.card_x.pack(side="left", expand=True, fill="x", padx=(0, 4))

        # Empate
        card_e = self._crear_score_card(score_frame, "EMPATE", "—", NEUTRAL)
        card_e.pack(side="left", expand=True, fill="x", padx=4)

        # IA O
        self.card_o = self._crear_score_card(score_frame, "IA", "O", O_COLOR)
        self.card_o.pack(side="left", expand=True, fill="x", padx=(4, 0))

        # ── Status
        self.lbl_status = tk.Label(self.root, text="Tu turno",
                                   font=self.fuente_status, bg=BG, fg=X_COLOR)
        self.lbl_status.pack(pady=(4, 8))

        # ── Tablero
        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.pack(**pad, pady=(0, 10))

        self.canvas = tk.Canvas(board_frame, width=340, height=340,
                                bg=PANEL, highlightthickness=1,
                                highlightbackground=BORDER)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._click_tablero)
        self._dibujar_tablero()

        # ── Botones
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill="x", **pad, pady=(0, 20))

        tk.Button(btn_frame, text="↺  NUEVA PARTIDA",
                  font=self.fuente_btn, bg=PANEL, fg=TEXT,
                  relief="flat", bd=0, padx=12, pady=10,
                  highlightthickness=1, highlightbackground=BORDER,
                  cursor="hand2", activebackground=BORDER,
                  command=self.nueva_partida).pack(side="left", expand=True, fill="x", padx=(0, 6))

        tk.Button(btn_frame, text="⚡  RESET TOTAL",
                  font=self.fuente_btn, bg=PANEL, fg=TEXT,
                  relief="flat", bd=0, padx=12, pady=10,
                  highlightthickness=1, highlightbackground=BORDER,
                  cursor="hand2", activebackground=BORDER,
                  command=self.reset_total).pack(side="left", expand=True, fill="x", padx=(6, 0))

    def _crear_score_card(self, parent, label, simbolo, color):
        frame = tk.Frame(parent, bg=PANEL, bd=0,
                         highlightthickness=1, highlightbackground=BORDER)
        tk.Label(frame, text=label, font=self.fuente_label,
                 bg=PANEL, fg=NEUTRAL).pack(pady=(8, 0))
        tk.Label(frame, text=simbolo, font=tkfont.Font(family="Courier", size=18, weight="bold"),
                 bg=PANEL, fg=color).pack()
        score_lbl = tk.Label(frame, text="0",
                             font=self.fuente_score, bg=PANEL, fg=TEXT)
        score_lbl.pack(pady=(0, 8))

        # Guardar referencia al label del puntaje
        if simbolo == "X":
            self.score_x_lbl = score_lbl
        elif simbolo == "O":
            self.score_o_lbl = score_lbl
        else:
            self.score_e_lbl = score_lbl

        return frame

    # ── Tablero ────────────────────────────────────────────────────────────
    def _dibujar_tablero(self):
        c = self.canvas
        c.delete("all")

        # Líneas de la cuadrícula
        grosor = 2
        color_linea = BORDER
        # Verticales
        c.create_line(113, 28, 113, 312, fill=color_linea, width=grosor)
        c.create_line(227, 28, 227, 312, fill=color_linea, width=grosor)
        # Horizontales
        c.create_line(28, 113, 312, 113, fill=color_linea, width=grosor)
        c.create_line(28, 227, 312, 227, fill=color_linea, width=grosor)

        # Dibujar símbolos
        for i, val in enumerate(self.tablero):
            if val:
                self._dibujar_simbolo(i, val)

    def _celda_a_coordenadas(self, index):
        """Devuelve el centro (x, y) de una celda."""
        fila = index // 3
        col  = index % 3
        x = 28 + col * 114 + 57
        y = 28 + fila * 114 + 57 + (6 if fila == 0 else 0) - (6 if fila == 2 else 0)
        # Más simple:
        x = 57 + col * 114
        y = 57 + fila * 114
        return x, y

    def _dibujar_simbolo(self, index, simbolo, color=None):
        x, y = self._celda_a_coordenadas(index)
        col = color or (X_COLOR if simbolo == "X" else O_COLOR)
        self.canvas.create_text(x, y, text=simbolo, font=self.fuente_celda,
                                fill=col, tags=f"sym_{index}")

    def _click_tablero(self, event):
        if not self.juego_activo or not self.turno_humano:
            return
        col = event.x // (340 // 3)
        fila = event.y // (340 // 3)
        if col > 2 or fila > 2:
            return
        index = fila * 3 + col
        if self.tablero[index]:
            return
        self._realizar_jugada(index, "X")

    def _realizar_jugada(self, index, simbolo):
        self.tablero[index] = simbolo
        self._dibujar_simbolo(index, simbolo)

        ganador, linea = verificar_ganador(self.tablero)
        if ganador:
            self._fin_juego(ganador, linea)
            return

        if simbolo == "X":
            self.turno_humano = False
            self.lbl_status.config(text="IA pensando...", fg=O_COLOR)
            self.root.after(350, self._turno_ia)

    def _turno_ia(self):
        if not self.juego_activo:
            return
        movimiento = jugada_ia(self.tablero, self.dificultad.get())
        if movimiento != -1:
            self._realizar_jugada(movimiento, "O")
        if self.juego_activo:
            self.turno_humano = True
            self.lbl_status.config(text="Tu turno", fg=X_COLOR)

    def _fin_juego(self, ganador, linea):
        self.juego_activo = False
        self.turno_humano = False

        if ganador == "empate":
            self.puntajes["empate"] += 1
            self.lbl_status.config(text="¡Empate!", fg=NEUTRAL)
        elif ganador == "X":
            self.puntajes["X"] += 1
            self.lbl_status.config(text="¡Ganaste! 🏆", fg=X_COLOR)
            self._dibujar_linea_ganadora(linea, X_COLOR)
        else:
            self.puntajes["O"] += 1
            msgs = {
                "Fácil":     "¡Ganó la IA! (suerte de noob 😂)",
                "Normal":    "¡Ganó la IA! 🤖",
                "Difícil":   "¡Ganó la IA! Difícil, ¿eh? 😤",
                "Imposible": "¡Imposible de ganar! 💀",
            }
            self.lbl_status.config(text=msgs[self.dificultad.get()], fg=O_COLOR)
            self._dibujar_linea_ganadora(linea, O_COLOR)

        self._actualizar_puntajes()

    def _dibujar_linea_ganadora(self, linea, color):
        if not linea:
            return
        x1, y1 = self._celda_a_coordenadas(linea[0])
        x2, y2 = self._celda_a_coordenadas(linea[2])
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5,
                                capstyle="round", tags="win_line")

    # ── Marcador ───────────────────────────────────────────────────────────
    def _actualizar_puntajes(self):
        self.score_x_lbl.config(text=str(self.puntajes["X"]))
        self.score_o_lbl.config(text=str(self.puntajes["O"]))
        self.score_e_lbl.config(text=str(self.puntajes["empate"]))

    # ── Dificultad ─────────────────────────────────────────────────────────
    def _cambiar_dificultad(self, diff):
        self.dificultad.set(diff)
        self._actualizar_botones_diff()
        self.nueva_partida()

    def _actualizar_botones_diff(self):
        actual = self.dificultad.get()
        for diff, btn in self.diff_buttons.items():
            if diff == actual:
                btn.config(fg=DIFF_COLORS[diff],
                           bg="#111820",
                           relief="flat")
            else:
                btn.config(fg=NEUTRAL, bg=PANEL, relief="flat")

    # ── Reset ──────────────────────────────────────────────────────────────
    def nueva_partida(self):
        self.tablero      = [None] * 9
        self.juego_activo = True
        self.turno_humano = True
        self.lbl_status.config(text="Tu turno", fg=X_COLOR)
        self._dibujar_tablero()

    def reset_total(self):
        self.puntajes = {"X": 0, "empate": 0, "O": 0}
        self._actualizar_puntajes()
        self.nueva_partida()

    # ── Utilidades ─────────────────────────────────────────────────────────
    def _centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - ancho) // 2
        y = (sh - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")


# ══════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = Totito(root)
    root.mainloop()