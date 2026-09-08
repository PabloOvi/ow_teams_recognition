import time
import keyboard
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract

# Configura la ruta de Tesseract si estás en Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def old():
    
   """  print("¡Capturando pantalla...")
    
    # Capturar pantalla
    screenshot = ImageGrab.grab()
    
    # Convertir imagen a formato OpenCV
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Procesamiento básico en grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gris, 200, 255, cv2.THRESH_BINARY)
    
    # OCR
    texto = pytesseract.image_to_string(thresh)
    nombres = [line.strip() for line in texto.split('\n') if line.strip()]
    
    print("Nombres detectados:", nombres) """

def old2():
    screenshot = ImageGrab.grab()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # 2. EJEMPLO DE RECORTE (ROI): Ajusta estos porcentajes según tu resolución y la pantalla de Overwatch
    #h, w, _ = frame.shape
    #frame_recortado = frame[int(h*0.2):int(h*0.8), int(w*0.1):int(w*0.9)]
    
    # Si de momento usas toda la pantalla, usa 'frame':
    frame_recortado = frame 

    # 3. Convertir a grises
    gris = cv2.cvtColor(frame_recortado, cv2.COLOR_BGR2GRAY)
    
    # 4. Aumentar tamaño x2 para mejorar la precisión del OCR en textos pequeños
    gris = cv2.resize(gris, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # 5. Binarización de Otsu (mucho más precisa que un umbral fijo)
    _, thresh = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 6. Configurar Tesseract con modo de bloque de texto y whitelist estricta (alfanumérico y #)
    config_ocr = r'--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#'
    
    texto = pytesseract.image_to_string(thresh, config=config_ocr)
    
    # Filtrar líneas vacías o muy cortas
    nombres = [line.strip() for line in texto.split('\n') if len(line.strip()) > 2]
    
    print("Nombres limpios detectados:", nombres)

def old3():
    screenshot = ImageGrab.grab()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # 2. Convertir a espacio de color HSV (permite aislar la luminosidad mejor que BGR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 3. Definir el rango del color blanco (Saturación baja, Brillo/Valor alto)
    # Puedes ajustar el 200 si el texto se ve un poco gris por el anti-aliasing
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 30, 255])
    
    # 4. Crear máscara: deja los píxeles blancos en blanco (255) y lo demás en negro (0)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # 5. Aumentar tamaño de la máscara para mejorar la precisión de Tesseract
    mask_resized = cv2.resize(mask, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # 6. OCR con lista blanca estricta
    config_ocr = r'--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#'
    texto = pytesseract.image_to_string(mask_resized, config=config_ocr)
    
    # Limpiar resultados
    nombres = [line.strip() for line in texto.split('\n') if len(line.strip()) > 2]
    print("Nombres blancos detectados:", nombres)

def procesar_mitad(imagen_recortada):
    # 1. Convertir a HSV para aislar el texto blanco
    hsv = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 30, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # 2. Escalar x2 para mejorar OCR
    mask_resized = cv2.resize(mask, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # 3. OCR con lista blanca estricta
    config_ocr = r'--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#'
    texto = pytesseract.image_to_string(mask_resized, config=config_ocr)
    
    # Limpiar líneas
    nombres = [line.strip() for line in texto.split('\n') if len(line.strip()) > 2]
    return nombres

def capturar_y_procesar():
    # 1. Capturar pantalla completa
    screenshot = ImageGrab.grab()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    h, w, _ = frame.shape
    
    # 2. Definir las mitades izquierda y derecha 
    # (El "VS" suele estar exactamente en el centro, así que partimos a la mitad horizontal)
    # [y_inicio:y_fin, x_inicio:x_fin]
    
    # Opcional: si la pantalla del VS muestra los nombres en una zona vertical específica (ej: del 30% al 70% de la altura)
    # puedes acotar también el eje Y para evitar los bordes superior e inferior.
    
    # Mitad Izquierda (Tu equipo)
    lado_izquierdo = frame[int(h*0.15):int(h*0.85), int(w*0.05):int(w*0.45)]
    
    # Mitad Derecha (Equipo enemigo)
    lado_derecho = frame[int(h*0.19):int(h*0.81), int(w*0.55):int(w*0.95)]
    
    # Procesar ambos lados por separado
    print("--- EQUIPO ALIADO ---")
    aliados = procesar_mitad(lado_izquierdo)
    print(aliados)
    
    print("--- EQUIPO ENEMIGO ---")
    enemigos = procesar_mitad(lado_derecho)
    print(enemigos)




print("Escuchando presiones de teclado. Presiona F9 para capturar. Presiona ESC para salir.")
keyboard.add_hotkey('f9', capturar_y_procesar)

keyboard.wait('esc')