import os

from aura_life import LifeService, hooks
from aura_life.world import WorldEnvironment


class Config:
    data_dir = "./src/amadeus_data"
    place_enabled = False


def _getConfig():
    return Config


hooks.configure(get_config=_getConfig)
os.makedirs(Config.data_dir, exist_ok=True)

_world = WorldEnvironment()
_amadeus = None


def get_world():
    return _world

def get_amadeus():
    global _amadeus
    if _amadeus is None:
        _amadeus = LifeService(
            db_path="./src/amadeus_data/kurisu.db",
            persona_id="kurisu",
            world_environment=_world,
            occupation="neuroscientist",
            interests=["physics", "time travel"],
        )
    return _amadeus