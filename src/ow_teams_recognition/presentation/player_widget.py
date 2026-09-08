from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtWidgets import ( QFrame, QLabel, QHBoxLayout, QPushButton, )
from pathlib import Path
from PyQt6.QtGui import QIcon

from ..domain.enums import Performance
from ..domain.player import Player


class HoverLabel(QLabel):

	entered = pyqtSignal()
	left = pyqtSignal()


	def enterEvent(self, event):

		self.entered.emit()

		super().enterEvent( event )


	def leaveEvent(self, event):

		self.left.emit()

		super().leaveEvent( event )



class PlayerWidget(QFrame):

	character_clicked = pyqtSignal()
	performance_changed = pyqtSignal(Performance)

	name_hovered = pyqtSignal(str, str)
	name_unhovered = pyqtSignal()

	def __init__(self, player: Player):

		super().__init__()

		self.player = player

		self.performance_buttons = {}

		self._create_ui()
		self._update_ui()


	# =====================================================
	# UI
	# =====================================================

	def _create_ui(self):

		self.setObjectName("playerWidget")

		self.setStyleSheet("""
			QFrame#playerWidget {
				background-color: #151e27;
				border: 1px solid #2b3945;
				border-radius: 3px;
			}

			QFrame#playerWidget:hover {
				background-color: #1b2732;
				border: 1px solid #f99e1a;
			}
		""")

		layout = QHBoxLayout(self)

		layout.setContentsMargins(
			8,
			8,
			12,
			8
		)

		layout.setSpacing(12)


		# -------------------------------------------------
		# PERSONAJE
		# -------------------------------------------------

		self.character_button = QPushButton("+")
		self.character_button.setFixedSize(60, 60)

		self.character_button.setCursor( Qt.CursorShape.PointingHandCursor )

		self.character_button.clicked.connect( self.character_clicked.emit )

		self.character_button.setStyleSheet("""
			QPushButton {
				background-color: #202c36;
				border: 1px solid #3a4b59;
				border-radius: 3px;
				color: #71808c;
				font-size: 26px;
				font-weight: bold;
			}

			QPushButton:hover {
				background-color: #293844;
				border: 1px solid #f99e1a;
				color: #f99e1a;
			}
		""")

		layout.addWidget( self.character_button )


		# -------------------------------------------------
		# NOMBRE
		# -------------------------------------------------

		self.name_label = HoverLabel()

		self.name_label.setMinimumWidth(160)

		self.name_label.setStyleSheet("""
			QLabel {
				color: #f2f2f2;
				font-size: 15px;
				font-weight: bold;
				border: none;
			}
		""")

		layout.addWidget( self.name_label )

		self.name_label.entered.connect(
		lambda:
			self.name_hovered.emit(
				self.player.name,
				self.player.team.value
			)
	)

		self.name_label.left.connect( self.name_unhovered.emit )

		layout.addStretch()


		# -------------------------------------------------
		# PERFORMANCE
		# -------------------------------------------------

		self._create_performance_button(
			Performance.GOOD,
			"↑"
		)

		self._create_performance_button(
			Performance.NEUTRAL,
			"━"
		)

		self._create_performance_button(
			Performance.BAD,
			"↓"
		)


	# =====================================================
	# PERFORMANCE BUTTONS
	# =====================================================

	def _create_performance_button( self, performance: Performance, text: str ):

		button = QPushButton(text)

		button.setFixedSize(50, 50)
		button.setCheckable(True)

		button.setCursor( Qt.CursorShape.PointingHandCursor )

		button.clicked.connect(
			lambda checked, value=performance:
				self._select_performance(value)
		)

		self.performance_buttons[performance] = button

		self.layout().addWidget( button )


	# =====================================================
	# SELECT PERFORMANCE
	# =====================================================

	def _select_performance( self, performance: Performance ):

		self.player.performance = performance

		self._update_performance()

		self.performance_changed.emit( performance )


	# =====================================================
	# UPDATE PERFORMANCE
	# =====================================================

	def _update_performance(self):

		colors = {
			Performance.GOOD: (
				"#22c55e",
				"#4ade80"
			),

			Performance.NEUTRAL: (
				"#64748b",
				"#94a3b8"
			),

			Performance.BAD: (
				"#ef4444",
				"#f87171"
			),
		}

		for performance, button in ( self.performance_buttons.items() ):

			selected = ( performance == self.player.performance )
			background, border = colors[performance]

			button.setChecked(selected)

			if selected:

				button.setStyleSheet(f"""
					QPushButton {{
						background-color: {background};
						color: white;
						border: 1px solid {border};
						border-radius: 3px;
						font-size: 16px;
						font-weight: bold;
					}}
				""")

			else:

				button.setStyleSheet("""
					QPushButton {
						background-color: #202c36;
						color: #60717f;
						border: 1px solid #354653;
						border-radius: 3px;
						font-size: 16px;
					}

					QPushButton:hover {
						background-color: #2b3945;
						color: white;
						border: 1px solid #71808c;
					}
				""")


	# =====================================================
	# UPDATE UI
	# =====================================================

	def _update_ui(self):

		self.name_label.setText( self.player.name )

		self._update_character_icon()
		
		self._update_performance()

		# PGAish no tiene métricas

		if not self.player.has_performance:

			for button in ( self.performance_buttons.values() ):

				button.setEnabled(False)

				button.setStyleSheet("""
					QPushButton {
						background-color: #171e24;
						color: white;
						border: 1px solid #26313a;
						border-radius: 3px;
					}
				""")

	# =====================================================
	# CHARACTER ICON
	# =====================================================

	def _update_character_icon(self):

		if not self.player.character:

			self.character_button.setIcon( QIcon() )

			self.character_button.setText( "+" )
			self.character_button.setIconSize(QSize(52, 52))

			return


		character_filename = (
			self.player.character
			.lower()
			.replace(
				" ",
				"_"
			)
			.replace(
				".",
				""
			)
			.replace(
				":",
				""
			)
		)


		icon_path = ( Path(__file__).resolve().parent.parent.parent/"resources"/"icons"/f"{character_filename}.png")

		if not icon_path.exists():

			self.character_button.setIcon( QIcon() )

			self.character_button.setText( self.player.character )

			return


		self.character_button.setText("")

		self.character_button.setIcon( QIcon( str(icon_path) ) )

		self.character_button.setIconSize( QSize(52, 52) )
