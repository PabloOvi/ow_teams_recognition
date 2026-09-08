import sys
import keyboard
from PyQt6.QtWidgets import QApplication
from interface import MainWindow

# ========================================================= # MAIN # =========================================================

def main():

	app = QApplication( sys.argv )

	# ----------------------------------------------------- # ESTILO GENERAL # -----------------------------------------------------
	
	app.setStyleSheet(""" QWidget { background-color: #121212; color: white; font-family: Arial; } """)

	# ----------------------------------------------------- # VENTANA # -----------------------------------------------------

	window = MainWindow()
	window.show()

	# ----------------------------------------------------- # F9 # -----------------------------------------------------
	
	keyboard.add_hotkey( "f9", window.iniciar_ocr )
	print( "Presiona F9 para capturar." )
	print( "Cierra la ventana para salir." )
	sys.exit( app.exec() )

# ========================================================= # EJECUTAR # =========================================================

if __name__ == "__main__":

	main()