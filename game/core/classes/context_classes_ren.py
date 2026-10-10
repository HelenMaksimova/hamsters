"""renpy
init -990 python:
"""

from dataclasses import dataclass, field


@dataclass
class GameStateContext:
    in_battle: bool = False


@dataclass
class BattleContext:
    mob: Mob | None = None


@dataclass
class Context:
    battle: BattleContext = field(init=False)
    game_state: GameStateContext = field(init=False)

    def __post_init__(self) -> None:
        self.battle = BattleContext()
        self.game_state = GameStateContext()
