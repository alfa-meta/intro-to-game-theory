import random
import os
import json
import secrets
from typing import Dict, List, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

### Core game helpers ###

def set_game_list(number_of_doors: int) -> List[bool]:
    return [False] * number_of_doors

def insert_random_true_value(game_list: List[bool], number_of_doors: int) -> List[bool]:
    game_list[random.randint(0, number_of_doors - 1)] = True
    return game_list

def return_2_doors(game_list: List[bool], players_original_decision: int) -> Tuple[int, int]:
    n = len(game_list)
    correct_door = next(i for i, v in enumerate(game_list) if v)

    if players_original_decision != correct_door:
        false_door = players_original_decision
    else:
        wrong_doors = [i for i in range(n) if i != correct_door]
        false_door = random.choice(wrong_doors)

    return (correct_door, false_door)

def prob_to_bool(prob: float) -> bool:
    if prob <= 0: return False
    if prob >= 1: return True
    return random.random() < prob

def change_or_stay(answer_tuple: Tuple[int, int], players_original_decision: int, probability: float) -> int:
    if players_original_decision not in answer_tuple:
        answer_tuple = (answer_tuple[0], players_original_decision)
    idx = answer_tuple.index(players_original_decision)
    if prob_to_bool(probability):
        return answer_tuple[1 - idx]
    else:
        return answer_tuple[idx]

def did_the_player_win(final_answer: int, answer_tuple: Tuple[int, int]) -> bool:
    return final_answer == answer_tuple[0]

### I/O + validation ###

def is_valid_format(data: dict) -> bool:
    if not isinstance(data, dict): return False
    if "name" not in data or not isinstance(data["name"], str): return False
    if "game" not in data or not isinstance(data["game"], dict): return False
    required_game_keys = {"three_doors", "five_doors", "ten_doors"}
    if not required_game_keys.issubset(data["game"].keys()): return False
    if not all(isinstance(data["game"][k], (int, float)) for k in required_game_keys): return False
    return True

def import_all_players(folder_path: str) -> Dict[str, Dict[str, float]]:
    player_dict = {}
    if not os.path.isdir(folder_path):
        print(f"Folder not found: {folder_path}")
        return player_dict
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if is_valid_format(data):
                    player_dict[data["name"]] = data["game"]
                else:
                    print(f"Invalid player format: {filename}")
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {filename}")
    return player_dict

### Simulation ###

def gameshow_once(number_of_doors: int, probability: float) -> bool:
    game_list: List[bool] = set_game_list(number_of_doors)
    game_list = insert_random_true_value(game_list, number_of_doors)
    players_original_decision = random.randint(0, number_of_doors - 1)
    answer_tuple = return_2_doors(game_list, players_original_decision)
    final_answer = change_or_stay(answer_tuple, players_original_decision, probability)
    return did_the_player_win(final_answer, answer_tuple)

def simulate_player(name: str, game_probs: Dict[str, float], runs_per_game: int = 100) -> Dict:
    door_map = {"three_doors": 3, "five_doors": 5, "ten_doors": 10}
    results = {
        "name": name,
        "per_game": {},
        "overall": {"wins": 0, "losses": 0, "winrate": 0.0}
    }

    for game_name, prob in game_probs.items():
        n_doors = door_map[game_name]
        wins = 0
        for _ in range(runs_per_game):
            wins += 1 if gameshow_once(n_doors, prob) else 0
        losses = runs_per_game - wins
        winrate = wins / runs_per_game
        results["per_game"][game_name] = {"wins": wins, "losses": losses, "winrate": winrate}

        results["overall"]["wins"] += wins
        results["overall"]["losses"] += losses

    total = results["overall"]["wins"] + results["overall"]["losses"]
    results["overall"]["winrate"] = results["overall"]["wins"] / total if total else 0.0
    return results

def save_player_results(results: Dict, out_dir: str = "gameshow_results") -> None:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{results['name']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def print_summary(rankings: List[Dict]) -> None:
    print("\n=== Per-Player Summary (ranked by overall winrate) ===")
    for rank, r in enumerate(rankings, start=1):
        name = r["name"]
        o = r["overall"]
        print(f"{rank}. {name} — Overall: {o['wins']}W/{o['losses']}L  ({o['winrate']*100:.2f}%)")
        for g, stats in r["per_game"].items():
            print(f"   - {g}: {stats['wins']}W/{stats['losses']}L  ({stats['winrate']*100:.2f}%)")

### Parallel helpers (new) ###

def _init_worker():
    # Give each process its own RNG seed to avoid correlated streams
    random.seed(secrets.randbits(64))

def _simulate_wrapper(args):
    name, game, runs = args
    return simulate_player(name, game, runs)

### Entry ###
def main():
    player_dict = import_all_players("gameshow_players")
    if not player_dict:
        print("No players found.")
        return

    runs_per_game = 100_000_000  # same as before
    tasks = [(name, game, runs_per_game) for name, game in player_dict.items()]

    all_results: List[Dict] = []

    # One process per player (bounded by CPU cores)
    max_workers = min(len(tasks), os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=max_workers, initializer=_init_worker) as ex:
        future_map = {ex.submit(_simulate_wrapper, t): t[0] for t in tasks}
        for fut in as_completed(future_map):
            res = fut.result()          # may raise if the worker crashed
            save_player_results(res)    # save as each player finishes
            all_results.append(res)

    # Rank by overall winrate, tie-break by total wins
    rankings = sorted(
        all_results,
        key=lambda r: (r["overall"]["winrate"], r["overall"]["wins"]),
        reverse=True
    )
    print_summary(rankings)

if __name__ == "__main__":
    start: float = time.time()
    main()
    end: float = time.time()
    print("Execution time:", end - start, "seconds")