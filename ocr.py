import cv2
import numpy as np
import easyocr
from PIL import ImageGrab

# ========================================================= # CONFIGURACIÓN # ========================================================= #
# EasyOCR# 
# PyTorch está instalado sin CUDA, por eso usamos CPU. 
reader = easyocr.Reader( ['en'], gpu=False, verbose=False ) 
# ========================================================= # COORDENADAS # ========================================================= 

FILAS_ALIADOS = [ (300, 370), (410, 480), (520, 580), (625, 685), (740, 790) ]
FILAS_ENEMIGOS = [ (320, 380), (430, 480), (520, 580), (625, 685), (730, 790) ]
X_IZQ_1 = 210
X_IZQ_2 = 625
X_DER_1 = 1300
X_DER_2 = 1600
# ========================================================= # EASY OCR # =========================================================
def ejecutar_easyocr(imagen):
	results = reader.readtext(imagen)
	extracted_text = "\n".join( text for (bbox, text, prob) in results )
	return extracted_text

# ========================================================= # PROCESAR NOMBRE # =========================================================
def procesar_nombre(crop):
	text = ejecutar_easyocr(crop)
	print(f"OCR: '{text}'")
	return text
# ========================================================= # PROCESAR EQUIPO # =========================================================
def procesar_equipo( frame, filas, x1, x2, nombre_equipo ):
	jugadores = []
	print()
	print(f"========== {nombre_equipo} ==========")
	for numero, (y1, y2) in enumerate( filas, 1 ):
		crop = frame[ y1:y2, x1:x2 ]
		print()
		print(f"Jugador #{numero}")
		nombre = procesar_nombre( crop )
		if nombre:
			jugadores.append( nombre )
		else:
			print( " -> NO DETECTADO" )
			jugadores.append("")

	return jugadores

# ========================================================= # CAPTURAR PANTALLA # =========================================================
def capturar_pantalla():
	screenshot = ImageGrab.grab()
	frame = cv2.cvtColor( np.array(screenshot), cv2.COLOR_RGB2BGR )
	return frame

# ========================================================= # PROCESAR CAPTURA COMPLETA # =========================================================
def capturar_y_procesar():
	frame = capturar_pantalla()
	h, w, _ = frame.shape
	print()
	print("========================================")
	print(f"Resolución: {w}x{h}")
	print("========================================")
	# ----------------------------------------------------- # EQUIPO ALIADO # -----------------------------------------------------
	
	aliados = procesar_equipo( frame, FILAS_ALIADOS, X_IZQ_1, X_IZQ_2, "EQUIPO ALIADO" )

	# ----------------------------------------------------- # EQUIPO ENEMIGO # -----------------------------------------------------
	enemigos = procesar_equipo( frame, FILAS_ENEMIGOS, X_DER_1, X_DER_2, "EQUIPO ENEMIGO" )

	return aliados, enemigos