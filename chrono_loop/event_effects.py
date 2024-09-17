def apply_event_effects(event, game):
    if event == "storm":
        print("A storm is raging. NPCs are grumpy and reluctant to help.")
        for npc in game.npcs.values():
            npc.state = "grumpy"
    elif event == "time_rift":
        print("A time rift opens. You catch a glimpse of a future clue.")
    elif event == "past_visitor":
        print("A mysterious visitor appears, leaving behind a cryptic note.")
        game.player_inventory.append("cryptic_note")
