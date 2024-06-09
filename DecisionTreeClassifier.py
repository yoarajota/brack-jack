import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from lib.MongoDBClient import MongoDBClient

collection = MongoDBClient["player"]

# Buscar dados do MongoDB
data = list(collection.find())

# Transformar dados em DataFrame
records = []
for entry in data:
    for result in entry['results']:
        record = {
            'num_of_decks': entry['num_of_decks'],
            'current_round': entry['current_round'],
            'current_points': result['current_points'],
            'result': result['result']
        }
        for card in result['hand']:
            record[f'card_{card["rank"]}_of_{card["suit"]}'] = 1
        for decision in result['decisions']:
            record['decision'] = decision['decision']
            record['decision_points'] = decision['current_points']
            record['hand_length'] = decision['hand_length']
            record['readeds_length'] = decision['readeds_length']
        records.append(record)

df = pd.DataFrame(records).fillna(0)

# Separar características e rótulos
X = df.drop(columns=['result', 'decision'])
y = df['decision']

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar um modelo simples (Árvore de Decisão)
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Avaliar o modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Prever a decisão para uma nova mão (exemplo)
new_hand = {
    'num_of_decks': 1,
    'current_round': 1,
    'current_points': 5,
    'card_2_of_Diamonds': 1,
    'card_3_of_Hearts': 1,
    'card_8_of_Diamonds': 0,
    'decision_points': 5,
    'hand_length': 2,
    'readeds_length': 3
}
for col in X.columns:
    if col not in new_hand:
        new_hand[col] = 0

new_hand_df = pd.DataFrame([new_hand])
predicted_decision = model.predict(new_hand_df)
print(f'Predicted Decision: {predicted_decision[0]}')