# ══════════════════════════════════════════════════════════════════════════════
#  TOTITO CON IA — Tkinter + Minimax
#  Librerías usadas:
#    - tkinter: interfaz gráfica de escritorio (viene con Python)
#    - random:  números aleatorios para simular errores en dificultades bajas
#    - math:    usamos math.inf (infinito) como valor inicial en minimax
# ══════════════════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import font as tkfont  # módulo de fuentes dentro de tkinter
import random
import math


# ══════════════════════════════════════════════════════════════════════════════
#  PALETA DE COLORES
#  Todos los colores están centralizados aquí como constantes.
#  Así si quieres cambiar un color, solo lo cambias en un lugar.
# ══════════════════════════════════════════════════════════════════════════════
BG      = "#060811"  # fondo principal (casi negro azulado)
PANEL   = "#0d1117"  # fondo de paneles/cards
BORDER  = "#1a2332"  # color de bordes
X_COLOR = "#00f5d4"  # color del jugador X (cian)
O_COLOR = "#f72585"  # color de la IA O (magenta)
NEUTRAL = "#8892a4"  # color de texto secundario (gris azulado)
TEXT    = "#e0e8ff"  # color de texto principal
ACCENT  = "#7209b7"  # color de acento (morado, reservado)
WIN_BG  = "#0d1f17"  # fondo al ganar (verde oscuro, reservado)

# Color del botón activo según dificultad
DIFF_COLORS = {
    "Fácil":   "#00f5d4",  # cian
    "Normal":  "#b069f8",  # morado claro
    "Difícil": "#ff4444",  # rojo (antes Imposible)
}


# ══════════════════════════════════════════════════════════════════════════════
#  LÓGICA DEL JUEGO (funciones puras, sin interfaz gráfica)
#
#  El tablero se representa como una lista de 9 elementos:
#
#    [0][1][2]
#    [3][4][5]   →  lista: [0, 1, 2, 3, 4, 5, 6, 7, 8]
#    [6][7][8]
#
#  Cada celda puede ser: None (vacía), "X" (jugador) o "O" (IA)
# ══════════════════════════════════════════════════════════════════════════════

# Todas las combinaciones posibles para ganar el juego.
# Son 8 en total: 3 filas + 3 columnas + 2 diagonales.
COMBINACIONES_GANADORAS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # filas
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columnas
    [0, 4, 8], [2, 4, 6],             # diagonales
]


def verificar_ganador(tablero):
    """
    Revisa si hay un ganador o empate en el tablero actual.

    Recorre cada combinación ganadora y verifica si las 3 celdas
    tienen el mismo símbolo (y no están vacías).

    Retorna:
        (símbolo, línea)  → si alguien ganó, ej: ("X", [0,1,2])
        ("empate", [])    → si todas las celdas están llenas y nadie ganó
        (None, None)      → si el juego sigue en curso
    """
    for linea in COMBINACIONES_GANADORAS:
        a, b, c = linea  # desempaquetar los 3 índices de la línea
        # Si la celda 'a' no es None y las 3 son iguales → hay ganador
        if tablero[a] and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a], linea

    # Si no hay ganador pero todas las celdas están llenas → empate
    if all(tablero):
        return "empate", []

    # Si hay celdas vacías y nadie ganó → el juego continúa
    return None, None


def celdas_vacias(tablero):
    """
    Retorna una lista con los índices de las celdas que están vacías (None).
    Ejemplo: si el tablero es [X, None, O, None, ...] retorna [1, 3, ...]
    Usamos enumerate() para obtener tanto el índice como el valor.
    """
    return [i for i, v in enumerate(tablero) if not v]


