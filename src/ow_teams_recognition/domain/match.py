from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .player import Player
from .enums import MatchResult


@dataclass
class Match:

	players: List[Player] = field( default_factory = list )

	created_at: datetime = field( default_factory = datetime.now )

	result: Optional[MatchResult] = None


	def allied_players(self) -> List[Player]:

		return [
			player
			for player in self.players
			if player.team.value == "allied"
		]


	def enemy_players(self) -> List[Player]:

		return [
			player
			for player in self.players
			if player.team.value == "enemy"
		]