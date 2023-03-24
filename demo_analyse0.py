import random
import os
from statistics import mean


FACTORS_FOR_WEIGHTS_ADJUSTING = {"0": 1.5, "1": 0.75, "2": 0.5, "3": 0.1}
MODES = {1: "random", 2: "new", 3: "stats"}
PROOFS_DIRECTORY = "proof_lists/"
DATA_DIRECTORY = "data/"
STARTING_WEIGHT = 1.0
ASCII_ART = r"""
 ____                          ___      ____    __                __              __  __          ___                            
/\  _`\                      /'___\    /\  _`\ /\ \__            /\ \            /\ \/\ \        /\_ \                           
\ \ \L\ \_ __   ___     ___ /\ \__/    \ \,\L\_\ \ ,_\  __  __   \_\ \  __  __   \ \ \_\ \     __\//\ \    _____      __   _ __  
 \ \ ,__/\`'__\/ __`\  / __`\ \ ,__\    \/_\__ \\ \ \/ /\ \/\ \  /'_` \/\ \/\ \   \ \  _  \  /'__`\\ \ \  /\ '__`\  /'__`\/\`'__\
  \ \ \/\ \ \//\ \L\ \/\ \L\ \ \ \_/      /\ \L\ \ \ \_\ \ \_\ \/\ \L\ \ \ \_\ \   \ \ \ \ \/\  __/ \_\ \_\ \ \L\ \/\  __/\ \ \/ 
   \ \_\ \ \_\\ \____/\ \____/\ \_\       \ `\____\ \__\\ \____/\ \___,_\/`____ \   \ \_\ \_\ \____\/\____\\ \ ,__/\ \____\\ \_\ 
    \/_/  \/_/ \/___/  \/___/  \/_/        \/_____/\/__/ \/___/  \/__,_ /`/___/> \   \/_/\/_/\/____/\/____/ \ \ \/  \/____/ \/_/ 
                                                                            /\___/                           \ \_\               
                                                                            \/__/                             \/_/               
"""


def choose_proof_list():
    def discover_proofs_lists():
        with os.scandir(PROOFS_DIRECTORY) as proof_files:
            return [file.name for file in proof_files]

    list_of_proofs_lists = discover_proofs_lists()

    print("Choisissez les démos à étudier :")
    print("\n".join(list(f"{i} : {name[:-4]}" for i, name in enumerate(list_of_proofs_lists))))
    proof_list_choice = int(input(
        "Input : "
    ))
    return list_of_proofs_lists[proof_list_choice]


def prepare_file(path: str, fill: str, number_of_lines: int) -> None:
    try:
        with open(path, "r") as f:
            pass
    except FileNotFoundError:
        with open(path, "w") as f:
            f.write((fill + "\n") * (number_of_lines - 1) + fill)


def new_file_name(proofs_file_name, data_name):
    return DATA_DIRECTORY + proofs_file_name[:-4] + "_" + data_name + ".txt"


def initialize_score_file(list_name: str) -> str:
    """
    creates the score file and data directory if they don't exist
    :return: score file relative path
    """
    if not os.path.isdir(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)

    score_file_relative_path = new_file_name(list_name, "scores")
    with open(PROOFS_DIRECTORY + list_name, "r") as f:
        number_of_demo = len(f.readlines())

    prepare_file(score_file_relative_path, str(STARTING_WEIGHT), number_of_demo)

    return score_file_relative_path


def get_stats(list_name: str, number_of_proofs) -> (list, str):
    """
    :param list_name: the name of the proof file
    :return: stats and stats file path
    """
    def create_stats_file(file_path):
        with open(file_path, "w") as f:
            f.write(" \n" * (len(proofs_and_scores)))

    stats_data_file_path = new_file_name(list_name, "history")

    prepare_file(stats_data_file_path, " ", number_of_proofs)

    with open(stats_data_file_path, 'r') as f:
        stats = f.read().splitlines()

    stats = [list(map(int, stat.split())) for stat in stats]
    return stats, stats_data_file_path


def initialize_from_file(proofs_file, scores_file):
    with open(proofs_file, "r", encoding="utf-8") as f:
        proofs_prompt = f.read().splitlines()
        new_proofs_and_scores = dict()
        for proof_number, proof in enumerate(proofs_prompt, start=1):
            new_proofs_and_scores[proof_number] = [proof]

    with open(scores_file, "r") as f:
        scores = map(float, f.read().splitlines())
        for proof_number, score in enumerate(scores, 1):
            new_proofs_and_scores[proof_number].append(score)

    return new_proofs_and_scores


def write_file(proofs_and_scores: dict, file_path: str) -> None:
    with open(file_path, "w") as f:
        for i in range(1, len(proofs_and_scores)):
            f.write(str(proofs_and_scores[i][1]) + "\n")
        f.write(str(proofs_and_scores[len(proofs_and_scores)][1]))


def write_stats(file_path: str, demo: int, score: str) -> None:
    with open(file_path, 'r') as file:
        data = file.readlines()

    data[demo - 1] = data[demo - 1].strip() + " " + score + "\n"

    with open(file_path, 'w') as file:
        file.writelines(data)


def choose_with_weights(curent_proofs_and_scores):
    probability_distribution = [
        curent_proofs_and_scores[i][1] for i in range(1, len(curent_proofs_and_scores) + 1)
    ]
    return random.choices(list(range(1, len(curent_proofs_and_scores) + 1)), weights=probability_distribution, k=1)[0]


