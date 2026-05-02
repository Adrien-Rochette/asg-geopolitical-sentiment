import torch
import torch.nn as nn

from vocab_demo import build_vocab, encode_text


class SimpleSentimentClassifier(nn.Module):
    def __init__(self, vocab_size: int, embedding_dim: int, num_classes: int):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0
        )

        self.classifier = nn.Linear(
            in_features=embedding_dim,
            out_features=num_classes
        )

    def forward(self, input_ids):
        embedded = self.embedding(input_ids)

        sentence_vector = embedded.mean(dim=1)

        logits = self.classifier(sentence_vector)

        return logits


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

    input_ids = torch.tensor(encoded_examples, dtype=torch.long)

    model = SimpleSentimentClassifier(
        vocab_size=len(vocab),
        embedding_dim=10,
        num_classes=3
    )

    logits = model(input_ids)
    probabilities = torch.softmax(logits, dim=1)
    predicted_classes = torch.argmax(probabilities, dim=1)

    print("Probabilités :")
    print(probabilities)

    print("Classes prédites :")
    print(predicted_classes)

    print("Input ids shape:")
    print(input_ids.shape)

    print("Logits:")
    print(logits)

    print("Logits shape:")
    print(logits.shape)