def minimax(tablero, es_ia, profundidad, alfa, beta):
    """
    Algoritmo Minimax con poda Alfa-Beta.

    Es un algoritmo de búsqueda recursiva que simula TODOS los posibles
    movimientos futuros del juego y elige el que maximiza las chances de la IA
    mientras minimiza las del jugador humano.

    Parámetros:
        tablero     → estado actual del juego (lista de 9)
        es_ia       → True si es el turno de la IA (maximizar), False si es el jugador (minimizar)
        profundidad → qué tan profundo estamos en el árbol de decisiones
        alfa        → el mejor puntaje que ya encontró el maximizador (IA)
        beta        → el mejor puntaje que ya encontró el minimizador (jugador)

    Retorna un puntaje numérico:
        +10 (menos profundidad) → la IA gana
        -10 (más profundidad)   → el jugador gana
         0                      → empate

    Por qué restar/sumar la profundidad:
        - Si la IA puede ganar en 1 movimiento vs 3 movimientos, prefiere ganar antes.
        - Si el jugador puede ganar, la IA prefiere que tarde más.

    Poda Alfa-Beta:
        Optimización que corta ramas del árbol que no van a afectar el resultado.
        Si alfa >= beta → esa rama no puede mejorar el resultado → la ignoramos.
        Esto hace el algoritmo mucho más rápido sin cambiar el resultado.
    """

    # ── Casos base (condiciones de término) ──────────────────────────────────
    ganador, _ = verificar_ganador(tablero)
    if ganador == "O":
        return 10 - profundidad   # la IA ganó (mientras más rápido, mejor puntaje)
    if ganador == "X":
        return profundidad - 10   # el jugador ganó (puntaje negativo para la IA)
    if ganador == "empate":
        return 0                  # nadie ganó

    vacias = celdas_vacias(tablero)
    if not vacias:
        return 0  # tablero lleno sin ganador

    # ── Turno de la IA (MAXIMIZADOR) ─────────────────────────────────────────
    # La IA quiere el puntaje MÁS ALTO posible
    if es_ia:
        mejor = -math.inf  # empezamos con el peor puntaje posible para el maximizador
        for i in vacias:
            tablero[i] = "O"          # simular jugada de la IA
            # llamada recursiva, ahora es turno del jugador (minimizador)
            puntaje = minimax(tablero, False, profundidad + 1, alfa, beta)
            tablero[i] = None         # deshacer la jugada (backtracking)
            mejor = max(mejor, puntaje)
            alfa = max(alfa, mejor)   # actualizar el mejor puntaje del maximizador
            if beta <= alfa:
                break  # poda: el minimizador nunca elegiría esta rama
        return mejor

    # ── Turno del jugador (MINIMIZADOR) ──────────────────────────────────────
    # El jugador quiere el puntaje MÁS BAJO posible (perjudica a la IA)
    else:
        mejor = math.inf  # empezamos con el peor puntaje posible para el minimizador
        for i in vacias:
            tablero[i] = "X"          # simular jugada del jugador
            # llamada recursiva, ahora es turno de la IA (maximizador)
            puntaje = minimax(tablero, True, profundidad + 1, alfa, beta)
            tablero[i] = None         # deshacer la jugada (backtracking)
            mejor = min(mejor, puntaje)
            beta = min(beta, mejor)   # actualizar el mejor puntaje del minimizador
            if beta <= alfa:
                break  # poda: el maximizador nunca elegiría esta rama
        return mejor


def mejor_jugada(tablero):
    """
    Encuentra el índice de la celda donde la IA debería jugar.

    Prueba cada celda vacía, llama a minimax para evaluar qué tan buena
    es esa jugada, y se queda con la que tenga el mayor puntaje.

    Retorna el índice (0-8) de la mejor celda, o -1 si no hay celdas vacías.
    """
    mejor_puntaje = -math.inf
    movimiento = -1

    for i in celdas_vacias(tablero):
        tablero[i] = "O"  # probar esta jugada
        # evaluar con minimax — es_ia=False porque después le toca al jugador
        puntaje = minimax(tablero, False, 0, -math.inf, math.inf)
        tablero[i] = None  # deshacer (backtracking)

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            movimiento = i  # guardar el índice de la mejor jugada

    return movimiento


