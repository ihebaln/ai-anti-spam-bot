import pandas as pd
from sklearn.model_selection import train_test_split
import os

print("📂 Loading cleaned dataset...")
df = pd.read_csv('data/cleaned_spam.csv')
print(f"Total messages: {len(df)}")

# Prepare features and labels
X = df['message']
y = df['label']

print("\n🔄 Splitting data into train (80%) and test (20%)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Training set: {len(X_train)} messages")
print(f"Testing set: {len(X_test)} messages")

# Create split folder
os.makedirs('data/split', exist_ok=True)

# Save the split data
pd.DataFrame({'message': X_train, 'label': y_train}).to_csv('data/split/train.csv', index=False)
pd.DataFrame({'message': X_test, 'label': y_test}).to_csv('data/split/test.csv', index=False)

print("\n✅ Split data saved to 'data/split/' folder")
print(f"Train: {len(X_train)} messages")
print(f"Test: {len(X_test)} messages")