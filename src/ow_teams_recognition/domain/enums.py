from enum import Enum

class Team(Enum):

	ALLIED = "allied"
	ENEMY = "enemy"

class Performance(Enum):

	BAD = "bad"
	NEUTRAL = "neutral"
	GOOD = "good"

class MatchResult(Enum):

	VICTORY = "victory"
	DEFEAT = "defeat"