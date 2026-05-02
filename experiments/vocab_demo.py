from text_processing import tokenize


PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"


def build_vocab(texts: list[str]) -> dict[str, int]:
    """
    Construit un dictionnaire mot -> identifiant numérique.
    """

    vocab = {
        PAD_TOKEN: 0,
        UNK_TOKEN: 1
    }

    for text in texts:
        tokens = tokenize(text)

        for token in tokens:
            # TODO :
            # si le token n'est pas déjà dans vocab,
            # ajoute-le avec un nouvel identifiant
            if token not in vocab:
                vocab[token] = len(vocab)

    return vocab


def encode_text(text: str, vocab: dict[str, int], max_len: int = 8) -> list[int]:
    """
    Transforme une phrase en liste d'identifiants numériques
    de longueur fixe.

    Si la phrase est trop longue, on la coupe.
    Si elle est trop courte, on ajoute du padding.
    """

    tokens = tokenize(text)

    ids = []

    for token in tokens:
        token_id = vocab.get(token, vocab[UNK_TOKEN])
        ids.append(token_id)

    # Cas 1 : phrase trop longue
    ids = ids[:max_len]

    # Cas 2 : phrase trop courte
    while len(ids) < max_len:
        ids.append(vocab[PAD_TOKEN])

    return ids


if __name__ == "__main__":
    titles = [
        "Peace talks resume between two countries",
        "Missile strikes hit border region",
        "Foreign ministers meet in Brussels"
    ]

    vocab = build_vocab(titles)

    print("Vocabulaire :")
    print(vocab)

    example = "Peace talks resume between two countries after long negotiations"

    encoded = encode_text(example, vocab, max_len=8)
    
    print("Longueur de la phrase encodée :")
    print(len(encoded))

    print("Phrase :")
    print(example)

    print("Phrase encodée :")
    print(encoded)