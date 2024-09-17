class NPC:
    def __init__(self, name, initial_state, quest_chain=None, dialogue_tree=None):
        self.name = name
        self.state = initial_state
        self.affection = 0
        self.quest_chain = quest_chain or []
        self.dialogue_tree = dialogue_tree or {}

    def interact(self, player_action):
        if player_action in self.dialogue_tree:
            response = self.dialogue_tree[player_action]
            print(f"{self.name}: {response}")
            if "quest" in response.lower():
                self.advance_quest()
        else:
            print(f"{self.name}: I don't understand what you mean.")

    def advance_quest(self):
        if self.quest_chain:
            current_task = self.quest_chain[0]
            print(f"{self.name}: Here's your task: {current_task}")
            # Remove task from chain as it progresses
            self.quest_chain = self.quest_chain[1:]
        else:
            print(f"{self.name}: No more tasks for now.")

    def give_clue(self, affection_level):
        if self.affection >= affection_level:
            print(f"{self.name}: Here's a clue to help you: 'The lighthouse holds the key to the machine.'")
        else:
            print(f"{self.name}: Maybe if we were closer, I could help you more.")
