from email.mime import base
import random
import math

# this prototype is to mostly work out the regular attack calculator & logic, super effective damage still needs to be worked into it


elemental_types = ("normal","grass","fire","water","flying","poison","electric","ground","psychic","rock","ice","bug","dragon","ghost","dark","steel","fairy")
natures = ('hardy','lonely','brave','adamant','naughty','bold','relaxed','impish','lax','timid','hasty','jolly','naive','modest','quiet','rash','calm','gentle','sassy','careful')
def generate_nature():
    return random.choice(natures)

class monster:
    def __init__(self, name: str):
        self.name = name # str
        self.elemental_typing = None # will be hard coded into the example monsters
        self.nature = generate_nature() # currently doesn't do anything 
        self.stats = None # will be hard coded 
        self.passive = None

        
    def get_monster(self):
        print(f"name: {self.name}\ntyping: {self.elemental_typing} \nnature: {self.nature} \nstats: {self.stats} \npassive: {self.passive} \n")
        self.get_attacks()
        print("\n\n")
    
    def get_attacks(self):
        for i in self.attacks:
            print(f'{i.name} - {i.base_power} - {i.elemental_typing} - {i.phys_or_spec} - {i.accuracy}')
    
    def use_attack(self, enemy):
        if self.name == "monster 2": # this is just to make the other monster attack at random 
            choice = random.randint(0,3)
        else:
            choice = int(input('type in the number of which attack you would like to use: ')) - 1

        attack = self.attacks[choice]
        print(f'using attack {attack.name}')
        crit_roll = random.randint(1,32)
        if crit_roll == 20:
            crit = True
            print("oh shit it's a crit")
        else:
            crit = False
    
        if attack.elemental_typing in self.elemental_typing:
            stab = True
        else:
            stab = False

        if attack.phys_or_spec == 'physical':
            damage = damage_calculator_basic_attack(50, attack.base_power, self.stats["attack"], enemy.stats["defense"], "clear", crit, stab, False, self.elemental_typing)
        else:
            damage = damage_calculator_basic_attack(50, attack.base_power, self.stats["special attack"], enemy.stats["special defense"], "clear", crit, stab, False, self.elemental_typing)
        print(f"{self.name}'s attack dealt {damage} damage")
        enemy.health -= damage
        
        


class attack:
    def __init__(self, name, base_power, elemental_typing, phys_or_spec, accuracy): 
        # work in a crit ratio into the calculator
        # side effects do not matter yet
        self.name = name
        self.base_power = base_power
        self.elemental_typing = elemental_typing
        self.phys_or_spec = phys_or_spec
        self.accuracy = accuracy


def damage_calculator_basic_attack(level, base_power, user_attack_stat, defender_def_stat, weather, critical, stab, burn, user_type):
    if stab == True:
        stab = 1.5
    else:
        stab = 1

    if critical == True:
        critical = 1.5
    else:
        critical = 1

    if weather == 'hail' and user_type == 'ice':
        weather = 1.5
    elif weather == 'sunny' and user_type == 'fire' or user_type == 'water':
        if user_type == 'fire':
            weather = 1.5
        else:
            weather = .5
    elif weather == 'sandstorm' and user_type == 'ground' or user_type == 'steel' or user_type == 'rock':
        weather = 1.5
    elif weather == 'rain' and user_type == 'water' or user_type == 'fire':
        if user_type == 'water':
            weather = 1.5
        else:
            weather = .5
    else:
        weather = 1

    if burn == True:
        burn = .5
    else:
        burn = 1


    damage = (((2*level)/5 +2) * base_power * (user_attack_stat/defender_def_stat)) * weather * critical * stab * burn

    print(damage)

    return int(damage)

class monster_1(monster):
    def __init__(self,name):
        super().__init__(name)
        self.elemental_typing = ["grass","poison"]
        self.stats = {"health":80, "attack":82, "defense":83,"special attack":100, "special defense":100, "speed":80}
        self.attacks = [attack('razor leaf',55,"grass","special",95), attack('sludge bomb',95,"poison","special",100), attack('earthquake',100,"ground","physical",100), attack('petal blizzard', 110, 'grass', 'special', 50)]
        self.health = self.stats["health"] + self.stats["health"] * 5

venusaur = monster_1("venusaur")
venusaur.get_monster()

class monster_2(monster):
    def __init__(self,name):
        super().__init__(name)
        self.elemental_typing = ["fire","flying"]
        self.stats = {"health":78, "attack":84, "defense":78,"special attack":109, "special defense":85, "speed":100}
        self.attacks = [attack('flamethrower',90,"fire","special",100), attack('air slash',75,"flying","physical",95), attack('earthquake',100,"ground","physical",100), attack('dragon claw', 80, 'dragon', 'physical', 100)]
        self.health = self.stats["health"] + self.stats["health"] * 5

charizard = monster_2("charizard")
charizard.get_monster()
#print(charizard.health)

class monster_3(monster):
    def __init__(self,name):
        super().__init__(name)
        self.elemental_typing = ["water"]
        self.stats = {"health":79, "attack":83, "defense":100,"special attack":85, "special defense":105, "speed":78}
        self.attacks = [attack('hydro pump',110,"water","special",80), attack('flash cannon',80,"steel","special",100), attack('earthquake',100,"ground","physical",100), attack('aura sphere', 80, 'fighting', 'special', 100)]
        self.health = self.stats["health"] + self.stats["health"] * 5

blastoise = monster_3("blastoise")
blastoise.get_monster()



# gameplay loop
monsters = [venusaur, charizard, blastoise]
monster1 = random.choice(monsters)
monster2 = random.choice(monsters)
while True:
    print(f'monster 1:{monster1.name}\nmonster 2:{monster2.name}')
    print(f"monster1 health: {monster1.health}\nmonster2 health: {monster2.health}")
    if monster1.stats["speed"] > monster2.stats["speed"]:
        monster1.use_attack(monster2)
        if monster2.health <= 0:
            print('monster1 wins')
            break
        monster2.use_attack(monster1)
        if monster1.health <= 0:
            print("monster2 wins")
            break
    else:
        monster2.use_attack(monster1)
        if monster1.health <= 0:
            print("monster2 wins")
            break
        monster1.use_attack(monster2)
        if monster2.health <= 0:
            print('monster1 wins')
            break