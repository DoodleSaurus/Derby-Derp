import random
import os
import sys
import time
from time import sleep

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Horse name
HORSE_FIRST_NAMES = ["Thunder", "Midnight", "Lightning", "Desert", "Ocean", "Mountain", "Silver", "Golden", "Red", "Shadow"]
HORSE_LAST_NAMES = ["Blaze", "Storm", "Rider", "Queen", "King", "Spirit", "Dream", "Chaser", "Flash", "Wind"]

# Weather effects
WEATHER_TYPES = ["Sunny", "Rainy", "Windy", "Foggy", "Perfect"]
WEATHER_EFFECTS = {
    "Sunny": {"speed_multiplier": 1.0, "description": "Clear skies, normal racing conditions"},
    "Rainy": {"speed_multiplier": 0.8, "description": "Slippery track, all horses 20% slower"},
    "Windy": {"speed_multiplier": 1.1, "description": "Tailwind boost, all horses 10% faster"},
    "Foggy": {"speed_multiplier": 0.9, "description": "Poor visibility, all horses 10% slower"},
    "Perfect": {"speed_multiplier": 1.2, "description": "Ideal conditions, all horses 20% faster"}
}

# Obstacles and Power-ups
OBSTACLES = [
    {"name": "Mud Patch", "effect": "lose 2 positions", "chance": 0.1},
    {"name": "Hurdle", "effect": "lose 1 position", "chance": 0.15},
    {"name": "Water Jump", "effect": "lose 3 positions", "chance": 0.05}
]

POWER_UPS = [
    {"name": "Energy Boost", "effect": "gain 4 positions", "chance": 0.1},
    {"name": "Lucky Horseshoe", "effect": "skip next obstacle", "chance": 0.08},
    {"name": "Second Wind", "effect": "recover 2 stamina", "chance": 0.05}
]

class Horse:
    def __init__(self, number):
        self.number = number
        self.name = self.generate_name()
        self.stamina = 100
        self.injury_days = 0
        self.races_run = 0
        self.total_wins = 0
        self.championship_points = 0
    
    def generate_name(self):
        return f"{random.choice(HORSE_FIRST_NAMES)} {random.choice(HORSE_LAST_NAMES)}"
    
    def can_race(self):
        return self.injury_days == 0 and self.stamina > 20
    
    def rest(self):
        if self.injury_days > 0:
            self.injury_days -= 1
        self.stamina = min(100, self.stamina + 30)
    
    def apply_race_effects(self):
        self.races_run += 1
        self.stamina -= random.randint(15, 25)
        
        # Injury chance increases with low stamina
        if self.stamina < 30 and random.random() < 0.3:
            self.injury_days = random.randint(1, 3)
            return f"{self.name} got injured! Will miss {self.injury_days} races."
        return None

class Championship:
    def __init__(self, num_races=5):
        self.num_races = num_races
        self.current_race = 0
        self.leaderboard = {}
        self.grand_prize = num_races * 200
    
    def award_points(self, positions):
        points = [10, 6, 4, 2, 1]  # Points for 1st through 5th
        for i, horse_num in enumerate(positions[:5]):
            if horse_num in self.leaderboard:
                self.leaderboard[horse_num] += points[i]
            else:
                self.leaderboard[horse_num] = points[i]
    
    def get_standings(self, horses):
        sorted_standings = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        standings = []
        for horse_num, points in sorted_standings:
            horse = next((h for h in horses if h.number == horse_num), None)
            if horse:
                standings.append((horse, points))
        return standings
    
    def is_complete(self):
        return self.current_race >= self.num_races

def race_animation(horses, weather, championship):
    horse_positions = [0] * len(horses)
    finish_line = 40
    obstacles_triggered = [False] * len(horses)
    powerups_used = [False] * len(horses)
    
    clear_console()
    print(f"\nWeather: {weather} - {WEATHER_EFFECTS[weather]['description']}")
    time.sleep(2)
    print("The race is starting!\n")
    time.sleep(2)
    clear_console()
    
    while True:
        clear_console()
        print(f"Championship Race {championship.current_race + 1}/{championship.num_races}")
        print(f"Weather: {weather}\n")
        
        for i, horse in enumerate(horses):
            if horse_positions[i] >= finish_line:
                continue
                
            # Base movement with stamina effect
            base_move = random.randint(1, 3)
            stamina_effect = horse.stamina / 100  # 50% stamina = 50% speed
            weather_effect = WEATHER_EFFECTS[weather]["speed_multiplier"]
            move = int(base_move * stamina_effect * weather_effect)
            
            # Apply obstacles
            if not obstacles_triggered[i] and random.random() < 0.1:
                obstacle = random.choice(OBSTACLES)
                if random.random() < obstacle["chance"]:
                    move = max(0, move - 2)
                    print(f"{horses[i].name} hit {obstacle['name']}! {obstacle['effect']}")
                    obstacles_triggered[i] = True
            
            # Apply power-ups
            if not powerups_used[i] and random.random() < 0.08:
                powerup = random.choice(POWER_UPS)
                if random.random() < powerup["chance"]:
                    if powerup["name"] == "Energy Boost":
                        move += 4
                    elif powerup["name"] == "Second Wind":
                        horse.stamina = min(100, horse.stamina + 20)
                    print(f"{horses[i].name} got {powerup['name']}! {powerup['effect']}")
                    powerups_used[i] = True
            
            horse_positions[i] += move
            if horse_positions[i] >= finish_line:
                horse_positions[i] = finish_line
        
        # Display race progress
        for i, horse in enumerate(horses):
            position_display = '-' * horse_positions[i] + 'P'
            stamina_display = f"[Stamina: {horse.stamina}%]"
            injury_display = "!" if horse.injury_days > 0 else ""
            print(f"{horse.name} {injury_display}: {position_display} {stamina_display}")
        
        if all(pos >= finish_line for pos in horse_positions):
            break
        
        sleep(0.3)
    
    # Determine finishing order
    finishing_order = sorted(range(len(horse_positions)), key=lambda i: horse_positions[i], reverse=True)
    winner_idx = finishing_order[0]
    
    print(f"\n{horses[winner_idx].name} wins the race!")
    return [horses[i].number for i in finishing_order]

