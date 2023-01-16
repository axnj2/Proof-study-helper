from tkinter import *
from tkinter import ttk
import backend

scores_file_location, mode = backend.initialize_variables()
proof_number, proof_text, mode = backend.next_proof(mode)


def update(result):
    backend.update_score(proof_number, result)
    proof_score.set(backend.get_score(proof_number))


def not_good():
    update(0)


def good():
    update(1)


def perfect():
    update(3)


def next_proof():
    global proof_number, proof_text, mode
    proof_number, proof_text, mode = backend.next_proof(mode)
    proof_display.set(proof_text)
    proof_score.set(backend.get_score(proof_number))


root = Tk()
root.title("Proofs training helper")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Démo à démontrer:").grid(column=1, row=1, sticky=W)

proof_display = StringVar()
proof_display.set(proof_text)
ttk.Label(mainframe, textvariable=proof_display).grid(column=0, row=2, columnspan=3)


ttk.Button(mainframe, text="not good", command=not_good).grid(column=1, row=3, sticky=E)
ttk.Button(mainframe, text="good", command=good).grid(column=2, row=3, )
ttk.Button(mainframe, text="perfect", command=perfect).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="current score on this proofs :").grid(column=1, row=4, sticky=E)

proof_score = StringVar()
proof_score.set(str(backend.get_score(proof_number)))
ttk.Label(mainframe, textvariable=proof_score).grid(column=2, row=4, sticky=W)
ttk.Button(mainframe, text="next", command=next_proof).grid(column=3, row=4, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)


root.mainloop()