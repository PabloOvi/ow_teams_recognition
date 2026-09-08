from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
	QDialog,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QListWidget,
	QListWidgetItem,
	QPushButton,
	QVBoxLayout,
)


class CharacterSelectorDialog(QDialog):

	character_selected = pyqtSignal(str)

	def __init__( self, characters: list[str], parent=None ):

		super().__init__(parent)

		self.characters = characters

		self.characters_path = Path(
			Path(__file__).resolve().parent.parent.parent/"resources"/"icons"
		)

		self.setWindowTitle( "Seleccionar personaje" )

		self.setFixedSize(
			560,
			620
		)

		self._create_ui()

		self._load_characters()


	# =====================================================
	# UI
	# =====================================================

	def _create_ui(self):

		self.setStyleSheet("""
			QDialog {
				background-color: #0b1117;
			}

			QLabel {
				color: #e8edf2;
			}

			QLineEdit {
				background-color: #151e27;
				color: white;
				border: 1px solid #334452;
				border-radius: 3px;
				padding: 10px;
				font-size: 13px;
			}

			QLineEdit:focus {
				border: 1px solid #f99e1a;
			}

			QListWidget {
				background-color: #101820;
				border: 1px solid #293946;
				outline: none;
			}

			QListWidget::item {
				background-color: #151e27;
				border: 1px solid #293946;
				margin: 5px;
				padding: 5px;
			}

			QListWidget::item:hover {
				background-color: #202d38;
				border: 1px solid #f99e1a;
			}

			QListWidget::item:selected {
				background-color: #2a241b;
				border: 2px solid #f99e1a;
			}
		""")

		layout = QVBoxLayout(self)

		layout.setContentsMargins(
			20,
			20,
			20,
			20
		)
		layout.setSpacing(12)


		# -------------------------------------------------
		# TITLE
		# -------------------------------------------------

		title = QLabel( "Seleccionar personaje" )

		title.setStyleSheet("""
			QLabel {
				color: #f2f2f2;
				font-size: 24px;
				font-weight: bold;
				padding-bottom: 2px;
			}
		""")


		layout.addWidget( title )

		subtitle = QLabel(
			"Selecciona el héroe utilizado en esta partida"
		)

		subtitle.setStyleSheet("""
			QLabel {
				color: #71808c;
				font-size: 11px;
				border: none;
			}
		""")

		layout.addWidget(subtitle)


		# -------------------------------------------------
		# SEARCH
		# -------------------------------------------------

		self.search_input = QLineEdit()

		self.search_input.setPlaceholderText( "Buscar personaje..." )

		self.search_input.textChanged.connect( self._filter_characters )

		layout.addWidget( self.search_input )


		# -------------------------------------------------
		# LIST
		# -------------------------------------------------

		self.character_list = QListWidget()

		self.character_list.setIconSize( QSize(76,76) )

		self.character_list.setViewMode( QListWidget.ViewMode.IconMode )

		self.character_list.setGridSize( QSize(100, 105) )

		self.character_list.setResizeMode( QListWidget.ResizeMode.Adjust )

		self.character_list.setMovement( QListWidget.Movement.Static )

		self.character_list.setSpacing( 4 )

		self.character_list.itemDoubleClicked.connect( self._select_character )

		layout.addWidget( self.character_list )


		# -------------------------------------------------
		# BUTTONS
		# -------------------------------------------------

		buttons_layout = QHBoxLayout()

		buttons_layout.addStretch()


		cancel_button = QPushButton( "Cancelar" )

		cancel_button.clicked.connect( self.reject )


		select_button = QPushButton( "Seleccionar" )

		select_button.setFixedHeight(38)

		select_button.setCursor( Qt.CursorShape.PointingHandCursor )

		select_button.setStyleSheet("""
			QPushButton {
				background-color: #f99e1a;
				color: #101010;
				border: none;
				border-radius: 3px;
				padding: 0 22px;
				font-weight: bold;
			}

			QPushButton:hover {
				background-color: #ffb347;
			}

			QPushButton:pressed {
				background-color: #d98208;
			}
		""")

		select_button.clicked.connect( self._select_character )


		buttons_layout.addWidget( cancel_button )

		buttons_layout.addWidget( select_button )

		layout.addLayout( buttons_layout )


	# =====================================================
	# LOAD CHARACTERS
	# =====================================================

	def _load_characters(self):

		self.character_list.clear()

		for character in self.characters:

			self._add_character( character )


	# =====================================================
	# ADD CHARACTER
	# =====================================================

	def _add_character( self, character: str ):

		item = QListWidgetItem()

		character_filename = ( character.lower().replace(" ","_").replace(".","").replace(":","") )

		image_path = ( self.characters_path / f"{character_filename}.png" )

		if image_path.exists():

			item.setIcon( QIcon( str(image_path) ) )

		else:

			# Imagen vacía si no existe
			item.setText( "?" )
			print( character_filename )


		# Guardamos el nombre real del personaje aunque no sea visible.

		item.setData( Qt.ItemDataRole.UserRole, character )

		self.character_list.addItem( item )


	# =====================================================
	# FILTER
	# =====================================================

	def _filter_characters( self, text: str ):

		search = text.lower().strip()

		self.character_list.clear()

		for character in self.characters:

			if search in character.lower():

				self._add_character( character )


	# =====================================================
	# SELECT
	# =====================================================

	def _select_character(self):

		item = self.character_list.currentItem()

		if item is None:

			return

		character = item.data( Qt.ItemDataRole.UserRole )

		self.character_selected.emit( character )

		self.accept()

