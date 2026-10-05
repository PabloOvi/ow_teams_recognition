import cv2
import numpy as np

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
				(190, 240),
				(260, 310),
				(330, 380),
				(390, 440),
				(450, 505)
			]

			x1 = 410
			x2 = 600

		else:

			rows = [
				(600, 650),
				(660, 710),
				(730, 780),
				(790, 850),
				(860, 910)
			]

			x1 = 370
			x2 = 600


		players = []

		for y1, y2 in rows:

			crop = frame[
				y1:y2,
				x1:x2
			]

			# Convertimos todo lo que no sea blanco a negro.
			crop = self._filter_colors( crop )

			text = self.ocr_reader.read( crop )

			name = text.replace( " ", "" ).upper()

			if not name:
				continue

			players.append( Player( name= name, team= team ) )

		return players


	def _filter_colors( self, crop ):

		# Convertimos BGR -> HSV para poder distinguir el blanco de colores.
		hsv = cv2.cvtColor(
			crop,
			cv2.COLOR_BGR2HSV
		)

		# Definimos qué consideramos "blanco".

		lower = np.array([
			0,
			0,
			160
		])

		upper = np.array([
			255,
			20,
			255
		])

		mask = cv2.inRange(
			hsv,
			lower,
			upper
		)

		return mask
