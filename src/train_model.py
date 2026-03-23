import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

print("📂 Loading datasets...")
# Load the training and testing data
train_df = pd.read_csv('data/split/train.csv')
test_df = pd.read_csv('data/split/test.csv')

print(f"Training set: {len(train_df)} messages")
print(f"Testing set: {len(test_df)} messages")

# Prepare features (X) and labels (y)
X_train = train_df['message']
y_train = train_df['label']
X_test = test_df['message']
y_test = test_df['label']

print("\n🔄 Converting text to numbers using TF-IDF...")

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,        # Use top 5000 words
    stop_words='english',     # Remove common words (the, a, is, etc.)
    lowercase=True,           # Already lowercase but just in case
    ngram_range=(1, 2)        # Consider single words and pairs
)

# Convert training text to numbers
print("   Processing training data...")
X_train_vectorized = vectorizer.fit_transform(X_train)
print(f"   Training data shape: {X_train_vectorized.shape}")

# Convert testing text to numbers (using the same vectorizer)
print("   Processing testing data...")
X_test_vectorized = vectorizer.transform(X_test)
print(f"   Testing data shape: {X_test_vectorized.shape}")

# Save the vectorizer for later use
os.makedirs('models', exist_ok=True)
joblib.dump(vectorizer, 'models/vectorizer.pkl')
print("\n✅ Vectorizer saved to 'models/vectorizer.pkl'")

# Show some information about what we learned
print("\n📊 TF-IDF Information:")
print(f"   Vocabulary size: {len(vectorizer.vocabulary_)} words")
print(f"   Max features: 5000")

# Show top 10 most important words
feature_names = vectorizer.get_feature_names_out()
print("\n🔍 Top 10 words in vocabulary:")
for i in range(10):
    print(f"   {i+1}. {feature_names[i]}")

# Save the vectorized data for next step
from scipy.sparse import save_npz
save_npz('data/split/X_train.npz', X_train_vectorized)
save_npz('data/split/X_test.npz', X_test_vectorized)
pd.Series(y_train.values).to_csv('data/split/y_train.csv', index=False)
pd.Series(y_test.values).to_csv('data/split/y_test.csv', index=False)

print("\n✅ Vectorized data saved to 'data/split/' folder")

# Show example of vectorization
print("\n🔍 Example - First message:")
print(f"Original: {X_train.iloc[0][:100]}...")
print(f"Vectorized shape: {X_train_vectorized[0].shape}")
print(f"Non-zero elements: {X_train_vectorized[0].nnz} words found")