def choose_only_new(curent_proofs_and_scores):
    new_proofs = []
    for i in range(1, len(curent_proofs_and_scores) + 1):
        if curent_proofs_and_scores[i][1] == 1.0:
            new_proofs.append(i)
    if new_proofs:
        return random.choice(new_proofs), len(new_proofs)
    else:
        return None, None


def choose_next_proof(current_mode, curent_proofs_and_scores):
    if MODES[current_mode] == "new":
        next_proof, number_of_new = choose_only_new(curent_proofs_and_scores)
        if next_proof is None:
            print("Tu as fait toutes les démos au moins une fois, mode changé vers random avec le poids.")
            current_mode = 1
        else:
            print(f"il reste {number_of_new} démonstration(s) pas encore faites")
    if MODES[current_mode] == "random":
        next_proof = choose_with_weights(curent_proofs_and_scores)

    return next_proof, current_mode


def initialize_mode():
    user_input = int(input(
        "Que veux tu faire ?\n"
        "   1 : Faire des démonstrations aléatoirement\n"
        "   2 : Faire des démonstrations pas encore faites\n"
        "   3 : Voir les statistiques de ma progression\n"
        "Input : "
    ))
    if user_input not in MODES:
        raise Exception(f'"{user_input}" is not one of the supported actions')
    return user_input


def stats_interface(proofs_and_scores):
    def precise_stats(maxs, moyennes):
        for proof_number in range(len(stats_data)):
            print(f"\n\033[91m\033[1m" + proofs_and_scores[proof_number + 1][0] + "\033[0m")
            if moyennes[proof_number] != -1:
                print(f"Elle a une moyenne de {moyennes[proof_number]*20}/{20}")
                print(f"Elle a un max de {maxs[proof_number]}")
                print(f"Elle a été faite {len(stats_data[proof_number])} fois")
                print(f"Les notes sont {stats_data[proof_number]}")
                print(f"poids actuel : {proofs_and_scores[proof_number+1][1]}")
            else:
                print("Pas encore faite")

    def get_normalised_success_score(choice):
        min_value = 1/FACTORS_FOR_WEIGHTS_ADJUSTING["0"]
        max_value = 1/FACTORS_FOR_WEIGHTS_ADJUSTING["3"]
        current_value = 1/FACTORS_FOR_WEIGHTS_ADJUSTING[str(choice)]
        # min max scaling
        normalized_value = (current_value - min_value) / (max_value-min_value)
        return normalized_value

    averages = []
    maxs = []
    averages_excluding_not_done_yet = []
    for proof_result_history in stats_data:
        success_scores = list(map(get_normalised_success_score, proof_result_history))
        if len(success_scores) != 0:
            maxs.append(max(success_scores))
            averages.append(mean(success_scores))
            averages_excluding_not_done_yet.append(mean(success_scores))
        else:
            maxs.append(None)
            averages.append(-1)

    if len(averages_excluding_not_done_yet) == 0:
        print("Tu n'as pas encore fait de démonstration, les stats ne sont pas encore disponibles !")
        return

    print("\n-----------------------------------------------\n\n")
    print(f"Tu as fait {len([m for m in averages if m != -1])} démonstrations sur {len(proofs_and_scores)}")
    print(f"Ta moyenne est de "
          f"{round((sum(averages_excluding_not_done_yet) / len(averages_excluding_not_done_yet))*20, 2)}/20"
          f"sur celles que tu as déjà faites")

    total_score = sum(averages_excluding_not_done_yet)/ len(averages)

    print(f"Ton score total est de {round(total_score*20, 2)}/20\n")

    continue_status = int(input(
        "Que veux tu faire ? \n"
        "   0 : Voir Des informations sur chaque démo\n"
        "   1 : Revenir en arrière\n"
        "input : "
    ))
    if continue_status == 0:
        precise_stats(maxs, averages)


if __name__ == "__main__":
    print(ASCII_ART)

    proof_list_name = choose_proof_list()
    proof_list_path = PROOFS_DIRECTORY + proof_list_name
    scores_file_path = initialize_score_file(proof_list_name)
    mode = initialize_mode()
    proofs_and_scores = initialize_from_file(proof_list_path, scores_file_path)
    stats_data, stats_file_path = get_stats(proof_list_name, len(proofs_and_scores))

    while mode == 3:
        stats_interface(proofs_and_scores)
        mode = initialize_mode()

    while True:
        proofs_and_scores = initialize_from_file(proof_list_path, scores_file_path)

        current_proof, mode = choose_next_proof(mode, proofs_and_scores)

        print("\n\033[91m\033[1m" + proofs_and_scores[current_proof][0] + "\033[0m")
        success_assessment = input(
            "Démo réussie ? \n"
            "   0 : Pas du tout\n"
            "   1 : Quelques erreurs\n"
            "   2 : Presque parfait\n"
            "   3 : Prêt pour l'examen\n"
            "   4 : S'arrêter ici\n"
            "input : "
        )
        if success_assessment == "4":
            break
        while success_assessment not in FACTORS_FOR_WEIGHTS_ADJUSTING:
            success_assessment = input("Input invalide, réessaye : ")

        proofs_and_scores[current_proof][1] *= FACTORS_FOR_WEIGHTS_ADJUSTING[success_assessment]
        print("Nouveau poids :", proofs_and_scores[current_proof][1])

        write_file(proofs_and_scores, scores_file_path)
        write_stats(stats_file_path, current_proof, success_assessment)
