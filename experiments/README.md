ces demo m'ont servi de test pour comprendre un peu mieux la gestion de texte dans une IA. 
Ne pas faire attention, peu utile au projet final (mais cela m'a été très utile).

## Ce qu’on a fait en machine learning

On a construit un **petit classifieur de texte en PyTorch** capable de prédire si un titre géopolitique est :

```text
positive / neutral / negative
```

Le pipeline machine learning est le suivant :

```text
titre brut
→ nettoyage du texte
→ tokenisation
→ vocabulaire
→ encodage numérique
→ padding
→ tenseur PyTorch
→ embedding
→ classifieur
→ sentiment prédit
```

---

## 1. Texte brut → tokens

Un modèle ne comprend pas directement une phrase comme :

```text
Peace talks resume between two countries
```

On commence donc par découper la phrase en mots simples :

```python
["peace", "talks", "resume", "between", "two", "countries"]
```

C’est la **tokenisation**.

Dans notre cas, elle est simple :

* passage en minuscules ;
* suppression de la ponctuation ;
* découpage avec `split()`.

---

## 2. Tokens → identifiants numériques

PyTorch ne manipule pas des mots, mais des nombres.

On construit donc un vocabulaire :

```python
{
  "<PAD>": 0,
  "<UNK>": 1,
  "peace": 2,
  "talks": 3,
  "resume": 4
}
```

Puis une phrase devient :

```python
[2, 3, 4]
```

Deux tokens spéciaux sont importants :

```text
<PAD> = remplissage
<UNK> = mot inconnu
```

---

## 3. Padding

Les phrases n’ont pas toutes la même longueur.

Exemple :

```python
[2, 3, 4]
```

est plus court que :

```python
[8, 9, 10, 11, 12]
```

Pour entraîner en batch, PyTorch a besoin de tailles fixes. On ajoute donc du padding :

```python
[2, 3, 4, 0, 0, 0, 0, 0]
```

Ici, `0` correspond à `<PAD>`.

---

## 4. Liste de nombres → tenseur PyTorch

Ensuite, on convertit les phrases encodées en tenseurs :

```python
torch.tensor(encoded_examples, dtype=torch.long)
```

La forme obtenue est du type :

```text
[batch_size, sequence_length]
```

Par exemple :

```text
[3, 12]
```

signifie :

```text
3 titres
12 tokens maximum par titre
```

---

## 5. Embedding

Une couche `Embedding` transforme chaque identifiant de mot en vecteur dense.

Exemple conceptuel :

```text
peace → 2 → [0.12, -0.45, 0.33, ...]
```

L’idée est que le modèle apprend une représentation numérique des mots.

Avant embedding :

```text
[batch_size, sequence_length]
```

Après embedding :

```text
[batch_size, sequence_length, embedding_dim]
```

Par exemple :

```text
[3, 12, 32]
```

signifie :

```text
3 titres
12 tokens
32 valeurs numériques par token
```

---

## 6. Moyenne des embeddings

Pour obtenir une représentation globale de la phrase, on fait la moyenne des vecteurs de mots :

```python
sentence_vector = embedded.mean(dim=1)
```

Cela transforme :

```text
[batch_size, sequence_length, embedding_dim]
```

en :

```text
[batch_size, embedding_dim]
```

Donc chaque titre est représenté par un seul vecteur.

---

## 7. Classifieur

Ce vecteur passe ensuite dans un petit réseau :

```text
Embedding
→ moyenne
→ Linear
→ ReLU
→ Linear
→ logits
```

Le modèle produit trois scores bruts :

```text
score negative
score neutral
score positive
```

Ces scores sont appelés **logits**.

---

## 8. Softmax et prédiction

Les logits sont transformés en probabilités avec :

```python
torch.softmax(logits, dim=1)
```

Puis on prend la classe avec la probabilité la plus élevée :

```python
torch.argmax(probabilities, dim=1)
```

Exemple :

```text
negative : 0.02
neutral  : 0.05
positive : 0.93
```

Le modèle prédit donc :

```text
positive
```

---

## 9. Entraînement

Pendant l’entraînement, on compare la prédiction du modèle au vrai label.

On utilise :

```python
nn.CrossEntropyLoss()
```

Puis la séquence PyTorch classique :

```python
optimizer.zero_grad()
logits = model(input_ids)
loss = criterion(logits, y_true)
loss.backward()
optimizer.step()
```

Ce que cela signifie :

```text
1. effacer les anciens gradients
2. faire une prédiction
3. mesurer l’erreur
4. calculer les gradients
5. mettre à jour les poids
```

C’est la base de la **backpropagation**.

---

# Les limites du modèle

## 1. Dataset beaucoup trop petit

C’est la plus grosse limite.

Le modèle a été entraîné sur très peu d’exemples. Il peut donc apprendre par cœur au lieu de généraliser.

Par exemple, il peut bien prédire :

```text
Peace agreement brings hope
```

parce qu’il a vu des mots proches pendant l’entraînement.

Mais il peut mal prédire une phrase nouvelle comme :

```text
Diplomatic uncertainty affects global markets
```

---

## 2. Confiance trop élevée

Tu as vu des scores comme :

```text
0.9997
```

Cela ne veut pas dire que le modèle est réellement sûr.

Avec un petit dataset, le modèle peut devenir **surconfiant** parce qu’il a mémorisé les exemples.

Donc la confiance affichée doit être interprétée avec prudence.

---

## 3. Modèle très simple

Notre modèle fait une moyenne des embeddings.

Cela veut dire qu’il perd beaucoup d’informations sur l’ordre des mots.

Exemple :

```text
Country A attacks Country B
Country B attacks Country A
```

Les mots sont presque les mêmes, mais le sens géopolitique change.

Notre modèle peut mal gérer ce type de nuance.

---

## 4. Pas de vraie compréhension du contexte

Le modèle ne comprend pas réellement la géopolitique.

Il associe surtout certains mots à certains labels.

Exemple :

```text
sanctions
clashes
crisis
aid
peace
summit
```

Il apprend des corrélations simples, mais il ne comprend pas :

* les acteurs ;
* les relations entre pays ;
* le contexte historique ;
* le point de vue politique ;
* l’ironie ou l’ambiguïté.

---

## 5. Sentiment géopolitique subjectif

Un même titre peut être positif pour une région et négatif pour une autre.

Exemple :

```text
Sanctions imposed on Russia
```

Cela peut être :

```text
négatif pour la Russie
positif pour ses opposants
neutre pour un observateur externe
```

Notre modèle prédit seulement un sentiment global, pas un sentiment par acteur ou par cible.

---

## 6. Gestion limitée des mots inconnus

Si un mot n’est pas dans le vocabulaire, il devient :

```text
<UNK>
```

Donc plusieurs mots différents peuvent être représentés par le même identifiant.

Exemple :

```text
ceasefire
embargo
referendum
mobilization
```

s’ils sont inconnus, ils deviennent tous :

```text
<UNK>
```

Le modèle perd donc de l’information.

---

## 7. Pas d’évaluation sérieuse

On n’a pas encore séparé les données en :

```text
train set
validation set
test set
```

Donc on ne mesure pas vraiment la performance du modèle.

Il faudrait ajouter :

* accuracy ;
* precision ;
* recall ;
* F1-score ;
* matrice de confusion.

---

# Synthèse à dire en entretien

Tu peux résumer comme ça :

> J’ai construit un modèle PyTorch simple de classification de texte. Le pipeline transforme un titre en tokens, puis en identifiants numériques, ajoute du padding, convertit le tout en tenseur, passe par une couche d’embedding, puis par un petit réseau linéaire qui produit trois classes : positif, neutre ou négatif. Le modèle est entraîné avec CrossEntropyLoss et backpropagation.
>
> La limite principale est que le dataset est très petit, donc le modèle peut surapprendre et afficher une confiance artificiellement élevée. Il ne comprend pas réellement le contexte géopolitique, il apprend surtout des associations entre mots et labels. C’est un modèle pédagogique qui montre le pipeline complet, mais pour une version robuste il faudrait un vrai dataset, une évaluation sérieuse, et probablement un modèle plus avancé comme un LSTM, un Transformer ou un modèle pré-entraîné.

Le modèle fonctionne bien sur des phrases proches du dataset, mais il généralise mal. Par exemple, une phrase contenant "violence" peut être mal classée si ce mot est peu présent dans les données d’entraînement. Cela montre que le modèle apprend des corrélations simples plutôt qu’une compréhension réelle du texte.
si je veux de nouvelle choses je dois aller dans /docs

J’ai entraîné un modèle de classification de texte en PyTorch : je transforme les titres en vecteurs via un embedding, puis un réseau de neurones apprend à prédire une classe (positif, neutre, négatif) en minimisant une fonction de perte avec backpropagation.

Type de ML que tu fais
supervised learning (apprentissage supervisé)
→ classification

Tu as :

entrée : texte
sortie : label (positive / neutral / negative)
Autres types classiques en machine learning
classification → prédire une catégorie
régression → prédire une valeur (ex: prix)
clustering → regrouper sans labels
réduction de dimension → simplifier les données
génération → créer du texte/images

Les lignes de code les plus importantes (ML pur)
1. Modèle
model = SentimentClassifier(...)
2. Fonction de perte
criterion = nn.CrossEntropyLoss()

explication : mesure l’erreur entre prédiction et vraie classe

3. Optimiseur
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

explication : met à jour les poids du modèle

4. Forward (prédiction)
logits = model(input_ids)

explication : passage dans le réseau

5. Calcul de la loss
loss = criterion(logits, y_true)
6. Backpropagation
loss.backward()

explication : calcule les gradients

7. Mise à jour des poids
optimizer.step()
8. Reset gradients
optimizer.zero_grad()
Résumé ultra court
données → modèle → logits → loss → backward → update


Utilisateur
   ↓
Dashboard / requête HTTP
   ↓
Backend TypeScript
   ↓
FastAPI Python + PyTorch
   ↓
PostgreSQL


Docker sert à lancer tout le projet dans des environnements isolés.

Sans Docker, il faut lancer à la main :

PostgreSQL local
Python + venv + FastAPI
NodeJS + backend
variables d’environnement
ports
dépendances

Avec Docker :

docker compose up --build

lance tout :

postgres
ai-service
backend


npm = lance le backend Node/TypeScript
uvicorn = lance l’API Python FastAPI
PyTorch = fait la prédiction
fetch = récupère les données côté dashboard