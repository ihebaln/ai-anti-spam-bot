import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from scipy.sparse import load_npz
import os

print("📂 Loading vectorized data...")
# Load the vectorized data
X_train = load_npz('data/split/X_train.npz')
X_test = load_npz('data/split/X_test.npz')
y_train = pd.read_csv('data/split/y_train.csv').squeeze()
y_test = pd.read_csv('data/split/y_test.csv').squeeze()

print(f"Training data: {X_train.shape}")
print(f"Testing data: {X_test.shape}")

print("\n🤖 Training Naive Bayes classifier...")
# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

print("✅ Model trained!")

print("\n📊 Evaluating model...")
# Make predictions
y_pred = model.predict(X_test)

# Show results
print("\n" + "="*50)
print("CLASSIFICATION REPORT")
print("="*50)
print(classification_report(y_test, y_pred))

print("\n" + "="*50)
print("CONFUSION MATRIX")
print("="*50)
cm = confusion_matrix(y_test, y_pred)
print(f"                Predicted")
print(f"                Ham    Spam")
print(f"Actual Ham     {cm[0,0]:5d}   {cm[0,1]:5d}")
print(f"       Spam    {cm[1,0]:5d}   {cm[1,1]:5d}")

# Calculate accuracy
accuracy = (cm[0,0] + cm[1,1]) / len(y_test)
print(f"\n✅ Accuracy: {accuracy:.2%}")

# Save model
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/model.pkl')
print("\n✅ Model saved to 'models/model.pkl'")

# Show some examples of what Boubou learned
print("\n🔍 Top spam indicators:")
feature_names = joblib.load('models/vectorizer.pkl').get_feature_names_out()
log_prob = model.feature_log_prob_[1]  # Spam class
top_spam_idx = np.argsort(log_prob)[-10:]
print("Top 10 words that indicate SPAM:")
for idx in reversed(top_spam_idx):
    print(f"   {feature_names[idx]}: {np.exp(log_prob[idx]):.4f}")