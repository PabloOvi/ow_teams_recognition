from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtWidgets import ( QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QToolTip, )
from PyQt6.QtGui import QCursor

from .workers.recognition_worker import( RecognitionWorker )
from ..application.recognition_service import RecognitionService
from ..application.match_service import MatchService
from ..domain.enums import Team, MatchResult
from ..domain.match import Match
from ..domain.characters import CHARACTERS
from .character_selector_dialog import CharacterSelectorDialog
from .player_widget import PlayerWidget


class MainWindow(QMainWindow):

	f9_pressed = pyqtSignal()


	def __init__( self, recognition_service: RecognitionService, match_service: MatchService ):

		super().__init__()

		self.recognition_service = ( recognition_service )

		self.match_service = match_service

		self.player_widgets = []

		self.current_match = None

		self.recognition_thread = None
		self.recognition_worker = None

		self.setWindowTitle( "Overwatch Teams Recognition" )

		self.resize(
			1100,
			700
		)

		self.f9_pressed.connect( self.capture_match 	)

		self._create_ui()



	# =====================================================
	# UI
	# =====================================================

	def _create_ui(self):

		central_widget = QWidget()

		self.setCentralWidget( central_widget )

		main_layout = QVBoxLayout( central_widget )

		main_layout.setContentsMargins(
			25,
			25,
			25,
			25
		)


		# -------------------------------------------------
		# TITLE
		# -------------------------------------------------

		title = QLabel( "OVERWATCH TEAMS RECOGNITION" )

		title.setAlignment( Qt.AlignmentFlag.AlignCenter )

		title.setStyleSheet("""
			QLabel {
				color: white;
				font-size: 24px;
				font-weight: bold;
			}
		""")

		main_layout.addWidget( title )

		# -------------------------------------------------
		# TEAMS
		# -------------------------------------------------

		teams_layout = QHBoxLayout()

		# Allied

		self.allied_frame = self._create_team_frame( "EQUIPO ALIADO" )

		teams_layout.addWidget( self.allied_frame )

		# Enemy

		self.enemy_frame = self._create_team_frame( "EQUIPO ENEMIGO" )

		teams_layout.addWidget( self.enemy_frame )

		main_layout.addLayout( teams_layout )


		# -------------------------------------------------
		# MATCH RESULT
		# -------------------------------------------------

		result_label = QLabel( "RESULTADO DE PARTIDA" )

		result_label.setAlignment( Qt.AlignmentFlag.AlignCenter )

		result_label.setStyleSheet("""
			QLabel {
				color: white;
				font-size: 16px;
				font-weight: bold;
				padding: 10px;
			}
		""")

		main_layout.addWidget( result_label )


		result_layout = QHBoxLayout()

		result_layout.addStretch()


		self.victory_button = QPushButton( "VICTORIA" )

		self.victory_button.setCheckable( True )

		self.victory_button.clicked.connect( self._set_victory )


		self.defeat_button = QPushButton( "DERROTA" )

		self.defeat_button.setCheckable( True )

		self.defeat_button.clicked.connect( self._set_defeat )


		result_layout.addWidget( self.victory_button )

		result_layout.addWidget( self.defeat_button )

		result_layout.addStretch()


		main_layout.addLayout( result_layout )

		# -------------------------------------------------
		# SAVE
		# -------------------------------------------------

		self.save_button = QPushButton( "GUARDAR PARTIDA" )

		self.save_button.setEnabled( False )

		self.save_button.clicked.connect( self._save_match )

		main_layout.addWidget( self.save_button )


		# -------------------------------------------------
		# STATUS
		# -------------------------------------------------

		self.status_label = QLabel( "Estado: Esperando captura..." )

		self.status_label.setAlignment( Qt.AlignmentFlag.AlignCenter )

		self.status_label.setStyleSheet("""
			QLabel {
				color: #888888;
				padding: 15px;
			}
		""")

		main_layout.addWidget( self.status_label )


	# =====================================================
	# TEAM FRAME
	# =====================================================

	def _create_team_frame( self, title: str ) -> QFrame:

		frame = QFrame()

		frame.setStyleSheet("""
			QFrame {
				background-color: #202020;
				border: 1px solid #383838;
				border-radius: 8px;
			}
		""")

		layout = QVBoxLayout( frame )

		team_title = QLabel(title)

		team_title.setAlignment( Qt.AlignmentFlag.AlignCenter )

		team_title.setStyleSheet("""
			QLabel {
				color: white;
				font-size: 18px;
				font-weight: bold;
				border: none;
				padding: 10px;
			}
		""")

		layout.addWidget( team_title )

		return frame


	# =====================================================
	# CAPTURE
	# =====================================================


	def capture_match(self):

		if self.recognition_thread is not None:

			if self.recognition_thread.isRunning():

				return

		self.status_label.setText( "Estado: Procesando OCR..." )
		self.recognition_thread = QThread()
		self.recognition_worker = ( RecognitionWorker( self.recognition_service ) )
		self.recognition_worker.moveToThread( self.recognition_thread )
		self.recognition_thread.started.connect( self.recognition_worker.run )
		self.recognition_worker.finished.connect( self._on_recognition_finished )
		self.recognition_worker.error.connect( self._on_recognition_error )
		self.recognition_worker.finished.connect( self._finish_recognition )
		self.recognition_worker.error.connect( self._finish_recognition )
		self.recognition_thread.start()


	# =====================================================
	# LOAD MATCH
	# =====================================================

	
	def load_match(	self, match: Match ):

		self.current_match = match

		self._clear_players()

		for player in match.players:

			widget = PlayerWidget(
				player
			)

			widget.character_clicked.connect(
				lambda player=player:
					self._select_character(player)
			)

			widget.name_hovered.connect( self._show_player_history )

			widget.name_unhovered.connect( self._hide_player_history )

			self.player_widgets.append(
				widget
			)

			if player.team == Team.ALLIED:

				self.allied_frame.layout().addWidget(
					widget
				)

			else:

				self.enemy_frame.layout().addWidget(
					widget
				)



	# =====================================================
	# CLEAR PLAYERS
	# =====================================================

	def _clear_players(self):

		for widget in self.player_widgets:

			widget.deleteLater()

		self.player_widgets.clear()

	# =====================================================
	# CHARACTER SELECTION
	# =====================================================

	def _select_character( self, player ):

		dialog = CharacterSelectorDialog( CHARACTERS, self )

		def on_character_selected( character: str ):

			player.character = character

			for widget in self.player_widgets:

				if widget.player is player:

					widget._update_ui()

					break


		dialog.character_selected.connect( on_character_selected )

		dialog.exec()

	# =====================================================
	# MATCH RESULT
	# =====================================================

	def _set_victory(self):

		if self.current_match is None:

			return

		self.current_match.result = ( MatchResult.VICTORY )

		self.victory_button.setChecked( True )

		self.defeat_button.setChecked( False )

		self._update_result_buttons()

		self.status_label.setText( "Estado: Victoria seleccionada." )


	def _set_defeat(self):

		if self.current_match is None:

			return

		self.current_match.result = ( MatchResult.DEFEAT )

		self.victory_button.setChecked( False )

		self.defeat_button.setChecked( True )

		self._update_result_buttons()

		self.status_label.setText( "Estado: Derrota seleccionada." )


	def _update_result_buttons(self):

		if self.current_match is None:

			return


		if self.current_match.result == MatchResult.VICTORY:

			self.victory_button.setStyleSheet("""
				QPushButton {
					background-color: #2e7d32;
					color: white;
					font-weight: bold;
					padding: 8px 20px;
					border-radius: 5px;
				}
			""")

			self.defeat_button.setStyleSheet("""
				QPushButton {
					background-color: #303030;
					color: #aaaaaa;
					padding: 8px 20px;
					border-radius: 5px;
				}
			""")


		elif self.current_match.result == MatchResult.DEFEAT:

			self.victory_button.setStyleSheet("""
				QPushButton {
					background-color: #303030;
					color: #aaaaaa;
					padding: 8px 20px;
					border-radius: 5px;
				}
			""")

			self.defeat_button.setStyleSheet("""
				QPushButton {
					background-color: #b71c1c;
					color: white;
					font-weight: bold;
					padding: 8px 20px;
					border-radius: 5px;
				}
			""")

	# =====================================================
	# SAVE MATCH
	# =====================================================

	def _save_match(self):

		if self.current_match is None:

			self.status_label.setText( "Error: no hay ninguna partida cargada." )

			return


		if self.current_match.result is None:

			self.status_label.setText( "Error: selecciona Victoria o Derrota." )

			return


		try:

			match_id = self.match_service.save_match( self.current_match )

			self.status_label.setText(
				f"Partida guardada correctamente. "
				f"ID: {match_id}"
			)

			self.save_button.setEnabled( False )


		except Exception as error:

			self.status_label.setText( f"Error al guardar la partida: {error}" )


	# =====================================================
	# MODULE CALLBACKS
	# =====================================================

	def _on_recognition_finished( self, match ):

		self.load_match( match )

		self.save_button.setEnabled( True )

		self.status_label.setText( "Estado: Partida reconocida." )



	# =====================================================
	# PLAYER HISTORY TOOLTIP
	# =====================================================

	def _show_player_history( self, player_name: str, player_team: str ):

		history = self.match_service.get_player_history( player_name, player_team, limit = 4 )


		if not history:

			tooltip = (
				f"<b>{player_name}</b><br>"
				"<span style='color:#888888;'>"
				"No hay partidas guardadas."
				"</span>"
			)

		else:

			lines = [
				f"<b>{player_name}</b>",
				"<br>"
			]


			for index, match in enumerate(
				history
			):

				result = match["result"]

				if player_team == "enemy":
					team_text = ("<span style='color:#f87171;'>" "ENEMIGO" "</span>" )
				else:
					team_text = ( "<span style='color:#4ade80;'>" "ALIADO" "</span>" )

				character = (
					match["character"]
					or "Sin héroe"
				)

				performance = (
					match["performance"]
				)


				if result == "victory":

					result_text = (
						"<span style='color:#4ade80;'>"
						"VICTORIA"
						"</span>"
					)

				else:

					result_text = (
						"<span style='color:#f87171;'>"
						"DERROTA"
						"</span>"
					)


				if performance == "good":

					performance_text = "↑ GOOD"

				elif performance == "bad":

					performance_text = "↓ BAD"

				else:

					performance_text = "━ NEUTRAL"


				lines.append(
					f"{result_text}"
					f"{team_text}"
					f" — {character}"
					f" — {performance_text}"
				)


				if index < len(history) - 1:

					lines.append(
						"<hr>"
					)


			tooltip = "<br>".join(
				lines
			)


		QToolTip.showText(
			QCursor.pos(),
			tooltip,
			self
		)


	def _hide_player_history(self):

		QToolTip.hideText()



	def _on_recognition_error( self, message: str ):

		self.status_label.setText( f"Error: {message}" )


	def _finish_recognition(self):

		if self.recognition_thread is None:

			return

		self.recognition_thread.quit()

		self.recognition_thread.wait()

		self.recognition_worker.deleteLater()

		self.recognition_thread.deleteLater()

		self.recognition_worker = None
		self.recognition_thread = None



