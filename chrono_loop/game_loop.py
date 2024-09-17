import pygame
import random
from npc import NPC
from puzzle import Puzzle

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Chrono Loop: The Paradox Chronicles")

# Load background image
background_image = pygame.image.load('background.jpg')

# Initialize font
font = pygame.font.SysFont(None, 36)

class ChronoLoopGame:
    def __init__(self):
        self.day = 1
        self.max_days = 7
        self.player_inventory = []
        self.environment_state = {
            "storm": 0,
            "time_rift": 0,
            "past_visitor": 0
        }
        self.npcs = {
            "baker": NPC("baker", "grumpy", quest_chain=["find_flour", "bake_bread", "deliver_bread"]),
            "scientist": NPC("scientist", "mysterious", quest_chain=["find_crystal", "power_machine", "escape_loop"])
        }
        self.puzzles = {
            "Lighthouse Signal": Puzzle("Lighthouse Signal", "align_lens", environmental_change="lighthouse_active"),
            "Time Machine": Puzzle("Time Machine", "activate_machine", required_items=["crystal_fragment", "temporal_key"], npc_help="scientist")
        }

    def random_event(self):
        events = [
            {"name": "storm", "effect": "navigation_harder", "duration": 2},
            {"name": "time_rift", "effect": "see_future", "duration": 1},
            {"name": "past_visitor", "effect": "cryptic_advice", "duration": 1}
        ]
        if random.random() < 0.3:  # 30% chance for an event each day
            event = random.choice(events)
            self.environment_state[event["name"]] = event["duration"]
            print(f"Random Event: A {event['name']} occurs! It will last for {event['duration']} days.")
            if event["name"] == "storm":
                print("A storm is making NPCs less helpful.")
                for npc in self.npcs.values():
                    npc.state = "grumpy"
            elif event["name"] == "time_rift":
                print("A time rift reveals a glimpse of the future.")
            elif event["name"] == "past_visitor":
                print("A mysterious visitor leaves behind a cryptic note.")
                self.player_inventory.append("mysterious_note")

    def draw_text(self, text, position):
        """Helper function to draw text on screen."""
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, position)

    def day_loop(self):
        self.random_event()
        
        # Handle storm duration
        if self.environment_state.get("storm", 0) > 0:
            self.environment_state["storm"] -= 1
            if self.environment_state["storm"] == 0:
                print("The storm has passed.")
                for npc in self.npcs.values():
                    npc.state = "neutral"
            else:
                print("The storm persists, making NPCs less helpful.")
        
        # Handle time rift duration
        if self.environment_state.get("time_rift", 0) > 0:
            self.environment_state["time_rift"] -= 1
            if self.environment_state["time_rift"] == 0:
                print("The time rift closes.")
            else:
                print("You feel time unraveling.")

        self.player_action()

    def player_action(self):
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(background_image, (0, 0))  # Draw background

        self.draw_text("Choose an action:", (50, 50))
        self.draw_text("1. Talk to an NPC", (50, 100))
        self.draw_text("2. Attempt to solve a puzzle", (50, 150))
        self.draw_text("3. Check your inventory", (50, 200))
        pygame.display.flip()

        action = input("\nEnter your action: ")
        
        if action == "1":
            self.talk_to_npc()
        elif action == "2":
            self.attempt_puzzle()
        elif action == "3":
            print(f"Inventory: {self.player_inventory}")
        else:
            print(f"Invalid action: {action}. Please choose a valid action.")

    def talk_to_npc(self):
        print(f"Available NPCs: {', '.join(self.npcs.keys())}")
        npc_name = input("Which NPC do you want to talk to? ")
        if npc_name in self.npcs:
            action = input(f"What do you say or do to {npc_name}? ")
            self.npcs[npc_name].interact(action)
        else:
            print(f"{npc_name} is not available.")

    def attempt_puzzle(self):
        print(f"Available Puzzles: {', '.join(self.puzzles.keys())}")
        puzzle_name = input("Which puzzle do you want to attempt? ")
        if puzzle_name in self.puzzles:
            action = input(f"How will you solve the {puzzle_name}? ")
            if self.puzzles[puzzle_name].attempt_solution(action, self.player_inventory, {npc.name: npc.state for npc in self.npcs.values()}):
                print(f"You've solved the puzzle: {puzzle_name}")
        else:
            print("That puzzle doesn't exist yet.")

    def handle_end_condition(self):
        if self.day > self.max_days:
            print("The loop resets!")
            self.reset_game()

    def reset_game(self):
        self.day = 1
        self.environment_state = {
            "storm": 0,
            "time_rift": 0,
            "past_visitor": 0
        }
        print("The world resets. Try again with new strategies.")
    
    def start_game(self):
        print("Welcome to Chrono Loop: The Paradox Chronicles!")
        while self.day <= self.max_days:
            print(f"--- Day {self.day} ---")
            self.day_loop()
            self.day += 1
        self.handle_end_condition()

if __name__ == "__main__":
    game = ChronoLoopGame()
    game.start_game()

    # Quit Pygame after game loop ends
    pygame.quit()
