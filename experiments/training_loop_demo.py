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


ID_TO_LABEL = {
    0: "negative",
    1: "neutral",
    2: "positive"
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

    num_epochs = 50

    for epoch in range(num_epochs):
        model.train()

        optimizer.zero_grad()

        logits = model(input_ids)

        loss = criterion(logits, y_true)

        loss.backward()

        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch + 1}/{num_epochs} - Loss: {loss.item():.4f}")

    model.eval()

    with torch.no_grad():
        logits = model(input_ids)
        probabilities = torch.softmax(logits, dim=1)
        predicted_classes = torch.argmax(probabilities, dim=1)

    print("\nRésultats finaux :")

    for title, true_label, predicted_class in zip(titles, labels, predicted_classes):
        predicted_label = ID_TO_LABEL[predicted_class.item()]

        print("Titre :", title)
        print("Label réel :", true_label)
        print("Label prédit :", predicted_label)
        print("---")