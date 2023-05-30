"""
    Proof Study Helper a tool to help you study your proofs
    Copyright (C) 2023  Antoine Jacques-Jourion

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import random
import os
from statistics import mean
#from add_new_proof_to_list import load_file

try:
    import PIL
except:
    print("Il faut installer la bibliothèque pillow pour pouvoir utiliser le script avec les images.\n"
          "Essaye les commandes suivantes :\n"
          "python3 -m pip install --upgrade pip\n"
          "python3 -m pip install --upgrade Pillow\n")
    exit()

try:
    import matplotlib.pyplot as plt
except:
    print("Il faut installer la bibliothèque matplotlib pour pouvoir afficher les énoncés en LATEX.\n"
          "Essaye les commandes suivantes :\n"
          "python3 -m pip install --upgrade pip\n"
          "python3 -m pip install --upgrade matplotlib\n")
    exit()

# Constants for the algorithms choosing the next proof
FACTORS_FOR_WEIGHTS_ADJUSTING = {"0": 1.5, "1": 0.75, "2": 0.5, "3": 0.1}
MODES = {1: "random", 2: "new", 3: "stats"}
STARTING_WEIGHT = 1.0

# directories
PROOFS_DIRECTORY = "proof_lists/"
DATA_DIRECTORY = "data/"
IMAGE_DIRECTORY = "images/"

# constants for matplotlib LATEX display
FONT_SIZE = 12
FONT_COLOR = "black"
DISPLAY_SHAPE = (12, 2) # a rectangle, width, height in inches

# noinspection PyPep8
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


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "y")


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


def initialize_files_path(proof_list_name):
    # noinspection PyUnusedLocal
    def prepare_file(path: str) -> None:
        try:
            with open(path, "r") as f:
                pass
        except FileNotFoundError:
            with open(path, "w") as f:
                pass

    def new_file_name(proofs_file_name, data_name):
        return DATA_DIRECTORY + proofs_file_name[:-4] + "_" + data_name + ".txt"

    def initialize_stats_file(list_name: str):
        """
        :param list_name: the name of the proof file
        :return: stats and stats file path
        """
        stats_data_file_path = new_file_name(list_name, "history")

        prepare_file(stats_data_file_path)

        return stats_data_file_path

    def initialize_score_file(list_name: str) -> str:
        """
        creates the score file and data directory if they don't exist
        :return: score file relative path
        """
        score_file_relative_path = new_file_name(list_name, "scores")

        prepare_file(score_file_relative_path)

        return score_file_relative_path

    if not os.path.isdir(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)

    proof_list_path = PROOFS_DIRECTORY + proof_list_name
    scores_file_path = initialize_score_file(proof_list_name)
    stats_file_path = initialize_stats_file(proof_list_name)
    images_directory_path = IMAGE_DIRECTORY + proof_list_name[:-4] + "/"

    return proof_list_path, scores_file_path, stats_file_path, images_directory_path

def load_file(proof_file_name) -> dict:
    proofs_and_scores = dict()  # key: proof number, value: [proof text, score, stats, is_latex, has_answer_image]

    with open(proof_file_name, 'r', encoding="utf-8") as f:
        number_of_proofs = int(f.readline())
        for i in range(number_of_proofs):
            header = f.readline().split()
            number_of_lines_in_proof, proof_number, is_latex, has_answer_image = int(header[0]), int(header[1]), str2bool(
                header[2]), str2bool(header[3])
            proof_text = r""
            for j in range(number_of_lines_in_proof):
                proof_text += f.readline()
            proof_text = proof_text.strip("\n")
            proofs_and_scores[proof_number] = [proof_text, None, None, is_latex, has_answer_image]

    return proofs_and_scores


def initialize_from_files(proofs_file, scores_file, stats_file):
    """
    Proof and scores dict format :
    key: proof number, value: [proof text, score, stats, is_latex, has_answer_image]

    :param proofs_file: path to the file containing the proofs
    :param scores_file: path to the file containing the scores
    :param stats_file: path to the file containing the stats
    :return: proofs_and_scores dictionary
    """

    # check if the file is in the new encoding or the legacy one
    proofs_file_format = "legacy"
    with open(proofs_file, "r", encoding="utf-8") as f:
        first_line = f.readline()
        if first_line.strip().isnumeric():
            proofs_file_format = "new"

    if proofs_file_format == "legacy":
        with open(proofs_file, "r", encoding="utf-8") as f:
            proofs_prompt = f.read().splitlines()
            new_proofs_and_scores = dict()
            for proof in proofs_prompt:
                number, prompt = proof.split("°")
                number = int(number)
                new_proofs_and_scores[number] = [prompt, None, None, None, None]

    elif proofs_file_format == "new":
        new_proofs_and_scores = load_file(proofs_file)

    with open(scores_file, "r", encoding="utf-8") as f:
        raw_scores = f.read().splitlines()
        for raw_score in raw_scores:
            number, score = raw_score.split("|")
            number = int(number)
            score = float(score)
            new_proofs_and_scores[number][1] = score

    # add starting score if there is no score for that demo
    for i in new_proofs_and_scores:
        if new_proofs_and_scores[i][1] is None:
            new_proofs_and_scores[i][1] = 1.0

    with open(stats_file, "r", encoding="utf-8") as f:
        raw_stats = f.read().splitlines()
        for raw_stat in raw_stats:
            number, stat = raw_stat.split("|")
            number = int(number)
            stat = list(map(int, stat.split()))
            new_proofs_and_scores[number][2] = stat

    # add empty list if it's a new proof
    for i in new_proofs_and_scores:
        if new_proofs_and_scores[i][2] is None:
            new_proofs_and_scores[i][2] = []

    return new_proofs_and_scores


def write_file(proofs_and_scores: dict, score_path: str, stats_path: str) -> None:
    sorted_proof_numbers = sorted(list(proofs_and_scores.keys()))
    with open(score_path, "w") as f:
        output = ""
        for i in sorted_proof_numbers:
            output += str(i) + "|" + str(proofs_and_scores[i][1]) + "\n"
        output = output[:-1]
        f.write(output)

    with open(stats_path, "w") as f:
        output = ""
        for i in sorted_proof_numbers:
            output += str(i) + "|"
            for result in proofs_and_scores[i][2]:
                output += str(result) + " "
            output += "\n"
        output = output[:-1]
        f.write(output)


def choose_with_weights(curent_proofs_and_scores):
    sorted_proof_numbers = sorted(list(curent_proofs_and_scores.keys()))
    probability_distribution = [
        curent_proofs_and_scores[i][1] for i in sorted_proof_numbers
    ]
    return random.choices(sorted_proof_numbers, weights=probability_distribution, k=1)[0]


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
    elif MODES[current_mode] == "random":
        next_proof = choose_with_weights(curent_proofs_and_scores)

    return next_proof, current_mode


def initialize_mode():
    user_input = int(input(
        "Que veux tu faire ?\n"
        "   1 : Faire des démonstrations aléatoirement\n"
        "   2 : Faire des démonstrations pas encore faites\n"
        "   3 : (ne fonctionne pas pour l'instant) Voir les statistiques de ma progression\n"
        "Input : "
    ))
    if user_input not in MODES:
        raise Exception(f'"{user_input}" is not one of the supported actions')
    return user_input


# noinspection SpellCheckingInspection
def stats_interface(proofs_and_scores):  # currently broken
    def precise_stats(maxs, moyennes):
        for proof_number in range(len(proofs_and_scores)):
            render_proof(proof_number + 1, proofs_and_scores, False)
            if moyennes[proof_number] != -1:
                print(f"Elle a une moyenne de {moyennes[proof_number] * 20}/{20}")
                print(f"Elle a un max de {maxs[proof_number]}")
                print(f"Elle a été faite {len(proofs_and_scores[proof_number][2])} fois")
                print(f"Les notes sont {proofs_and_scores[proof_number][2]}")
                print(f"poids actuel : {proofs_and_scores[proof_number + 1][1]}")
            else:
                print("Pas encore faite")

    def get_normalised_success_score(choice):
        min_value = 1 / FACTORS_FOR_WEIGHTS_ADJUSTING["0"]
        max_value = 1 / FACTORS_FOR_WEIGHTS_ADJUSTING["3"]
        current_value = 1 / FACTORS_FOR_WEIGHTS_ADJUSTING[str(choice)]
        # min max scaling
        normalized_value = (current_value - min_value) / (max_value - min_value)
        return normalized_value

    averages = []
    maxs = []
    averages_excluding_not_done_yet = []
    for proof in proofs_and_scores:
        proof_result_history = proofs_and_scores[proof][2]
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
          f" {round((sum(averages_excluding_not_done_yet) / len(averages_excluding_not_done_yet)) * 20, 2)}/20"
          f"sur celles que tu as déjà faites")

    total_score = sum(averages_excluding_not_done_yet) / len(averages)

    print(f"Ton score total est de {round(total_score * 20, 2)}/20\n")

    continue_status = int(input(
        "Que veux tu faire ? \n"
        "   0 : Voir Des informations sur chaque démo\n"
        "   1 : Revenir en arrière\n"
        "input : "
    ))
    if continue_status == 0:
        precise_stats(maxs, averages)


def display_math(latex_code):
    plt.figure(figsize=DISPLAY_SHAPE)
    ax = plt.subplot()
    plt.subplots_adjust(left=0)
    ax.axis('off')
    ax.text(0, 0, latex_code, fontsize=FONT_SIZE, color=FONT_COLOR)
    plt.show()


# noinspection PyPep8
def render_proof(current_proof, proofs_and_scores, image_directory, display_image=True):
    # noinspection PySimplifyBooleanCheck
    if proofs_and_scores[current_proof][4] == True:  # has_image = True
        solution_image_path = image_directory + str(current_proof) + ".png"
        solution_image = PIL.Image.open(solution_image_path)

        # show the prompt
        display_math(proofs_and_scores[current_proof][0])
        # if proofs_and_scores[current_proof][3] == True: # has_latex = True
        #     display_math(proofs_and_scores[current_proof][0])
        # else:
        #     print("\n\033[91m\033[1m" + proofs_and_scores[current_proof][0] + "\033[0m")

        # show the solution
        if display_image:
            solution_image.show()
        else:
            print(f"Réponse: {os.path.abspath(solution_image_path)}")

    else:
        print("\n\033[91m\033[1m" + proofs_and_scores[current_proof][0] + "\033[0m")


if __name__ == "__main__":
    print(ASCII_ART)

    proof_list_name = choose_proof_list()
    proof_list_path, scores_file_path, stats_file_path, images_directory_path = initialize_files_path(proof_list_name)
    proofs_and_scores = initialize_from_files(proof_list_path, scores_file_path, stats_file_path)

    mode = initialize_mode()
    while mode == 3:
        stats_interface(proofs_and_scores)
        mode = initialize_mode()

    while True:
        proofs_and_scores = initialize_from_files(proof_list_path, scores_file_path, stats_file_path)

        current_proof, mode = choose_next_proof(mode, proofs_and_scores)

        render_proof(current_proof, proofs_and_scores, images_directory_path)
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
        proofs_and_scores[current_proof][2].append(success_assessment)

        write_file(proofs_and_scores, scores_file_path, stats_file_path)
