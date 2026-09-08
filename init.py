import sys
import cv2
import numpy as np
import easyocr
import keyboard

from PIL import ImageGrab

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame
)


# =========================================================
# CONFIGURACIÓN
# =========================================================

# EasyOCR
# Como PyTorch no tiene CUDA disponible, usamos CPU.
reader = easyocr.Reader(
    ['en'],
    gpu=False,
    verbose=False
)


# Filas del equipo aliado
FILAS_ALIADOS = [
    (300, 370),
    (410, 480),
    (520, 580),
    (625, 685),
    (740, 790)
]

# Filas del equipo enemigo
FILAS_ENEMIGOS = [
    (320, 380),
    (430, 480),
    (520, 580),
    (625, 685),
    (730, 790)
]


# Coordenadas horizontales
X_IZQ_1 = 210
X_IZQ_2 = 625

X_DER_1 = 1300
X_DER_2 = 1600


# =========================================================
# OCR
# =========================================================

def ejecutar_easyocr(imagen):

    results = reader.readtext(imagen)

    extracted_text = "\n".join(
        text for (bbox, text, prob) in results
    )

    return extracted_text


# =========================================================
# PROCESAR NOMBRE
# =========================================================

def procesar_nombre(crop):

    text = ejecutar_easyocr(crop)

    print(f"OCR: '{text}'")

    return text


# =========================================================
# PROCESAR EQUIPO
# =========================================================

def procesar_equipo(frame, filas, x1, x2, nombre_equipo):

    jugadores = []

    print()
    print(f"========== {nombre_equipo} ==========")

    for numero, (y1, y2) in enumerate(filas, 1):

        crop = frame[
            y1:y2,
            x1:x2
        ]

        print()
        print(f"Jugador #{numero}")

        nombre = procesar_nombre(crop)

        if nombre:

            jugadores.append(nombre)

        else:

            print("   -> NO DETECTADO")

            jugadores.append("")

    return jugadores


# =========================================================
# CAPTURAR Y PROCESAR
# =========================================================

def capturar_y_procesar():

    screenshot = ImageGrab.grab()

    frame = cv2.cvtColor(
        np.array(screenshot),
        cv2.COLOR_RGB2BGR
    )

    h, w, _ = frame.shape

    print()
    print("========================================")
    print(f"Resolución: {w}x{h}")
    print("========================================")

    # -----------------------------------------------------
    # EQUIPO ALIADO
    # -----------------------------------------------------

    aliados = procesar_equipo(
        frame,
        FILAS_ALIADOS,
        X_IZQ_1,
        X_IZQ_2,
        "EQUIPO ALIADO"
    )

    # -----------------------------------------------------
    # EQUIPO ENEMIGO
    # -----------------------------------------------------

    enemigos = procesar_equipo(
        frame,
        FILAS_ENEMIGOS,
        X_DER_1,
        X_DER_2,
        "EQUIPO ENEMIGO"
    )

    return aliados, enemigos


# =========================================================
# WORKER
# =========================================================

