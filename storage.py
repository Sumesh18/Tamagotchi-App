import json
from pathlib import Path

from tamagotchi import Tamagotchi


SAVE_FILE = Path(__file__).with_name("savegame.json")
PET_COUNT = 3


def save_game(pets: list[Tamagotchi], file_path: str | Path = SAVE_FILE) -> None:
    if len(pets) != PET_COUNT:
        raise ValueError(f"A save must contain exactly {PET_COUNT} Tamagotchis.")

    data = {
        "pets": [
            {
                "name": pet.name,
                "hunger": pet.hunger,
                "health": pet.health,
                "boredom": pet.boredom,
                "exhaustion": pet.exhaustion,
                "alive": pet.is_alive(),
            }
            for pet in pets
        ]
    }

    with Path(file_path).open("w", encoding="utf-8") as save_file:
        json.dump(data, save_file, indent=2)


def load_game(file_path: str | Path = SAVE_FILE) -> list[Tamagotchi] | None:
    try:
        with Path(file_path).open("r", encoding="utf-8") as save_file:
            data = json.load(save_file)
    except FileNotFoundError:
        return None

    if not isinstance(data, dict) or not isinstance(data.get("pets"), list):
        raise ValueError("The save file must contain a list of pets.")
    if len(data["pets"]) != PET_COUNT:
        raise ValueError(f"The save file must contain exactly {PET_COUNT} Tamagotchis.")

    pets = []
    for pet_data in data["pets"]:
        if not isinstance(pet_data, dict):
            raise ValueError("Each saved Tamagotchi must be a JSON object.")

        name = pet_data.get("name")
        status_values = (
            pet_data.get("hunger"),
            pet_data.get("health"),
            pet_data.get("boredom"),
            pet_data.get("exhaustion"),
        )
        alive = pet_data.get("alive")
        if not isinstance(name, str):
            raise ValueError("Tamagotchi name must be a string.")
        if any(type(value) is not int for value in status_values):
            raise ValueError("Tamagotchi status values in the save file must be integers.")
        if status_values[1] < 0:
            raise ValueError("Saved Tamagotchi health cannot be negative.")
        if type(alive) is not bool or alive != (status_values[1] > 0):
            raise ValueError("Saved living/dead status does not match the health value.")

        pet = Tamagotchi(name)
        pet.hunger, pet.health, pet.boredom, pet.exhaustion = status_values
        pets.append(pet)

    return pets