import requests


BACKEND_URL = "http://127.0.0.1:3000/analyze"


HEADLINES = [
    {
        "text": "Peace agreement brings hope",
        "source": "manual",
        "region": "Europe"
    },
    {
        "text": "Violent clashes erupt near border",
        "source": "manual",
        "region": "Middle East"
    },
    {
        "text": "Leaders gather for climate summit",
        "source": "manual",
        "region": "Europe"
    },
    {
        "text": "Economic sanctions increase tensions",
        "source": "manual",
        "region": "Europe"
    },
    {
        "text": "Humanitarian aid reaches civilians",
        "source": "manual",
        "region": "Africa"
    }
]


def main():
    for headline in HEADLINES:
        response = requests.post(BACKEND_URL, json=headline)

        print("Titre :", headline["text"])
        print("Status :", response.status_code)

        if response.ok:
            print("Réponse :", response.json())
        else:
            print("Erreur :", response.text)

        print("---")


if __name__ == "__main__":
    main()