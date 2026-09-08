from dataclasses import dataclass
from typing import Optional
from .enums import Performance, Team

# Es importante setear el nombre del 'titular'.

MAIN_PLAYER_NAME = "PGAish"

# Creamos las cosas obligatorias que tiene que tener un jugador dentro del sistema.

@dataclass
class Player:

	name: str
	team: Team
	character: Optional[str] = None
	performance: Performance = Performance.NEUTRAL

	# Agregamos propieades para ver si es titular y si guardamos las estadisticas del mismo.

	@property
	def is_main_player(self) -> bool:
		return self.name.lower() == MAIN_PLAYER_NAME.lower()

	@property
	def has_performance(self) -> bool:

		return not self.is_main_player