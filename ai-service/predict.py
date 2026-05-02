import torch

from model import SentimentClassifier
from vocab_demo import encode_text


ID_TO_LABEL = {
    0: "negative",
    1: "neutral",
    2: "positive"
}


def load_model(path: str = "sentiment_model.pt"):
    checkpoint = torch.load(path, map_location="cpu")

    vocab = checkpoint["vocab"]
    max_len = checkpoint["max_len"]

    model = SentimentClassifier(
        vocab_size=len(vocab),
        embedding_dim=32,
        hidden_dim=16,
        num_classes=3
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, vocab, max_len


def predict_sentiment(text: str):
    model, vocab, max_len = load_model()

    encoded = encode_text(text, vocab, max_len=max_len)

    input_ids = torch.tensor([encoded], dtype=torch.long)

    with torch.no_grad():
        logits = model(input_ids)
        probabilities = torch.softmax(logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()

    return {
        "text": text,
        "sentiment": ID_TO_LABEL[predicted_class],
        "confidence": probabilities[0][predicted_class].item()
    }


if __name__ == "__main__":
    examples = [
        "Peace agreement brings hope",
        "Violent clashes erupt near border",
        "President attends international summit"
    ]

    for example in examples:
        result = predict_sentiment(example)

        print("Titre :", result["text"])
        print("Sentiment :", result["sentiment"])
        print("Confiance :", round(result["confidence"], 4))
        print("---")