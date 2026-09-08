import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import keyboard
import re
import easyocr

pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'
)
#Este test si funciona, nomas agrege el easyorc para testear.

# =========================================================
# OCR
# =========================================================

def ejecutar_easyorc(imagen):
    # Initialize the reader and specify the language(s) you need (e.g., 'en' for English)
    reader = easyocr.Reader(['en'])
    # Read the text from the image
    results = reader.readtext(imagen)
    
    # EasyOCR returns a list of tuples containing bounding boxes, text, and confidence scores.
    # We will extract just the text fragments and join them.
    extracted_text = "\n".join([text for (bbox, text, prob) in results])
    
    return extracted_text

def ejecutar_ocr(imagen):

    config = (
        r'--oem 3 --psm 7 '
        r'-c tessedit_char_whitelist='
        r'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #r'abcdefghijklmnopqrstuvwxyz'
        r'0123456789'
    )

    texto = pytesseract.image_to_string(
        imagen,
        config=config
    )

    texto = texto.strip()

    # Solo permitimos letras y números
    texto = re.sub(
        r'[^A-Za-z0-9]',
        '',
        texto
    )

    return texto


# =========================================================
# PROCESAR UNA ZONA DE NOMBRE
# =========================================================

def procesar_nombre(crop):

    # -----------------------------------------------------
    # 1. Escala de grises
    # -----------------------------------------------------

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )

    # -----------------------------------------------------
    # 2. PRIMER INTENTO - OTSU
    # -----------------------------------------------------

    _, thresh = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # -----------------------------------------------------
    # 3. Escalar x3
    # -----------------------------------------------------

    thresh = cv2.resize(
        thresh,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # -----------------------------------------------------
    # DEBUG
    # -----------------------------------------------------

    cv2.imwrite(
        "debug_ocr.png",
        thresh
    )

    # -----------------------------------------------------
    # 4. OCR
    # -----------------------------------------------------

    texto = ejecutar_easyorc(crop)

    print(
        f"OCR intento 1: '{texto}'"
    )

    # -----------------------------------------------------
    # 5. SEGUNDO INTENTO
    # Si no detectó nada
    # -----------------------------------------------------

    if not texto:

        print(
            "   -> Sin resultado. "
            "Probando segundo método..."
        )

        _, thresh2 = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY
        )

        thresh2 = cv2.resize(
            thresh2,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        cv2.imwrite(
            "debug_ocr_2.png",
            thresh2
        )

        texto = ejecutar_ocr(thresh2)

        print(
            f"OCR intento 2: '{texto}'"
        )

    return texto


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
			(715, 815)
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