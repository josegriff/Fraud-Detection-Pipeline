import pandas as pd

file_path= "data/raw/fraudTrain.csv"

df = pd.read_csv(file_path)

print("Shape (rows, columns):", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())
print("\nFraud rate check:\n", df['is_fraud'].value_counts(normalize=True))

print("\nRaw counts:")
print(df['is_fraud'].value_counts())

print("\nPercentages (%):")
print(df['is_fraud'].value_counts(normalize=True) * 100)

sample_size = 100000
sample_df = df.head(sample_size)
output_path = "data/processed/fraudTrain_sample.csv"
sample_df.to_csv(output_path, index=False)

