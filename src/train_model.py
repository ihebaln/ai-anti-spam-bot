import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import os

# This code splitting the data to make it ready for training

print("📂 Loading cleaned dataset...")
# Load the cleaned data
df = pd.read_csv('data/cleaned_spam.csv')
print(f"Total messages: {len(df)}")

# Prepare features (X) and labels (y)
X = df['message']  # The text messages
y = df['label']    # The labels (spam/ham)

print("\n🔄 Splitting data into train (80%) and test (20%)...")
# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,           # 20% for testing
    random_state=42,         # For reproducible results
    stratify=y               # Maintain same spam/ham ratio in both sets
)

print(f"Training set: {len(X_train)} messages")
print(f"Testing set: {len(X_test)} messages")

# Check the split is balanced
print("\n📊 Training set distribution:")
print(y_train.value_counts())
print("\n📊 Testing set distribution:")
print(y_test.value_counts())

# Save the split data for later use
os.makedirs('data/split', exist_ok=True)
pd.DataFrame({'message': X_train, 'label': y_train}).to_csv('data/split/train.csv', index=False)
pd.DataFrame({'message': X_test, 'label': y_test}).to_csv('data/split/test.csv', index=False)

print("\n✅ Split data saved to 'data/split/' folder")

# Show some examples
print("\n🔍 First 5 training messages:")
for i in range(5):
    print(f"{i+1}. [{y_train.iloc[i]}] {X_train.iloc[i][:50]}...")