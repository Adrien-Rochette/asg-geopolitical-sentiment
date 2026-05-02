import re


def tokenize(text: str) -> list[str]:
    """
    Transforme une phrase en liste de mots simples.

    Étapes :
    1. mettre en minuscules ;
    2. enlever la ponctuation ;
    3. découper la phrase en mots.
    """

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    tokens = text.split()

    return tokens


if __name__ == "__main__":
    title = "Peace talks resume between two countries"

    tokens = tokenize(title)

    print("Titre original :")
    print(title)

    print("Tokens :")
    print(tokens)