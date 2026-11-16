from tamagotchi import Tamagotchi
from game import living_and_dead
from storage import PET_COUNT, load_game, save_game


def create_pets():
    pets = []
    for index in range(PET_COUNT):
        name = input(f"Enter the name of pet {index + 1}: ")
        pets.append(Tamagotchi(name))
    return pets


def main():
    pets = None
    while pets is None:
        print("***START***\n1. New game\n2. Load saved game")
        choice = input("Enter your choice: ")
        if choice == "1":
            pets = create_pets()
        elif choice == "2":
            try:
                pets = load_game()
            except (OSError, ValueError) as error:
                print(f"Could not load saved game: {error}")
            else:
                if pets is None:
                    print("No saved game was found.")
        else:
            print("Invalid choice. Please choose 1 or 2.")

    should_exit = False
    for pet in pets:
        while pet.is_alive() and not should_exit:
            print(
                "***MENU***\n1. Feed\n2. Play\n3. Sleep\n4. Heal\n"
                "5. Statistics\n6. Save game\n7. Exit\n"
            )
            choice = input("Enter your choice: ")
            if choice == "7":
                should_exit = True
                break
            elif choice == "1":
                pet.feed()
            elif choice == "2":
                pet.play()
            elif choice == "3":
                pet.sleep()
            elif choice == "4":
                pet.heal()
            elif choice == "5":
                pet.stats()
            elif choice == "6":
                try:
                    save_game(pets)
                except (OSError, ValueError) as error:
                    print(f"Could not save game: {error}")
                else:
                    print("Game saved.")
                continue
            else:
                print("Invalid choice. Please choose 1-7.")
                continue
            pet.random_event()

    for index, pet in enumerate(pets):
        print(
            f"Pet {index + 1}:\nName: {pet.name}\nHunger: {pet.hunger}\n"
            f"Health: {pet.health}\nBoredom: {pet.boredom}\n"
            f"Exhaustion: {pet.exhaustion}\n"
        )
    living_and_dead(pets)


if __name__ == "__main__":
    main()
