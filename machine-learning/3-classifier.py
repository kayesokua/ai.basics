import numpy as np
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load

X_train = np.load("X_train.npy", allow_pickle=True)
y_train = np.load("y_train.npy", allow_pickle=True)
X_eval = np.load("X_eval.npy", allow_pickle=True)
y_eval = np.load("y_eval.npy", allow_pickle=True)

model = DecisionTreeClassifier(random_state=0)

model.fit(X_train, y_train)
dump(model, 'dance_classifier.joblib')

loaded_model = load('dance_classifier.joblib')
predictions = loaded_model.predict(X_eval)

for i in range(len(predictions)):
    print('Predicted label:', predictions[i], 'Correct label:', y_eval[i])