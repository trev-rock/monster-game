import random
# in this prototype a monster is generated with the method, then it becomes an object, the object will generate its own moves
# this has no error handling so type in everything precisely

# tuples containing all of the attributes that will be chosen at random upon a monsters creation
class_affinities = ("reinforcer","elementalist","controller","materializer","effluence","specialist") # one of the 6 nen types, these will influence what moves they can and have a damage multiplier, a monster has 1 of these assigned at creation, cannot use specalist moves unless they are a specalist 

elemental_types = ("normal","grass","fire","water","flying","poison","electric","ground","psychic","rock","ice","bug","dragon","ghost","dark","steel","fairy") # a monster has one or two types, STAB exists for bonus damage

natures = ('hardy','lonely','brave','adamant','naughty','bold','relaxed','impish','lax','timid','hasty','jolly','naive','modest','quiet','rash','calm','gentle','sassy','careful') # effect stats, at some point add values to these that effect the stats that are generated

# passives will be based on their affinities, for sake of this example there will only be a few so it just won't boost the moves as much instead of not being able to use it at all for the affinities
passives = ('brawler_buff', 'summon_minion', 'electrify') # increase melee attack dmg and defense, summon a minion that will eventually do something, increase speed


def generate_affinity():
    return random.choice(class_affinities)

def generate_elemental_type():
    num = random.randint(1,2)
    if num == 1:
       type = random.choice(elemental_types)
    elif num == 2:
        type = random.choices(elemental_types, k = 2)
    return type

def generate_nature():
    return random.choice(natures)

def generate_stats():
    hp_iv, a_iv, spa_iv, d_iv, spd_iv, s_iv = random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10)
    stats = {
        "health": random.randint(50,100) + hp_iv,
        "attack" : random.randint(50,100) + a_iv,
        "special attack": random.randint(50,100) + spa_iv,
        "defense": random.randint(50,100) + d_iv,
        "special defense": random.randint(50,100) + spd_iv,
        "speed": random.randint(50,100) + s_iv
        }
    return stats 

def generate_passive():
    return random.choice(passives)

def class_affinity_multiplier(affinity, move_affinity):
    # enhancer -> reinforcer
    # manipulator -> controller
    # transmuter -> elementalist/ransformationist 
    # conjurerer -> materializer 
    # emitter -> effluence

    # only speciailists can use specialist attacks

    if affinity == 'reinforcer':
        if move_affinity == 'reinforcer':
            return 1
        elif move_affinity == 'emission' or move_affinity == 'elementalist':
            return .8
        else:
            return .6
    
    if affinity == 'controller':
        if move_affinity == 'controller':
            return 1
        elif move_affinity == 'effluence':
            return .8
        elif move_affinity == 'reinforcer' or move_affinity == 'materializer':
            return .6
        else:
            return .4
    
    if affinity == 'effluence':
        if move_affinity == 'effluence':
            return 1
        elif move_affinity == 'reinforcer' or move_affinity == 'controller':
            return .8
        elif move_affinity == 'elementalist':
            return .6
        else:
            return .4
    
    if affinity == 'elementalist':
        if move_affinity == 'elementalist':
            return 1
        elif move_affinity == 'reinforcer' or move_affinity == 'materialist':
            return .8
        elif move_affinity == 'effluence':
            return .6
        else:
            return .4
    
    if affinity == 'materialist':
        if move_affinity == 'materialist':
            return 1
        elif move_affinity == 'elementalist':
            return .8
        elif move_affinity == 'controller' or move_affinity == 'reinforcer':
            return .6
        else: 
            return .4
        
    if affinity == 'specialist':
        if move_affinity == 'specialist':
            return 1
        if move_affinity == 'controller' or move_affinity == 'materialist':
            return .8
        if move_affinity == 'effluence' or move_affinity == 'elementalist':
            return .6
        else:
            return .4

def phys_or_spec():
    num = random.randint(1,2)
    if num == 1:
        return "physical"
    else: 
        return "special"


