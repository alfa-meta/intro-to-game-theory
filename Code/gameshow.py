import random
import os
import json



def set_game_list(game_list: bool, number_of_doors: int)-> bool:
    print("Setting Game List")
    for _ in list(range(number_of_doors)):
        game_list.append(False)
    print("Game List: " + str(game_list))
    return game_list

def insert_random_true_value(game_list: bool, number_of_doors:int) -> bool:
    print("Inserting Random True Value")
    num = random.randint(0, number_of_doors - 1)
    print(num, number_of_doors)
    game_list[num] = True
    print("Game List: " + str(game_list))
    return game_list

def return_2_doors(game_list: bool, players_original_decision: int) -> int:
    new_game_list = list(range(len(game_list)))
    correct_door = 0
    false_door = 1
    for i in new_game_list:
        if game_list[i] == True:
            correct_door = i
            if players_original_decision != i:
                false_door = players_original_decision
                break
            if correct_door == 0:
                false_door = random.randint(1, len(new_game_list)- 1)
            elif correct_door == len(new_game_list)-1:
                false_door = random.randint(0, len(new_game_list)- 2)
            else:
                range_1 = random.randint(0, i-1)
                range_2 = random.randint(i+1, len(new_game_list) - 1)
                outcome = random.randint(0, 1)
                if outcome == 0:
                    false_door = range_1
                else:
                    false_door = range_2
            break
    print(f"Correct Door: {correct_door}", f"False Door: {false_door}")
    return correct_door, false_door

def change_or_stay(answer_tuple: int, players_original_decision:int, probability: float) -> int:
    
    change: bool = prob_to_bool(probability)
    value_selected = answer_tuple.index(players_original_decision)
    final_answer = 0
    if change:
        final_answer = answer_tuple[value_selected - 1]
    else:
        final_answer = answer_tuple[value_selected]
    print(f"Final Answer: {final_answer}")
    return final_answer


def prob_to_bool(prob: float) -> bool:
    if prob <= 0:   # 0 means always False
        return False
    if prob >= 1:   # 1 means always True
        return True
    return random.random() < prob  # weighted random for values in between


        

def did_the_player_win(final_answer:int, answer_tuple: int) -> bool:
    if answer_tuple[0] == final_answer:
        return "Yes"
    return "No"      



def is_valid_format(data: dict) -> bool:
    # Must contain name (string) and game with required keys
    if not isinstance(data, dict):
        return False
    if "name" not in data or not isinstance(data["name"], str):
        return False
    if "game" not in data or not isinstance(data["game"], dict):
        return False
    
    required_game_keys = {"three_doors", "five_doors", "ten_doors"}
    if not required_game_keys.issubset(data["game"].keys()):
        return False
    
    # Check all game values are numbers (int/float)
    if not all(isinstance(data["game"][k], (int, float)) for k in required_game_keys):
        return False
    
    return True

def import_all_players(folder_path) -> dict:
    print("Importing all Players")
    player_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if is_valid_format(data):
                        player_dict[data["name"]] = data["game"]
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {filename}")
    return player_dict

def gameshow(player_dict: dict, number_of_doors: int):
    
    game_list: bool = []
    players_original_decision = random.randint(0, number_of_doors - 1)
    print(players_original_decision)
    game_list = set_game_list(game_list, number_of_doors)
    game_list = insert_random_true_value(game_list, number_of_doors)
    answer_tuple = (return_2_doors(game_list, players_original_decision))
    final_answer = change_or_stay(answer_tuple, players_original_decision, change=True)
    print(did_the_player_win(final_answer, answer_tuple))


def main(player_dict: dict):
    print("Starting Game")
    for name, game in player_dict.items():
        print(f"Name: {name}")
        print("Games:")
        for game_name, probability in game.items():
            print(f"{game_name}: {probability}")
        # gameshow(player, 3)
        # gameshow(player, 5)
        # gameshow(player, 10)

### Main ###
player_dict = import_all_players("gameshow_players")

main(player_dict)