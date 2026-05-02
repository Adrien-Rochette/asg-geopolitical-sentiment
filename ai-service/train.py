import csv
import torch
import torch.nn as nn
import torch.optim as optim

from vocab_demo import build_vocab, encode_text
from model import SentimentClassifier


LABEL_TO_ID = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}


def load_data(path: str):
    texts = []
    labels = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            texts.append(row["text"])
            labels.append(row["label"])

    return texts, labels


def main():
    texts, labels = load_data("data.csv")

    vocab = build_vocab(texts)

    encoded_examples = []

    for text in texts:
        encoded = encode_text(text, vocab, max_len=12)
        encoded_examples.append(encoded)

    input_ids = torch.tensor(encoded_examples, dtype=torch.long)

    label_ids = []

    for label in labels:
        label_ids.append(LABEL_TO_ID[label])

    y_true = torch.tensor(label_ids, dtype=torch.long)

    model = SentimentClassifier(
        vocab_size=len(vocab),
        embedding_dim=32,
        hidden_dim=16,
        num_classes=3
    )

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    num_epochs = 100

    for epoch in range(num_epochs):
        model.train()

        optimizer.zero_grad()

        logits = model(input_ids)
        loss = criterion(logits, y_true)

        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch + 1}/{num_epochs} - Loss: {loss.item():.4f}")

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "vocab": vocab,
            "max_len": 12
        },
        "sentiment_model.pt"
    )

    print("Modèle sauvegardé dans sentiment_model.pt")


if __name__ == "__main__":
    main()