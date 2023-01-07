from pprint import pprint
import random


def initialize():
    with open("liste_des_demo.txt", "r", encoding="utf-8") as f:
        demos = f.read().splitlines()
        demo_dict = dict()
        for number, demo in enumerate(demos, 1):
            demo_dict[number] = [demo, ]

    with open("demo-scores.txt", "r") as f:
        scores = map(float, f.read().splitlines())
        for number, score in enumerate(scores, 1):
            demo_dict[number].append(score)

    return demo_dict

def write_file(data: dict) -> None:
    with open("demo-scores.txt", "w") as f:
        for i in range(1,40):
            f.write(str(data[i][1]) + "\n")
        f.write(str(data[40][1]))


result_weigths = {"0":1.5, "1":0.75, "2":0.5, "3":0.1}
studying = True
while studying:
    dictionnary_of_demo = initialize()

    probability = [dictionnary_of_demo[i][1] for i in range(1,41)]
    todo = random.choices(list(range(1, 41)), weights=probability, k=1)[0]

    print(dictionnary_of_demo[todo][0])
    result = input("Démo réussite ? (0=pas du tout, 1=quelques erreure, 2=presque parfait et 3=prêt pour l'examen)\n")

    dictionnary_of_demo[todo][1] *= result_weigths[result]
    print("nouveau poids :", dictionnary_of_demo[todo][1])

    write_file(dictionnary_of_demo)
