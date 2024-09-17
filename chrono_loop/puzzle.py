class Puzzle:
    def __init__(self, name, solution, required_items=None, npc_help=None, environmental_change=None):
        self.name = name
        self.solution = solution
        self.state = "unsolved"
        self.required_items = required_items or []
        self.npc_help = npc_help
        self.environmental_change = environmental_change

    def attempt_solution(self, player_action, player_inventory, npc_states):
        if not all(item in player_inventory for item in self.required_items):
            print("You're missing the necessary items to solve this puzzle.")
            return False

        if self.npc_help and npc_states[self.npc_help] != "helpful":
            print(f"{self.npc_help} is not willing to help right now. You might need to improve their mood or affection.")
            return False

        self.state = "solved"
        print(f"You've solved the puzzle: {self.name}!")
        if self.environmental_change:
            print(f"{self.environmental_change} has changed in the environment.")
        return True