class OCRWorker(QThread):

    finished = pyqtSignal(list, list)
    error = pyqtSignal(str)

    def run(self):

        try:

            aliados, enemigos = capturar_y_procesar()

            self.finished.emit(
                aliados,
                enemigos
            )

        except Exception as e:

            self.error.emit(str(e))


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Overwatch Teams Recognition"
        )

        self.setMinimumSize(
            800,
            500
        )

        self.worker = None

        self.labels_aliados = []
        self.labels_enemigos = []

        self.crear_interfaz()


    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout_principal = QVBoxLayout(
            central
        )

        layout_principal.setContentsMargins(
            30,
            25,
            30,
            25
        )

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        titulo = QLabel(
            "OVERWATCH TEAMS RECOGNITION"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 10px;
            }
        """)

        layout_principal.addWidget(
            titulo
        )

        # -------------------------------------------------
        # CONTENEDOR DE EQUIPOS
        # -------------------------------------------------

        equipos_layout = QHBoxLayout()

        # =================================================
        # ALIADOS
        # =================================================

        frame_aliados = self.crear_panel_equipo(
            "EQUIPO ALIADO",
            "#3b82f6"
        )

        equipos_layout.addWidget(
            frame_aliados
        )

        # =================================================
        # ENEMIGOS
        # =================================================

        frame_enemigos = self.crear_panel_equipo(
            "EQUIPO ENEMIGO",
            "#ef4444"
        )

        equipos_layout.addWidget(
            frame_enemigos
        )

        layout_principal.addLayout(
            equipos_layout
        )

        # -------------------------------------------------
        # ESTADO
        # -------------------------------------------------

        self.label_estado = QLabel(
            "Estado: Esperando captura..."
        )

        self.label_estado.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.label_estado.setStyleSheet("""
            QLabel {
                color: #aaaaaa;
                font-size: 14px;
                padding: 15px;
            }
        """)

        layout_principal.addWidget(
            self.label_estado
        )


    # =====================================================
    # CREAR PANEL DE EQUIPO
    # =====================================================

    def crear_panel_equipo(
        self,
        titulo,
        color
    ):

        frame = QFrame()

        frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        frame.setStyleSheet("""
            QFrame {
                background-color: #202020;
                border: 1px solid #404040;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(
            frame
        )

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        label_titulo = QLabel(
            titulo
        )

        label_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label_titulo.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: bold;
                border: none;
                padding: 10px;
            }}
        """)

        layout.addWidget(
            label_titulo
        )

        # -------------------------------------------------
        # JUGADORES
        # -------------------------------------------------

        jugadores_layout = QGridLayout()

        for i in range(5):

            numero = QLabel(
                f"{i + 1}."
            )

            numero.setFixedWidth(
                30
            )

            numero.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 15px;
                    border: none;
                }
            """)

            nombre = QLabel(
                "[NO DETECTADO]"
            )

            nombre.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 15px;
                    background-color: #151515;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                }
            """)

            nombre.setMinimumHeight(
                35
            )

            jugadores_layout.addWidget(
                numero,
                i,
                0
            )

            jugadores_layout.addWidget(
                nombre,
                i,
                1
            )

            if titulo == "EQUIPO ALIADO":

                self.labels_aliados.append(
                    nombre
                )

            else:

                self.labels_enemigos.append(
                    nombre
                )

        layout.addLayout(
            jugadores_layout
        )

        return frame


    # =====================================================
    # INICIAR OCR
    # =====================================================

    def iniciar_ocr(self):

        # Evitamos lanzar otro OCR
        # mientras uno ya está funcionando.

        if self.worker is not None:

            if self.worker.isRunning():

                self.label_estado.setText(
                    "Estado: Ya hay una captura en proceso..."
                )

                return

        self.label_estado.setText(
            "Estado: Procesando OCR..."
        )

        self.worker = OCRWorker()

        self.worker.finished.connect(
            self.ocr_terminado
        )

        self.worker.error.connect(
            self.ocr_error
        )

        self.worker.start()


    # =====================================================
    # OCR TERMINADO
    # =====================================================

    def ocr_terminado(
        self,
        aliados,
        enemigos
    ):

        # -------------------------------------------------
        # ALIADOS
        # -------------------------------------------------

        for i, nombre in enumerate(
            aliados
        ):

            if nombre:

                self.labels_aliados[i].setText(
                    nombre
                )

            else:

                self.labels_aliados[i].setText(
                    "[NO DETECTADO]"
                )

        # -------------------------------------------------
        # ENEMIGOS
        # -------------------------------------------------

        for i, nombre in enumerate(
            enemigos
        ):

            if nombre:

                self.labels_enemigos[i].setText(
                    nombre
                )

            else:

                self.labels_enemigos[i].setText(
                    "[NO DETECTADO]"
                )

        # -------------------------------------------------
        # ESTADO
        # -------------------------------------------------

        self.label_estado.setText(
            "Estado: Captura completada."
        )


    # =====================================================
    # ERROR
    # =====================================================

    def ocr_error(
        self,
        mensaje
    ):

        self.label_estado.setText(
            f"Error: {mensaje}"
        )

        print()
        print("ERROR:")
        print(mensaje)


# =========================================================
# MAIN
# =========================================================

def main():

    app = QApplication(
        sys.argv
    )

    # -----------------------------------------------------
    # ESTILO GENERAL
    # -----------------------------------------------------

    app.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: white;
            font-family: Arial;
        }
    """)

    window = MainWindow()

    window.show()

    # -----------------------------------------------------
    # F9
    # -----------------------------------------------------

    keyboard.add_hotkey(
        "f9",
        window.iniciar_ocr
    )

    print(
        "Presiona F9 para capturar."
    )

    print(
        "Cierra la ventana para salir."
    )

    sys.exit(
        app.exec()
    )


# =========================================================
# EJECUTAR
# =========================================================

if __name__ == "__main__":

    main()
