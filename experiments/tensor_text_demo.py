import torch

from vocab_demo import build_vocab, encode_text


if __name__ == "__main__":
    titles = [
        "Peace talks resume between two countries",
        "Missile strikes hit border region",
        "Foreign ministers meet in Brussels"
    ]

    vocab = build_vocab(titles)

    examples = [
        "Peace talks resume",
        "Missile strikes hit border region",
        "Foreign ministers meet in Brussels"
    ]

    encoded_examples = []

    for example in examples:
        encoded = encode_text(example, vocab, max_len=8)
        encoded_examples.append(encoded)

    print("Exemples encodés :")
    print(encoded_examples)

    input_ids = torch.tensor(encoded_examples, dtype=torch.long)

    print("Tenseur input_ids :")
    print(input_ids)

    print("Shape du tenseur :")
    print(input_ids.shape)

    print("Type du tenseur :")
    print(input_ids.dtype)