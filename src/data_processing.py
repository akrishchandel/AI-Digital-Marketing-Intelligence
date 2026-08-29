from importlib import import_module


try:
    pd = import_module("pandas")
except ImportError as exc:
    raise ImportError(
        "pandas is required to run this script. Install it with: pip install pandas"
    ) from exc

# Load dataset
df = pd.read_csv("data/campaigns.csv")

print("Original dataset:")
print(df.head())

# Check dataset information
print("\nDataset information:")
print(df.info())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# Make sure numerical columns contain valid numbers
numeric_columns = [
    "impressions",
    "clicks",
    "spend",
    "conversions",
    "revenue"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows where important numerical values are invalid
df = df.dropna(subset=numeric_columns)

# Remove impossible values
df = df[
    (df["impressions"] > 0) &
    (df["clicks"] >= 0) &
    (df["spend"] >= 0) &
    (df["conversions"] >= 0) &
    (df["revenue"] >= 0)
]

# Save cleaned dataset
df.to_csv("data/clean_campaigns.csv", index=False)

print("\nData cleaning completed!")
print("Final dataset shape:", df.shape)
print("Clean dataset saved as data/clean_campaigns.csv")