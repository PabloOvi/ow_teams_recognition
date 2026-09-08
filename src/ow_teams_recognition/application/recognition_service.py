from ..domain.enums import Team
from ..domain.match import Match
from ..domain.player import Player


class RecognitionService:

	def __init__( self, screen_capture, ocr_reader ):

		self.screen_capture = screen_capture
		self.ocr_reader = ocr_reader


	def recognize_match( self ) -> Match:

		frame = self.screen_capture.capture()

		# Obtenemos la lista de jugadores.

		allied_players = self._recognize_team( frame, Team.ALLIED )

		enemy_players = self._recognize_team( frame, Team.ENEMY )

		return Match( players=[ *allied_players, *enemy_players ] )


	def _recognize_team( self, frame, team: Team ) -> list[Player]:

		# Recortamos la pantalla para obtener las tarjetas de nombre sin los titulos, evitando tener texto extra para la lectura de ocr.

		if team == Team.ALLIED:

			rows = [
				(300, 370),
				(410, 480),
				(520, 580),
				(625, 685),
				(740, 790)
			]

			x1 = 210
			x2 = 625

		else:

			rows = [
				(320, 380),
				(430, 480),
				(520, 580),
				(625, 685),
				(730, 790)
			]

			x1 = 1300
			x2 = 1600


		players = []

		for y1, y2 in rows:

			crop = frame[
							y1:y2,
							x1:x2
			]

			text = self.ocr_reader.read( crop )

			name = text.strip()

			if not name:
				continue

			players.append( Player( name = name, team = team ) )

		return players