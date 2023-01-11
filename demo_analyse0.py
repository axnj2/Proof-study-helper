import random

AJUSTING_WEIGHTS = {"0": 1.5, "1": 0.75, "2": 0.5, "3": 0.1}
MODES = {1: "random", 2: "new"}
DEMOS_FILE = "demos_analyse0.txt"
LEGACY_SCORES_FILE = "demo-scores.txt" # to avoid breaking compatibility with older files name


def initialize_dictionnary():
    with open(DEMOS_FILE, "r", encoding="utf-8") as f:
        demos = f.read().splitlines()
        demo_dict = dict()
        for number, demo in enumerate(demos, 1):
            demo_dict[number] = [demo, ]

    with open(score_file, "r") as f:
        scores = map(float, f.read().splitlines())
        for number, score in enumerate(scores, 1):
            demo_dict[number].append(score)

    return demo_dict


def write_file(data: dict) -> None:
    with open(score_file, "w") as f:
        for i in range(1, len(data)):
            f.write(str(data[i][1]) + "\n")
        f.write(str(data[len(data)][1]))


def choose_random_with_weights():
    probability = [float(dictionnary_of_demo[i][1]) for i in range(1, len(dictionnary_of_demo) + 1)]
    return random.choices(list(range(1, len(dictionnary_of_demo) + 1)), weights=probability, k=1)[0]


def choose_random_only_new():
    new_demos = []
    for i in range(1, len(dictionnary_of_demo) + 1):
        if dictionnary_of_demo[i][1] == 1.0:
            new_demos.append(i)
    if new_demos:
        return random.choice(new_demos), len(new_demos)
    else:
        return None, None


def initialize_modes():
    user_input = int(input("Quel mode veux-tu ?\n"
                           "   1 : Au hasard avec des chances d'être choisie ajusté en fonction de la réussite\n"
                           "   2 : Uniquement les nouvelles (ne fonctionne que si les démos n'ont pas encore toutes été faites)\n"
                           "input : "))
    return MODES[user_input]


def initialize_score_file():
    try:
        with open(LEGACY_SCORES_FILE, "r") as f:
            pass
        score_file = LEGACY_SCORES_FILE
    except FileNotFoundError:
        score_file = DEMOS_FILE.strip(".txt") + "_scores.txt"
        try:
            with open(score_file, "r") as f:
                pass
        except FileNotFoundError:
            with open(DEMOS_FILE, "r") as f:
                number_of_demo = len(f.readlines())
            with open(score_file, "w") as f:
                f.write("1.0\n"*(number_of_demo-1) + "1.0")
    return score_file


score_file = initialize_score_file()
mode = initialize_modes()
studying = True
while studying:
    dictionnary_of_demo = initialize_dictionnary()

    if mode == "new":
        todo, number_of_new = choose_random_only_new()
        if todo is None:
            print("Tu as fait toutes les démos au moins une fois, mode changé vers random avec le poids.")
            mode = "random"
        else:
            print(f"il reste {number_of_new} démonstration pas encore faites")
    if mode == "random":
        todo = choose_random_with_weights()

    print(dictionnary_of_demo[todo][0])
    result = input("Démo réussite ? (0=pas du tout, 1=quelques erreure, 2=presque parfait et 3=prêt pour l'examen)\n")

    dictionnary_of_demo[todo][1] *= AJUSTING_WEIGHTS[result]
    print("nouveau poids :", dictionnary_of_demo[todo][1])

    write_file(dictionnary_of_demo)
