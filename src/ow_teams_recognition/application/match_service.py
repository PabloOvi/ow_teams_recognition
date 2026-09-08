from ..domain.match import Match
from ..data.repositories.match_repository import MatchRepository


class MatchService:

	def __init__( self, match_repository: MatchRepository ):

		self.match_repository = ( match_repository )


	def save_match(	self, match: Match ) -> int:

		if match.result is None:

			raise ValueError( "La partida no tiene resultado." )


		if not match.players:

			raise ValueError( "La partida no tiene jugadores." )


		return self.match_repository.save( match )

	# =====================================================
	# PLAYER HISTORY
	# =====================================================

	def get_player_history( self, player_name: str, player_team: str, limit: int = 4 ) -> list[dict]:

		return self.match_repository.get_player_history( player_name, player_team, limit )


