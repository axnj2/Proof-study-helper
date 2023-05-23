
PROOF_FILE_NAME = "test_proofs.txt"

def load_file(proof_file_name) -> dict:
    proofs_and_scores = dict() # key: proof number, value: [proof text, score, stats, is_latex, has_answer_image]

    with open(proof_file_name, 'r') as f:
        number_of_proofs = int(f.readline())
        for i in range(number_of_proofs):
            header = f.readline().split()
            number_of_lines_in_proof, proof_number, is_latex, has_answer_image = int(header[0]), int(header[1]), bool(header[2]), bool(header[3])
            proof_text = r""
            for j in range(number_of_lines_in_proof):
                proof_text += f.readline()
            proof_text = proof_text.strip()
            proofs_and_scores[proof_number] = [proof_text, None, None, is_latex, has_answer_image]

    return proofs_and_scores


def write_to_proof_file(proof_file_name: str, data: dict):
    with open(proof_file_name, 'w') as f:
        f.write(f"{len(data)}\n")
        for proof_number in data.keys():
            proof_text, score, stats, is_latex, has_answer_image = data[proof_number]
            f.write(f"{len(proof_text.splitlines())} {proof_number} {is_latex} {has_answer_image}\n")
            f.write(proof_text + "\n")


def ask_for_new_proof_question():
    # input raw string
    proof_text = input("Enter your new proof question: ") # TODO : only works for one line at the moment needs to be fixed
    has_image = input("Does your proof have an image? (y/n): ")
    if has_image == "y":
        has_image = True
    else:
        has_image = False
    is_latex = input("Is your proof in latex? (y/n): ")
    if is_latex == "y":
        is_latex = True
    else:
        is_latex = False
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

        working = input("Do you want to add another proof? (y/n): ")
        if working == "y":
            working = True
        else:
            working = False