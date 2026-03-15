import pandas as pd

print("📂 Loading dataset...")
# Load dataset
df = pd.read_csv('data/spam.csv', encoding='latin-1')

print(f"Before cleaning: {df.shape[0]} rows, {df.shape[1]} columns")

# Keep only first 2 columns (v1 and v2)
df = df.iloc[:, :2]
print(f"After removing empty columns: {df.shape[0]} rows, {df.shape[1]} columns")

# Rename columns to something meaningful
df.columns = ['label', 'message']
print("✓ Columns renamed to 'label' and 'message'")

# Clean the text: convert to lowercase
df['message'] = df['message'].str.lower()
print("✓ Text converted to lowercase")

# Remove punctuation (simple version)
df['message'] = df['message'].str.replace('[^\w\s]', '', regex=True)
print("✓ Punctuation removed")

# Check for missing values
print(f"\nMissing values: {df.isnull().sum().sum()}")

# Count spam vs ham
spam_count = len(df[df['label'] == 'spam'])
ham_count = len(df[df['label'] == 'ham'])
print(f"\n📊 Dataset stats:")
print(f"   Total messages: {len(df)}")
print(f"   Spam: {spam_count} ({spam_count/len(df)*100:.1f}%)")
print(f"   Ham: {ham_count} ({ham_count/len(df)*100:.1f}%)")

# Save cleaned dataset
df.to_csv('data/cleaned_spam.csv', index=False)
print("\n✅ Cleaned data saved to 'data/cleaned_spam.csv'")

# Show first 5 cleaned messages
print("\n🔍 First 5 cleaned messages:")
print(df.head())