def display_horse_status(horses):
    print("\nHorse Status:")
    for horse in horses:
        status = "READY" if horse.can_race() else f"INJURED ({horse.injury_days} races left)"
        print(f"{horse.number}. {horse.name} - Stamina: {horse.stamina}% - {status}")

def main():
    print("Welcome to the Horse Betting Championship!")
    
    # Initialize championship
    championship = Championship(num_races=5)
    
    # Create horses
    horses = [Horse(i+1) for i in range(5)]  # 5 horses for championship
    
    balance = 100
    race_count = 0
    
    while balance > 0 and not championship.is_complete():
        print(f"\n{'='*50}")
        print(f"HORSE BETTING CHAMPIONSHIP - Race {championship.current_race + 1}/{championship.num_races}")
        print(f"Your balance: ${balance}")
        print(f"{'='*50}")
        
        display_horse_status(horses)
        
        # Check if any horses can race
        available_horses = [h for h in horses if h.can_race()]
        if len(available_horses) < 2:
            print("\nNot enough healthy horses to race! Resting all horses...")
            for horse in horses:
                horse.rest()
            continue
        
        try:
            bet_amount = int(input("\nEnter your bet amount (or 0 to quit): "))
            if bet_amount == 0:
                clear_console()
                print("Thanks for playing! Goodbye.")
                time.sleep(3)
                break
            if bet_amount > balance or bet_amount < 0:
                clear_console()
                print("Invalid bet amount. Try again.")
                time.sleep(3)
                continue
            clear_console()
            print("\nAvailable horses:")
            for horse in available_horses:
                print(f"{horse.number}. {horse.name} (Stamina: {horse.stamina}%)")
            
            horse_choice = int(input("Choose a horse to bet on: "))
            if horse_choice not in [h.number for h in available_horses]:
                clear_console()
                print("Invalid horse choice or horse cannot race. Try again.")
                time.sleep(3)
                clear_console()
                continue
                
        except ValueError:
            clear_console()
            print("Invalid input. Please enter numbers only.")
            time.sleep(3)
            clear_console()
            continue
        
        clear_console()
        # Determine weather for this race
        weather = random.choice(WEATHER_TYPES)
        
        # Run the race
        finishing_order = race_animation(available_horses, weather, championship)
        
        # Update championship points
        championship.award_points(finishing_order) 
        championship.current_race += 1
        
        # Check if player won
        chosen_horse = next(h for h in available_horses if h.number == horse_choice)
        if finishing_order[0] == horse_choice:
            winnings = bet_amount * 2
            clear_console()
            print(f"Congratulations! {chosen_horse.name} won! You won ${winnings}!")
            time.sleep(3)
            clear_console()
            balance += winnings
        else:
            clear_console()
            print(f"Sorry, {chosen_horse.name} didn't win. You lost ${bet_amount}.")
            time.sleep(3)
            clear_console()
            balance -= bet_amount
        
        # Apply race effects to horses
        print("\nPost-Race Updates:")
        for horse in available_horses:
            injury_msg = horse.apply_race_effects()
            if injury_msg:
                print(f"  {injury_msg}")
        
        # Rest horses between races
        clear_console()
        print("\nHorses are resting...")
        for horse in horses:
            horse.rest()
        
        time.sleep(3)
        clear_console()
        
        # Show championship standings
        if championship.current_race > 0:
            print(f"\nChampionship Standings after Race {championship.current_race}:")
            standings = championship.get_standings(horses)
            for i, (horse, points) in enumerate(standings[:3], 1):
                print(f"  {i}. {horse.name}: {points} points")
    
    # Championship completion
    if championship.is_complete():
        print(f"\n{'*' * 10} CHAMPIONSHIP COMPLETE! {'*' * 10}")
        final_standings = championship.get_standings(horses)
        if final_standings:  # Check if standings exist
            champion = final_standings[0][0]
            champion_points = final_standings[0][1]
            
            print(f"\nCHAMPION: {champion.name} with {champion_points} points!")
            print(f"Grand Prize: ${championship.grand_prize}")
            
            # Award bonus for betting on champion
            balance += championship.grand_prize // 10
            print(f"You received ${championship.grand_prize // 10} bonus for completing the championship!")
    
    print(f"\nFinal balance: ${balance}")
    print("Thanks for playing the Horse Betting Championship!")

if __name__ == "__main__":
    main()