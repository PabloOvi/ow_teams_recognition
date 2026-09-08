
import sys
import keyboard

from PyQt6.QtWidgets import QApplication

from .application.recognition_service import ( RecognitionService )
from .application.match_service import MatchService

from .infrastructure.ocr.easyocr_reader import ( EasyOCRReader )

from .infrastructure.ocr.screen_capture import ( ScreenCapture )

from .data.database import ( Database )

from .data.repositories.match_repository import ( MatchRepository )

from .presentation.main_window import ( MainWindow )



def main():

	app = QApplication(sys.argv)

	app.setStyleSheet("""
		QWidget {
			background-color: #121212;
			color: white;
			font-family: Arial;
		}
	""")


	# =====================================================
	# INFRASTRUCTURE
	# =====================================================

	screen_capture = ScreenCapture()

	ocr_reader = EasyOCRReader()


	# =====================================================
	# DATABASE
	# =====================================================

	database = Database()

	match_repository = MatchRepository( database )


	# =====================================================
	# APPLICATION
	# =====================================================

	match_service = MatchService( match_repository )

	recognition_service = RecognitionService(
		screen_capture=screen_capture,
		ocr_reader=ocr_reader
	)


	# =====================================================
	# PRESENTATION
	# =====================================================

	window = MainWindow(
		recognition_service=recognition_service,
		match_service=match_service
	)

	window.show()


	# =====================================================
	# GLOBAL HOTKEYS
	# =====================================================

	keyboard.add_hotkey(
		"f9",
		window.f9_pressed.emit
	)


	sys.exit( app.exec() )


if __name__ == "__main__":

	main()

