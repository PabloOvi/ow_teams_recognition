import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import keyboard
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def old(crop):
    """
    Procesa UNA sola zona de nombre.
    """

    # Escala de grises
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Aumentar contraste
    gray = cv2.convertScaleAbs(
        gray,
        alpha=1.5,
        beta=-50
    )

    # Texto blanco -> blanco
    _, thresh = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY
    )

    # Agrandar
    thresh = cv2.resize(
        thresh,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # =====================================================
    # DEBUG
    # =====================================================

    #cv2.imwrite("debug_ocr.png", thresh)

    #cv2.imshow("Lo que ve Tesseract", thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # =====================================================
    # OCR
    # =====================================================

    config = (
        r'--oem 3 --psm 8 '
        r'-c tessedit_char_whitelist='
        r'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #r'abcdefghijklmnopqrstuvwxyz'
        r'0123456789'
    )

    texto = pytesseract.image_to_string(
        thresh,
        config=config
    )


    texto = texto.strip()

    texto = re.sub(
        r'[^A-Z0-9]',
        '',
        texto
    )

    return texto

def procesar_nombre(crop):

    # ==========================================
    # 1. Escala de grises
    # ==========================================

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )

    # ==========================================
    # 2. Threshold
    # ==========================================

    _, thresh = cv2.threshold(
        gray,
        120,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # ==========================================
    # 3. Agrandar
    # ==========================================

    thresh = cv2.resize(
        thresh,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # ==========================================
    # DEBUG
    # ==========================================

    cv2.imwrite(
        "debug_ocr.png",
        thresh
    )

    # ==========================================
    # 4. OCR
    # ==========================================

    config = (
        r'--oem 3 --psm 7 '
        r'-c tessedit_char_whitelist='
        r'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        r'abcdefghijklmnopqrstuvwxyz'
        r'0123456789'
    )

    texto = pytesseract.image_to_string(
        thresh,
        config=config
    )

    # ==========================================
    # 5. Limpiar
    # ==========================================

    texto = texto.strip()

    texto = re.sub(
        r'[^A-Za-z0-9]',
        '',
        texto
    )

    print(f"OCR detectado: '{texto}'")

    return texto

def capturar_y_procesar():

    screenshot = ImageGrab.grab()

    frame = cv2.cvtColor(
        np.array(screenshot),
        cv2.COLOR_RGB2BGR
    )

    h, w, _ = frame.shape

    print(f"Resolución: {w}x{h}")

    # =========================================================
    # COORDENADAS
    # =========================================================

    # Zona horizontal donde están los nombres
    #
    # izquierda:
    #   x = 210 -> 625
    #
    # derecha:
    #   x = 1120 -> 1535

    filas = [
        (300, 370),
        (410, 480),
        (520, 580),
        (625, 685),
        (715, 815)
    ]

    # =========================================================
    # EQUIPO 1
    # =========================================================

    aliados = []
    
    for y1, y2 in filas:

        crop = frame[
            y1:y2,
            210:625
        ]



        nombre = procesar_nombre(crop)

        if nombre:
            aliados.append(nombre)

    # =========================================================
    # EQUIPO 2
    # =========================================================

    filas = [
        (320, 380),
        (430, 480),
        (520, 580),
        (625, 685),
        (730, 790)
    ]

    enemigos = []



    # =========================================================
    # RESULTADO
    # =========================================================

    print()
    print("========== EQUIPO ALIADO ==========")

    for i, nombre in enumerate(aliados, 1):
        print(f"{i}. {nombre}")

    print()
    print("========== EQUIPO ENEMIGO ==========")

    for i, nombre in enumerate(enemigos, 1):
        print(f"{i}. {nombre}")

    print()


print(
    "Presiona F9 para capturar. "
    "Presiona ESC para salir."
)

keyboard.add_hotkey(
    "f9",
    capturar_y_procesar
)

keyboard.wait("esc")