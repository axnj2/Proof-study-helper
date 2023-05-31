"""
This script is used to add new proofs to the proof list file. The format of the file is as follows:
    <number of proofs>
    <number of lines in proof> <proof number> <is latex> <has image>
    <proof text>
    ...
    <number of lines in proof> <proof number> <is latex> <has image>
    <proof text>
    ...
    ...

The script will first load the file into a dictionary, and then ask the user for a new proof. The user will input the
proof text, and the metadata (proof number, whether the proof is in latex, whether the proof has an image). The script
will then add the new proof to the dictionary, and write the dictionary back to the file.

If the user wants to add a proof that has already been added, the user should
delete the proof from the proof list file first.
"""
import display_module

from IO_module import str2bool
from IO_module import load_file

PROOF_FILE_NAME = "proof_lists/analyse1.txt"


def write_to_proof_file(proof_file_name: str, data: dict):
    with open(proof_file_name, 'w', encoding="utf-8") as f:
        f.write(f"{len(data)}\n")
        for proof_number in sorted(data.keys()):
            proof_text, score, stats, is_latex, has_answer_image = data[proof_number]
            f.write(f"{len(proof_text.splitlines())} {proof_number} {is_latex} {has_answer_image}\n")
            f.write(proof_text + "\n")


def ask_for_proof_text():
    # input raw string
    proof_text = ""
    new_proof_line = input("Enter your new proof question (return a single \"e\" to finish): \n") + "\n"
    while new_proof_line != "e\n":
        proof_text += new_proof_line
        new_proof_line = input() + "\n"
    proof_text = proof_text.strip()
    return proof_text


def ask_for_new_proof_question():
    proof_text = ask_for_proof_text()
    keep_proof = False
    while not keep_proof:
        display_module.display_math(proof_text)
        keep_proof = str2bool(input("Do you want to keep this proof? (y/n): "))
        if not keep_proof:
            proof_text = ask_for_proof_text()

    # input metadata
    has_image = str2bool(input("Does your proof have an image? (y/n): "))
    is_latex = str2bool(input("Is your proof in latex? (y/n): "))

    new_proof = [proof_text, None, None, is_latex, has_image]

    proof_number = int(input("Enter the proof number: "))

    return proof_number, new_proof


if __name__ == "__main__":
    working = True
    while working:
        proofs_and_scores = load_file(PROOF_FILE_NAME)
        proof_number, new_proof = ask_for_new_proof_question()

        proofs_and_scores[proof_number] = new_proof
        write_to_proof_file(PROOF_FILE_NAME, proofs_and_scores)

        working = str2bool(input("Do you want to add another proof? (y/n): "))