# using the move is another method and that's where it'll get put in the calculator to figure out which stat to use from the user

# have something for moves that it will generate a random number that if it is a certain number or range then it is a crit and otherwise it isn't this would be when the monster uses the move which then goes into the calculator 

def damage_calculator(level, base_power, user_attack_stat, defender_def_stat, weather, critical, stab, user_affinity, move_affinity, burn, terrain, user_type):
    # need to eventually add in the enemies type as a factor for increasing/reducing damage 
    # stab value gets figured out when the user uses the use move method 
    if stab == True:
        stab = 1.5
    else:
        stab = 1

    # critical value
    if critical == True:
        critical = 1.5
    else:
        critical = 1

    # user's type and terrain to be added to boost other types damage
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
    
    # add a feature to if they get the timing right on moves that allow it to increase some other additional damage
    # add a multiplier for terrain
    # add a multiplier for other things that can be factored in, this would always be 1 unless it is otherwise something else

    if burn == True:
        burn = .5
    else:
        burn = 1
    
    affinity_mult = class_affinity_multiplier(user_affinity, move_affinity)


    damage = (((2*level)/5 +2) * base_power * (user_attack_stat/defender_def_stat)) * weather * critical * random.randint(85,100)/100 * stab * affinity_mult * burn

    return int(damage)

class monster:
    def __init__(self, name: str):
        self.name = name # str
        self.class_affinity = generate_affinity() # str
        self.elemental_typing = generate_elemental_type() # list 
        self.nature = generate_nature() # str
        self.stats = generate_stats() # dict
        self.passive = generate_passive() # str
        self.attacks = []

        self.health = self.stats["health"] + self.stats["health"] * 5

        for i in range(1,5):
            self.attacks.append(attack(f'attack {i}'))
        
    def get_monster(self):
        print(f"name: {self.name} \naffinity: {self.class_affinity} \ntyping: {self.elemental_typing} \nnature: {self.nature} \nstats: {self.stats} \npassive: {self.passive} \n\n")
        self.get_attacks()
    
    def get_attacks(self):
        for i in self.attacks:
            print(f'{i.name} - {i.base_power} - {i.elemental_typing} - {i.class_affinity} - {i.phys_or_spec}')
    
    def use_attack(self, enemy):
        if self.name == "monster 2": # this is just to make the other monster attack at random 
            choice = random.randint(0,3)
        else:
            choice = int(input('type in the number of which attack you would like to use: ')) - 1

        attack = self.attacks[choice]
        print(f'using attack {attack.name}')
        crit_roll = random.randint(1,32)
        if crit_roll == 1:
            crit = True
            print("oh shit it's a crit")
        else:
            crit = False
        
        # this might cause errors eventually since they're two lists
        # maybe in order for it to be stab it has to exact even if its a two type attack
        if attack.elemental_typing == self.elemental_typing:
            stab = True
        else:
            stab = False

        if attack.phys_or_spec == 'physical':
            damage = damage_calculator(10, attack.base_power, self.stats["attack"], enemy.stats["defense"], 'none', crit, stab, self.class_affinity, attack.class_affinity, False, "none", self.elemental_typing)
        else:
            damage = damage_calculator(10, attack.base_power, self.stats["special attack"], enemy.stats["special defense"], 'none', crit, stab, self.class_affinity, attack.class_affinity, False, "none", self.elemental_typing)
        print(f"{self.name}'s attack dealt {damage} damage")
        enemy.health -= damage
        


class attack:
    def __init__(self, name): 
        # work in a crit ratio into the calculator
        self.name = name
        self.base_power = random.randint(30,120)
        self.elemental_typing = generate_elemental_type()
        self.class_affinity = generate_affinity()
        self.phys_or_spec = phys_or_spec()
       # self.crit_ratio = crit_ratio # we want the attack to only crit at random so figure that out


monster1 = monster("monster 1")
monster2 = monster("monster 2")
monster1.get_monster()
monster2.get_monster()

# gameplay loop
while True:
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
