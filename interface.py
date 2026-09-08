from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import ( QLabel, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame )
from ocr import capturar_y_procesar

# ========================================================= # WORKER OCR # =========================================================
class OCRWorker(QThread):

	finished = pyqtSignal(list, list)
	error = pyqtSignal(str)

	def run(self):
		try: 
			aliados, enemigos = ( capturar_y_procesar() )
			self.finished.emit( aliados, enemigos )

		except Exception as e:
				self.error.emit( str(e) )

# ========================================================= # VENTANA PRINCIPAL # =========================================================
class MainWindow(QMainWindow):

	def __init__(self):

		super().__init__()
		self.setWindowTitle( "Overwatch Teams Recognition" )

		self.setMinimumSize( 800, 500 )
		self.worker = None
		self.labels_aliados = []
		self.labels_enemigos = []
		self.crear_interfaz()

# ===================================================== # CREAR INTERFAZ # =====================================================

	def crear_interfaz(self):

		central = QWidget()
		self.setCentralWidget( central )
		layout_principal = QVBoxLayout( central )
		layout_principal.setContentsMargins( 30, 25, 30, 25 )

		# ------------------------------------------------- # TÍTULO # -------------------------------------------------

		titulo = QLabel( "OVERWATCH TEAMS RECOGNITION" )
		titulo.setAlignment( Qt.AlignmentFlag.AlignCenter )
		titulo.setStyleSheet(""" QLabel { font-size: 24px; font-weight: bold; color: white; padding: 10px; } """)
		layout_principal.addWidget( titulo )

		# ------------------------------------------------- # EQUIPOS # -------------------------------------------------
		
		equipos_layout = QHBoxLayout()
		aliados = self.crear_panel_equipo( "EQUIPO ALIADO", "#3b82f6", self.labels_aliados )
		enemigos = self.crear_panel_equipo( "EQUIPO ENEMIGO", "#ef4444", self.labels_enemigos )
		equipos_layout.addWidget( aliados )
		equipos_layout.addWidget( enemigos )
		layout_principal.addLayout( equipos_layout ) 

		# ------------------------------------------------- # ESTADO # -------------------------------------------------
		
		self.label_estado = QLabel( "Estado: Esperando captura..." )
		self.label_estado.setAlignment( Qt.AlignmentFlag.AlignCenter )
		self.label_estado.setStyleSheet(""" QLabel { color: #aaaaaa; font-size: 14px; padding: 15px; } """)
		layout_principal.addWidget( self.label_estado )

		# ===================================================== # PANEL DE EQUIPO # =====================================================
		
	def crear_panel_equipo( self, titulo, color, lista_labels ):

		frame = QFrame()
		frame.setFrameShape( QFrame.Shape.StyledPanel )
		frame.setStyleSheet(""" QFrame { background-color: #202020; border: 1px solid #404040; border-radius: 8px; } """)
		layout = QVBoxLayout( frame )

		# ------------------------------------------------- # TÍTULO # -------------------------------------------------
		
		label_titulo = QLabel( titulo )
		label_titulo.setAlignment( Qt.AlignmentFlag.AlignCenter )
		label_titulo.setStyleSheet(f""" QLabel {{ color: {color}; font-size: 18px; font-weight: bold; border: none; padding: 10px; }} """)
		layout.addWidget( label_titulo )

		# ------------------------------------------------- # JUGADORES # -------------------------------------------------
		
		jugadores_layout = QGridLayout()
		for i in range(5):

			numero = QLabel( f"{i + 1}." )
			numero.setFixedWidth( 30 )
			numero.setStyleSheet(""" QLabel { color: #888888; font-size: 15px; border: none; } """)
			nombre = QLabel( "[NO DETECTADO]" )
			nombre.setMinimumHeight( 35 )
			nombre.setStyleSheet(""" QLabel { color: white; font-size: 15px; background-color: #151515; border: none; border-radius: 4px; padding: 8px; } """)
			jugadores_layout.addWidget( numero, i, 0 )
			jugadores_layout.addWidget( nombre, i, 1 )
			lista_labels.append( nombre )

		layout.addLayout( jugadores_layout )

		return frame

		# ===================================================== # INICIAR OCR # =====================================================
	def iniciar_ocr(self):

		if self.worker is not None:
			if self.worker.isRunning():
				self.label_estado.setText( "Estado: Ya hay una captura en proceso..." )

				return

		self.label_estado.setText( "Estado: Procesando OCR..." )
		self.worker = OCRWorker()
		self.worker.finished.connect( self.ocr_terminado )
		self.worker.error.connect( self.ocr_error )
		self.worker.start()

	# ===================================================== # OCR TERMINADO # =====================================================
	
	def ocr_terminado( self, aliados, enemigos ):

			for i, nombre in enumerate( aliados ):

				if nombre:

					self.labels_aliados[i].setText( nombre )

				else:

					self.labels_aliados[i].setText( "[NO DETECTADO]" )
			for i, nombre in enumerate( enemigos ):

				if nombre:

					self.labels_enemigos[i].setText( nombre )

				else:

					self.labels_enemigos[i].setText( "[NO DETECTADO]" )

			self.label_estado.setText( "Estado: Captura completada." )

	# ===================================================== # ERROR # =====================================================
	def ocr_error( self, mensaje ):

		self.label_estado.setText( f"Error: {mensaje}" )
		print()
		print("ERROR:")
		print(mensaje)