import torch
import torch.nn as nn
import torch.optim as optim

from vocab_demo import build_vocab, encode_text
from classifier_demo import SimpleSentimentClassifier


LABEL_TO_ID = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}


if __name__ == "__main__":
    titles = [
        "Peace talks resume between two countries",
        "Missile strikes hit border region",
        "Foreign ministers meet in Brussels"
    ]

    labels = [
        "positive",
        "negative",
        "neutral"
    ]

    vocab = build_vocab(titles)

    encoded_examples = []

    for title in titles:
        encoded = encode_text(title, vocab, max_len=8)
        encoded_examples.append(encoded)

    input_ids = torch.tensor(encoded_examples, dtype=torch.long)

    label_ids = []

    for label in labels:
        label_id = LABEL_TO_ID[label]
        label_ids.append(label_id)

    y_true = torch.tensor(label_ids, dtype=torch.long)

    model = SimpleSentimentClassifier(
        vocab_size=len(vocab),
        embedding_dim=10,
        num_classes=3
    )

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    print("Labels réels :")
    print(y_true)

    logits_before = model(input_ids)
    loss_before = criterion(logits_before, y_true)

    print("Loss avant entraînement :")
    print(loss_before.item())

    optimizer.zero_grad()

    logits = model(input_ids)

    loss = criterion(logits, y_true)

    loss.backward()

    optimizer.step()

    logits_after = model(input_ids)
    loss_after = criterion(logits_after, y_true)

    print("Loss après une étape :")
    print(loss_after.item())

    probabilities = torch.softmax(logits_after, dim=1)
    predicted_classes = torch.argmax(probabilities, dim=1)

    print("Probabilités après entraînement :")
    print(probabilities)

    print("Classes prédites après entraînement :")
    print(predicted_classes)