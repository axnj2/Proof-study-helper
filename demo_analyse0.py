import random

FACTORS_FOR_WEIGHTS_ADJUSTING = {"0": 1.5, "1": 0.75, "2": 0.5, "3": 0.1}
MODES = {1: "random", 2: "new"}
PROOFS_FILE_LOCATION = "demos_analyse0.txt"
LEGACY_SCORES_FILE_LOCATION = "demo-scores.txt"  # to avoid breaking compatibility with older files name


def initialize_proofs_and_scores(proofs_file_location):
    with open(proofs_file_location, "r", encoding="utf-8") as f:
        proofs_prompt = f.read().splitlines()
        new_proofs_and_scores = dict()
        for proof_number, proof in enumerate(proofs_prompt, start=1):
            new_proofs_and_scores[proof_number] = [proof]

    with open(scores_file_location, "r") as f:
        scores = map(float, f.read().splitlines())
        for proof_number, score in enumerate(scores, 1):
            new_proofs_and_scores[proof_number].append(score)

    return new_proofs_and_scores


def write_file(proofs_and_scores: dict) -> None:
    with open(scores_file_location, "w") as f:
        for i in range(1, len(proofs_and_scores)):
            f.write(str(proofs_and_scores[i][1]) + "\n")
        f.write(str(proofs_and_scores[len(proofs_and_scores)][1]))


def choose_with_weights():
    probability_distribution = [
        float(proofs_and_scores[i][1]) for i in range(1, len(proofs_and_scores) + 1)
    ]
    return int(random.choices(list(range(1, len(proofs_and_scores) + 1)), weights=probability_distribution, k=1))


def choose_only_new():
    new_proofs = []
    for i in range(1, len(proofs_and_scores) + 1):
        if proofs_and_scores[i][1] == 1.0:
            new_proofs.append(i)
    if new_proofs:
        return random.choice(new_proofs), len(new_proofs)
    else:
        return None, None


def choose_next_proof(current_mode):
    if MODES[current_mode] == "new":
        next_proof, number_of_new = choose_only_new()
        if next_proof is None:
            print("Tu as fait toutes les démos au moins une fois, mode changé vers random avec le poids.")
            current_mode = "random"
        else:
            print(f"il reste {number_of_new} démonstration(s) pas encore faites")
    elif MODES[current_mode] == "random":
        next_proof = choose_with_weights()

    return next_proof, current_mode


def initialize_score_file(proofs_file_location):
    try:
        with open(LEGACY_SCORES_FILE_LOCATION, "r"):
            pass
        score_file = LEGACY_SCORES_FILE_LOCATION
    except FileNotFoundError:
        score_file = proofs_file_location.strip(".txt") + "_scores.txt"
        try:
            with open(score_file, "r"):
                pass
        except FileNotFoundError:
            with open(proofs_file_location, "r") as f:
                number_of_demo = len(f.readlines())
            with open(score_file, "w") as f:
                f.write("1.0\n"*(number_of_demo-1) + "1.0")
    return score_file


def initialize_mode():
    user_input = int(input(
        "Quel mode voulez-vous ?\n"
        "   1 : Au hasard avec des chances d'être choisie ajusté en fonction de la réussite\n"
        "   2 : Uniquement les nouvelles (ne fonctionne que si les démos n'ont pas encore toutes été faites)\n"
        "input : "
    ))
    if user_input not in MODES:
        raise Exception(f'"{user_input}" is not one of the supported modes')
    return user_input


scores_file_location = initialize_score_file(PROOFS_FILE_LOCATION)
mode = initialize_mode()
studying = True
while studying:
    proofs_and_scores = initialize_proofs_and_scores(PROOFS_FILE_LOCATION)

    current_proof, mode = choose_next_proof(mode)

    print(proofs_and_scores[current_proof][0])
    success_assessment = input(
        "Démo réussie ? (0=pas du tout, 1=quelques erreurs, 2=presque parfait et 3=prêt pour l'examen)\n"
    )

    proofs_and_scores[current_proof][1] *= FACTORS_FOR_WEIGHTS_ADJUSTING[success_assessment]
    print("nouveau poids :", proofs_and_scores[current_proof][1])

    write_file(proofs_and_scores)
