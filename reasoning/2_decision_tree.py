from sklearn.tree import DecisionTreeClassifier
from chatbot import create_user_session, generate_recommendation, load_movement_vocabulary, questions, choices, load_techniques_list
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import json
def load_session_data(dir="data/"):
    sessions = []
    for filename in os.listdir(dir):
        if filename.endswith(".json"):
            with open(dir + filename, "r") as f:
                session_data = json.load(f)
                session_data["id"] = filename.split(".")[0]
                sessions.append(session_data)
    return sessions

session_data = load_session_data("data/")
movement_vocabulary = load_movement_vocabulary()

df = pd.DataFrame(session_data)

# Split the data into training and testing sets
X = df.drop(['recommendations', 'id'], axis=1)
y = df['recommendations']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create decision tree classifier
dtc = DecisionTreeClassifier(random_state=42)
dtc.fit(X_train, y_train)

# Make predictions on testing data
y_pred = dtc.predict(X_test)

# Evaluate model
accuracy = dtc.score(X_test, y_test)
print('Accuracy:', accuracy)