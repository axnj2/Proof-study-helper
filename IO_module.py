def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "y")


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