def jugada_ia(tablero, dificultad):
    """
    Decide qué celda juega la IA según la dificultad seleccionada.

    La dificultad se simula mezclando jugadas aleatorias (malas) con
    la jugada óptima del minimax. Cuanto más fácil, más aleatoria es la IA.

    Probabilidades de jugar de forma aleatoria (mala):
        Fácil:     90% random — la IA casi siempre juega mal
        Normal:    50% random — mitad y mitad
        Difícil:   15% random — casi siempre juega bien, pero comete errores
        Imposible:  0% random — siempre minimax perfecto, no se puede ganar
    """
    vacias = celdas_vacias(tablero)
    if not vacias:
        return -1  # no hay donde jugar

    rand = lambda: random.choice(vacias)  # función auxiliar para elegir al azar

    if dificultad == "Fácil":
        return rand() if random.random() < 0.90 else mejor_jugada(tablero)
    elif dificultad == "Normal":
        return rand() if random.random() < 0.50 else mejor_jugada(tablero)
    else:  # Difícil — minimax perfecto (antes era Imposible)
        return mejor_jugada(tablero)


# ══════════════════════════════════════════════════════════════════════════════
#  INTERFAZ GRÁFICA — Clase Totito
#
#  Tkinter funciona con widgets (Label, Button, Canvas, Frame) que se
#  organizan con el método .pack() o .grid().
#
#  El Canvas es un widget especial donde podemos dibujar líneas y texto
#  manualmente con coordenadas (x, y) — lo usamos para el tablero de juego.
# ══════════════════════════════════════════════════════════════════════════════
class Totito:
    def __init__(self, root):
        """
        Constructor de la clase. Se ejecuta al crear el objeto.
        Recibe 'root' que es la ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("TOTITO — IA")
        self.root.configure(bg=BG)        # color de fondo de la ventana
        self.root.resizable(False, False) # no se puede redimensionar

        # ── Estado del juego ──────────────────────────────────────────────────
        self.tablero      = [None] * 9   # 9 celdas vacías al inicio
        self.juego_activo = True         # False cuando termina la partida
        self.turno_humano = True         # True = jugador, False = IA
        self.dificultad   = tk.StringVar(value="Fácil")  # variable de Tkinter para el texto
        self.puntajes     = {"X": 0, "empate": 0, "O": 0}

        self._construir_ui()              # construir todos los widgets
        self._centrar_ventana(500, 680)   # centrar en pantalla

    # ──────────────────────────────────────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ──────────────────────────────────────────────────────────────────────────
    def _construir_ui(self):
        """
        Crea y posiciona todos los widgets de la ventana.
        Se llama una sola vez al iniciar el programa.
        """

        # ── Fuentes ───────────────────────────────────────────────────────────
        # tkfont.Font() crea objetos de fuente reutilizables
        self.fuente_titulo    = tkfont.Font(family="Courier", size=28, weight="bold")
        self.fuente_subtitulo = tkfont.Font(family="Courier", size=9)
        self.fuente_celda     = tkfont.Font(family="Courier", size=52, weight="bold")  # X y O grandes
        self.fuente_score     = tkfont.Font(family="Courier", size=22, weight="bold")
        self.fuente_label     = tkfont.Font(family="Courier", size=8)
        self.fuente_status    = tkfont.Font(family="Courier", size=11, weight="bold")
        self.fuente_btn       = tkfont.Font(family="Courier", size=9, weight="bold")
        self.fuente_diff      = tkfont.Font(family="Courier", size=8, weight="bold")

        pad = {"padx": 20}  # padding horizontal reutilizable

        # ── Título ────────────────────────────────────────────────────────────
        # tk.Label() crea una etiqueta de texto
        # .pack() la agrega a la ventana — pady=(arriba, abajo)
        tk.Label(self.root, text="T O T I T O", font=self.fuente_titulo,
                 bg=BG, fg=X_COLOR).pack(pady=(24, 0))
        tk.Label(self.root, text="INTELIGENCIA ARTIFICIAL", font=self.fuente_subtitulo,
                 bg=BG, fg=NEUTRAL).pack(pady=(2, 16))

        # ── Botones de dificultad ─────────────────────────────────────────────
        # Frame = contenedor invisible para agrupar widgets en fila
        diff_frame = tk.Frame(self.root, bg=PANEL, bd=0,
                              highlightthickness=1, highlightbackground=BORDER)
        diff_frame.pack(fill="x", **pad, pady=(0, 12))  # fill="x" → ocupa todo el ancho

        self.diff_buttons = {}  # dict para guardar referencia a cada botón
        dificultades = ["Fácil", "Normal", "Difícil"]
        emojis        = ["😊",    "😐",     "💀"]

        for diff, emoji in zip(dificultades, emojis):
            btn = tk.Button(
                diff_frame,
                text=f"{emoji} {diff}",
                font=self.fuente_diff,
                bg=PANEL, fg=NEUTRAL,
                relief="flat",           # sin borde en relieve
                bd=0,
                padx=8, pady=8,
                cursor="hand2",          # cursor de manita al pasar encima
                activebackground=PANEL,
                # lambda con d=diff captura el valor actual de diff en el loop
                # sin esto, todos los botones llamarían con el último valor del loop
                command=lambda d=diff: self._cambiar_dificultad(d)
            )
            btn.pack(side="left", expand=True, fill="x")  # todos en la misma fila
            self.diff_buttons[diff] = btn  # guardar para modificarlo después

        self._actualizar_botones_diff()  # resaltar el botón activo al inicio

        # ── Marcador ──────────────────────────────────────────────────────────
        score_frame = tk.Frame(self.root, bg=BG)
        score_frame.pack(fill="x", **pad, pady=(0, 10))

        # 3 cards en fila: Tú / Empate / IA
        self.card_x = self._crear_score_card(score_frame, "TÚ", "X", X_COLOR)
        self.card_x.pack(side="left", expand=True, fill="x", padx=(0, 4))

        card_e = self._crear_score_card(score_frame, "EMPATE", "—", NEUTRAL)
        card_e.pack(side="left", expand=True, fill="x", padx=4)

        self.card_o = self._crear_score_card(score_frame, "IA", "O", O_COLOR)
        self.card_o.pack(side="left", expand=True, fill="x", padx=(4, 0))

        # ── Etiqueta de estado ────────────────────────────────────────────────
        # Guardamos referencia en self para cambiarla dinámicamente con .config()
        self.lbl_status = tk.Label(self.root, text="Tu turno",
                                   font=self.fuente_status, bg=BG, fg=X_COLOR)
        self.lbl_status.pack(pady=(4, 8))

        # ── Canvas del tablero ────────────────────────────────────────────────
        # El Canvas es un área de dibujo donde colocamos líneas y texto con (x, y)
        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.pack(**pad, pady=(0, 10))

        self.canvas = tk.Canvas(board_frame, width=340, height=340,
                                bg=PANEL, highlightthickness=1,
                                highlightbackground=BORDER)
        self.canvas.pack()
        # Asociar clic izquierdo ("<Button-1>") al método _click_tablero
        self.canvas.bind("<Button-1>", self._click_tablero)
        self._dibujar_tablero()  # dibujar cuadrícula vacía al inicio

        # ── Botones de acción ─────────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill="x", **pad, pady=(0, 20))

        tk.Button(btn_frame, text="↺  NUEVA PARTIDA",
                  font=self.fuente_btn, bg=PANEL, fg=TEXT,
                  relief="flat", bd=0, padx=12, pady=10,
                  highlightthickness=1, highlightbackground=BORDER,
                  cursor="hand2", activebackground=BORDER,
                  command=self.nueva_partida
                  ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        tk.Button(btn_frame, text="⚡  RESET TOTAL",
                  font=self.fuente_btn, bg=PANEL, fg=TEXT,
                  relief="flat", bd=0, padx=12, pady=10,
                  highlightthickness=1, highlightbackground=BORDER,
                  cursor="hand2", activebackground=BORDER,
                  command=self.reset_total
                  ).pack(side="left", expand=True, fill="x", padx=(6, 0))

    def _crear_score_card(self, parent, label, simbolo, color):
        """
        Crea una card del marcador con etiqueta, símbolo y número de victorias.
        Guarda referencia al Label del número para poder actualizarlo después.
        Retorna el Frame para que el caller lo posicione con .pack().
        """
        frame = tk.Frame(parent, bg=PANEL, bd=0,
                         highlightthickness=1, highlightbackground=BORDER)
        tk.Label(frame, text=label, font=self.fuente_label,
                 bg=PANEL, fg=NEUTRAL).pack(pady=(8, 0))
        tk.Label(frame, text=simbolo,
                 font=tkfont.Font(family="Courier", size=18, weight="bold"),
                 bg=PANEL, fg=color).pack()
        # Label del número — guardamos referencia para actualizarlo
        score_lbl = tk.Label(frame, text="0", font=self.fuente_score, bg=PANEL, fg=TEXT)
        score_lbl.pack(pady=(0, 8))

        # Guardar referencia en self según qué card es
        if simbolo == "X":
            self.score_x_lbl = score_lbl
        elif simbolo == "O":
            self.score_o_lbl = score_lbl
        else:
            self.score_e_lbl = score_lbl

        return frame

    # ──────────────────────────────────────────────────────────────────────────
    #  TABLERO (CANVAS)
    # ──────────────────────────────────────────────────────────────────────────
    def _dibujar_tablero(self):
        """
        Borra el canvas y redibuja el tablero desde cero.
        Dibuja las 4 líneas de la cuadrícula y los símbolos actuales.
        Se llama al inicio y al resetear la partida.
        """
        c = self.canvas
        c.delete("all")  # borrar todo lo que hay en el canvas

        # Líneas de la cuadrícula — create_line(x1, y1, x2, y2)
        c.create_line(113, 28, 113, 312, fill=BORDER, width=2)  # vertical izquierda
        c.create_line(227, 28, 227, 312, fill=BORDER, width=2)  # vertical derecha
        c.create_line(28, 113, 312, 113, fill=BORDER, width=2)  # horizontal superior
        c.create_line(28, 227, 312, 227, fill=BORDER, width=2)  # horizontal inferior

        # Redibujar los símbolos que ya existen en el tablero
        for i, val in enumerate(self.tablero):
            if val:
                self._dibujar_simbolo(i, val)

    def _celda_a_coordenadas(self, index):
        """
        Convierte un índice de celda (0-8) al centro en píxeles (x, y) del canvas.

        El canvas mide 340x340. Cada celda mide ~114px.
        El centro de la primera celda está en (57, 57).

        Ejemplos:
            índice 0 → (col=0, fila=0) → centro (57,  57)
            índice 4 → (col=1, fila=1) → centro (171, 171)  ← centro del tablero
            índice 8 → (col=2, fila=2) → centro (285, 285)
        """
        fila = index // 3   # 0, 1 o 2
        col  = index % 3    # 0, 1 o 2
        x = 57 + col * 114  # centro horizontal de la celda
        y = 57 + fila * 114 # centro vertical de la celda
        return x, y

    def _dibujar_simbolo(self, index, simbolo, color=None):
        """
        Dibuja el símbolo (X u O) en el centro de la celda indicada.
        create_text() dibuja texto en el canvas en las coordenadas dadas.
        El tag permite identificar y borrar este texto individualmente si fuera necesario.
        """
        x, y = self._celda_a_coordenadas(index)
        col = color or (X_COLOR if simbolo == "X" else O_COLOR)
        self.canvas.create_text(x, y, text=simbolo, font=self.fuente_celda,
                                fill=col, tags=f"sym_{index}")

    def _click_tablero(self, event):
        """
        Se ejecuta cada vez que el jugador hace clic en el canvas.
        Calcula en qué celda hizo clic y realiza la jugada si es válido.

        event.x y event.y son las coordenadas del clic dentro del canvas.
        Dividiendo entre el tamaño de celda (~113px) obtenemos columna y fila.
        """
        # Ignorar si el juego terminó o no es el turno del humano
        if not self.juego_activo or not self.turno_humano:
            return

        # Calcular en qué celda (col, fila) cayó el clic
        col  = event.x // (340 // 3)
        fila = event.y // (340 // 3)

        # Ignorar clics fuera del área de juego
        if col > 2 or fila > 2:
            return

        # Convertir (fila, col) al índice lineal (0-8)
        index = fila * 3 + col

        # Ignorar si la celda ya está ocupada
        if self.tablero[index]:
            return

        self._realizar_jugada(index, "X")  # realizar la jugada del humano

    def _realizar_jugada(self, index, simbolo):
        """
        Registra la jugada en el tablero y la dibuja en el canvas.
        Verifica si hay ganador tras la jugada.
        Si jugó el humano (X), programa el turno de la IA con delay de 350ms.
        """
        self.tablero[index] = simbolo   # actualizar estado del tablero
        self._dibujar_simbolo(index, simbolo)  # dibujar en el canvas

        # Verificar si con esta jugada hay ganador o empate
        ganador, linea = verificar_ganador(self.tablero)
        if ganador:
            self._fin_juego(ganador, linea)
            return

        # Si jugó el humano, programar el turno de la IA
        if simbolo == "X":
            self.turno_humano = False
            self.lbl_status.config(text="IA pensando...", fg=O_COLOR)
            # after(ms, función) ejecuta la función después de N milisegundos
            # Da la sensación de que la IA "piensa" antes de responder
            self.root.after(350, self._turno_ia)

    def _turno_ia(self):
        """
        Ejecuta la jugada de la IA.
        Se llama automáticamente después del delay en _realizar_jugada().
        Obtiene el movimiento según dificultad y lo registra en el tablero.
        """
        if not self.juego_activo:
            return  # el usuario pudo resetear durante el delay

        movimiento = jugada_ia(self.tablero, self.dificultad.get())
        if movimiento != -1:
            self._realizar_jugada(movimiento, "O")

        # Si el juego no terminó, devolver el turno al humano
        if self.juego_activo:
            self.turno_humano = True
            self.lbl_status.config(text="Tu turno", fg=X_COLOR)

    def _fin_juego(self, ganador, linea):
        """
        Maneja el fin de la partida.
        Desactiva el tablero, actualiza el marcador, muestra el resultado
        y dibuja la línea ganadora si aplica.
        """
        self.juego_activo = False  # bloquear más clics en el tablero
        self.turno_humano = False

        if ganador == "empate":
            self.puntajes["empate"] += 1
            self.lbl_status.config(text="¡Empate!", fg=NEUTRAL)

        elif ganador == "X":
            self.puntajes["X"] += 1
            self.lbl_status.config(text="¡Ganaste! 🏆", fg=X_COLOR)
            self._dibujar_linea_ganadora(linea, X_COLOR)

        else:  # ganó la IA ("O")
            self.puntajes["O"] += 1
            # Mensaje distinto por dificultad para darle personalidad
            msgs = {
                "Fácil":   "¡Ganó la IA! (suerte de noob 😂)",
                "Normal":  "¡Ganó la IA! 🤖",
                "Difícil": "¡Imposible de ganar! 💀",
            }
            self.lbl_status.config(text=msgs[self.dificultad.get()], fg=O_COLOR)
            self._dibujar_linea_ganadora(linea, O_COLOR)

        self._actualizar_puntajes()

    def _dibujar_linea_ganadora(self, linea, color):
        """
        Dibuja una línea gruesa sobre las 3 celdas ganadoras.
        Toma el centro de la primera y última celda de la línea
        y traza una línea entre ellas.
        """
        if not linea:
            return
        x1, y1 = self._celda_a_coordenadas(linea[0])
        x2, y2 = self._celda_a_coordenadas(linea[2])
        # capstyle="round" hace los extremos de la línea redondeados
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5,
                                capstyle="round", tags="win_line")

    # ──────────────────────────────────────────────────────────────────────────
    #  MARCADOR
    # ──────────────────────────────────────────────────────────────────────────
    def _actualizar_puntajes(self):
        """
        Actualiza el texto de los Labels del marcador con los valores actuales.
        .config(text=...) modifica el contenido de un Label ya creado sin recrearlo.
        """
        self.score_x_lbl.config(text=str(self.puntajes["X"]))
        self.score_o_lbl.config(text=str(self.puntajes["O"]))
        self.score_e_lbl.config(text=str(self.puntajes["empate"]))

    # ──────────────────────────────────────────────────────────────────────────
    #  DIFICULTAD
    # ──────────────────────────────────────────────────────────────────────────
    def _cambiar_dificultad(self, diff):
        """
        Cambia la dificultad, actualiza el estilo de los botones
        y reinicia la partida actual (sin borrar el marcador).
        """
        self.dificultad.set(diff)        # actualizar la StringVar de Tkinter
        self._actualizar_botones_diff()  # resaltar el botón correcto
        self.nueva_partida()             # limpiar el tablero

    def _actualizar_botones_diff(self):
        """
        Aplica estilos visuales a los botones de dificultad:
        - Activo: color propio + fondo ligeramente más claro
        - Inactivos: color neutro + fondo normal del panel
        """
        actual = self.dificultad.get()
        for diff, btn in self.diff_buttons.items():
            if diff == actual:
                btn.config(fg=DIFF_COLORS[diff], bg="#111820", relief="flat")
            else:
                btn.config(fg=NEUTRAL, bg=PANEL, relief="flat")

    # ──────────────────────────────────────────────────────────────────────────
    #  RESET
    # ──────────────────────────────────────────────────────────────────────────
    def nueva_partida(self):
        """
        Reinicia solo el tablero actual. El marcador se mantiene.
        Resetea el estado del juego y redibuja el canvas vacío.
        """
        self.tablero      = [None] * 9
        self.juego_activo = True
        self.turno_humano = True
        self.lbl_status.config(text="Tu turno", fg=X_COLOR)
        self._dibujar_tablero()  # limpiar canvas y redibujar la cuadrícula

    def reset_total(self):
        """
        Resetea el marcador completo (victorias, derrotas, empates) y el tablero.
        """
        self.puntajes = {"X": 0, "empate": 0, "O": 0}
        self._actualizar_puntajes()
        self.nueva_partida()

    # ──────────────────────────────────────────────────────────────────────────
    #  UTILIDADES
    # ──────────────────────────────────────────────────────────────────────────
    def _centrar_ventana(self, ancho, alto):
        """
        Posiciona la ventana en el centro de la pantalla.
        winfo_screenwidth/height() retorna la resolución del monitor.
        geometry("AxB+X+Y") define tamaño (AxB) y posición (+X+Y) de la ventana.
        update_idletasks() fuerza a Tkinter a calcular los tamaños antes de continuar.
        """
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()    # ancho del monitor en píxeles
        sh = self.root.winfo_screenheight()   # alto del monitor en píxeles
        x  = (sw - ancho) // 2               # posición X centrada
        y  = (sh - alto)  // 2               # posición Y centrada
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")


# ══════════════════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA DEL PROGRAMA
#
#  if __name__ == "__main__" asegura que este bloque solo se ejecute
#  cuando corres el archivo directamente (no si lo importas como módulo).
#
#  Flujo de ejecución:
#    1. tk.Tk()       → crea la ventana principal vacía
#    2. Totito(root)  → construye toda la interfaz y el estado inicial del juego
#    3. mainloop()    → inicia el loop de eventos de Tkinter:
#                        → espera clicks, teclas, eventos del sistema
#                        → llama a las funciones correspondientes cuando ocurren
#                        → se queda corriendo hasta que el usuario cierra la ventana
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()       # crear ventana principal
    app  = Totito(root)  # inicializar el juego (construye UI + estado)
    root.mainloop()      # iniciar loop de eventos (mantiene la ventana abierta)