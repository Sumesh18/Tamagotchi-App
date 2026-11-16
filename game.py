def living_and_dead(pets):
    for pet in pets:
        if pet.is_alive():
            print(f"{pet.name} is Alive!")
        else:
            print(f"{pet.name} is Dead!")

def average_health(pets):
    print(f"Average health of all pets is : {sum(pets.health)/len(pets)}")
    
def average_stats(pets):
    print(f"Average hunger of all pets is : {sum(pets.hunger)/len(pets)}")    
    print(f"Average boredom of all pets is : {sum(pets.boredom)/len(pets)}")    
    print(f"Average exhaustion of all pets is : {sum(pets.exhaustion)/len(pets)}")    