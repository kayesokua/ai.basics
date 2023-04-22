import numpy as np
from sklearn.linear_model import LogisticRegression
from joblib import dump, load


X_train = np.load("X_features.npy", allow_pickle=True)
y_train = np.load("y_labels.npy", allow_pickle=True)
X_eval = np.load("X_eval_features.npy", allow_pickle=True)
y_eval = np.load("y_eval_labels.npy", allow_pickle=True)

model = LogisticRegression()
model.name = "Logistic Regression"

model.fit(X_train, y_train)
dump(model, 'logistic_regression_model.joblib')

# Load the model
loaded_model = load('logistic_regression_model.joblib')
predictions = loaded_model.predict(X_eval)

for i in range(len(predictions)):
    print('Predicted label:', predictions[i], 'Correct label:', y_train[i])
