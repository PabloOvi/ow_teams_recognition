import cv2
import numpy as np
from PIL import ImageGrab
import keyboard
import easyocr

# Inicializo el easyorc, dejando por defecto el idioma en ingles, como tengo la version de pytoch sin gpu desactivo el uso, para evitar problemas.

reader = easyocr.Reader(['en'], gpu=False,verbose=False)

# =========================================================
# OCR
# =========================================================

def execute_easyorc(imagen):

    # Leo la imagen.

    results = reader.readtext(imagen)

    # EasyOCR devuelve una lista de tuplas con contenedores de texto.
    # Extraigo lo que puedo de ellas y las uno para formar el texto bien completo (util dado que la tipografia de OW puede generar problemas).
    extracted_text = "\n".join([text for (bbox, text, prob) in results])

    return extracted_text


# =========================================================
# PROCESAR UNA ZONA DE NOMBRE
# =========================================================

def procesar_nombre(crop):

    # -----------------------------------------------------
    # DEBUG
    # -----------------------------------------------------

    #cv2.imwrite(
    #    "debug_ocr.png",
    #    crop
    #)

    # -----------------------------------------------------
    # 4. OCR
    # -----------------------------------------------------

    text = execute_easyorc(crop)

    print(
        f"OCR intento 1: '{text}'"
    )

    return text


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


    # =====================================================
    # FILAS
    # =====================================================
    #
    # IMPORTANTE:
    # Acá dejá los valores que vos ajustaste.
    #

    filas = [
			(300, 370),
			(410, 480),
			(520, 580),
			(625, 685),
			(740, 790)
		]


    # =====================================================
    # COORDENADAS HORIZONTALES
    # =====================================================

    X_IZQ_1 = 210
    X_IZQ_2 = 625

    X_DER_1 = 1300
    X_DER_2 = 1600


    # =====================================================
    # EQUIPO ALIADO
    # =====================================================

    aliados = []

    print()
    print("========== EQUIPO ALIADO ==========")

    for numero, (y1, y2) in enumerate(filas, 1):

        crop = frame[
            y1:y2,
            X_IZQ_1:X_IZQ_2
        ]

        print()
        print(f"Jugador aliado #{numero}")

        nombre = procesar_nombre(crop)

        if nombre:

            aliados.append(nombre)

        else:

            print("   -> NO DETECTADO")

            aliados.append("")


    # =====================================================
    # EQUIPO ENEMIGO
    # =====================================================

    enemigos = []

    filas = [
			(320, 380),
			(430, 480),
			(520, 580),
			(625, 685),
			(730, 790)
		]

    print()
    print("========== EQUIPO ENEMIGO ==========")

    for numero, (y1, y2) in enumerate(filas, 1):

        crop = frame[
            y1:y2,
            X_DER_1:X_DER_2
        ]

        print()
        print(f"Jugador enemigo #{numero}")

        nombre = procesar_nombre(crop)

        if nombre:

            enemigos.append(nombre)

        else:

            print("   -> NO DETECTADO")

            enemigos.append("")


    # =====================================================
    # RESULTADO
    # =====================================================

    print()
    print("========================================")
    print("             RESULTADO")
    print("========================================")

    print()
    print("========== EQUIPO ALIADO ==========")

    for i, nombre in enumerate(aliados, 1):

        if nombre:
            print(f"{i}. {nombre}")
        else:
            print(f"{i}. [NO DETECTADO]")


    print()
    print("========== EQUIPO ENEMIGO ==========")

    for i, nombre in enumerate(enemigos, 1):

        if nombre:
            print(f"{i}. {nombre}")
        else:
            print(f"{i}. [NO DETECTADO]")


    print()


# =========================================================
# HOTKEYS
# =========================================================

print(
    "Presiona F9 para capturar. "
    "Presiona ESC para salir."
)

keyboard.add_hotkey(
    "f9",
    capturar_y_procesar
)

keyboard.wait("esc")