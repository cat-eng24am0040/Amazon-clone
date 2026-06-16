import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import pickle

# Read training data
data = pd.read_csv("training_data.csv")

# Inputs
X = data["query"]

# Outputs
y = data["product_id"]

# Convert text into numbers
vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Create model
model = LogisticRegression()

# Train model
model.fit(X_vectorized, y)

# Save model
with open("search_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Model Trained Successfully")