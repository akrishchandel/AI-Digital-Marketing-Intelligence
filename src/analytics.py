import pandas as pd  # pyright: ignore[reportMissingModuleSource]

# Load cleaned dataset
df = pd.read_csv("data/clean_campaigns.csv")

# Calculate marketing metrics

# Click Through Rate
df["CTR"] = (df["clicks"] / df["impressions"]) * 100

# Cost Per Click
df["CPC"] = df["spend"] / df["clicks"]

# Conversion Rate
df["Conversion_Rate"] = (df["conversions"] / df["clicks"]) * 100

# Return On Ad Spend
df["ROAS"] = df["revenue"] / df["spend"]

# Return On Investment
df["ROI"] = ((df["revenue"] - df["spend"]) / df["spend"]) * 100

# Display results
print("\nMarketing Campaign Analysis")
print("=" * 50)

print(df[
    [
        "campaign",
        "platform",
        "CTR",
        "CPC",
        "Conversion_Rate",
        "ROAS",
        "ROI"
    ]
].head(10))

# Overall performance
print("\nOverall Performance")
print("=" * 50)

print("Total Spend: ₹", round(df["spend"].sum(), 2))
print("Total Revenue: ₹", round(df["revenue"].sum(), 2))
print("Total Clicks:", df["clicks"].sum())
print("Total Conversions:", df["conversions"].sum())

# Best campaign based on ROAS
best_campaign = df.loc[df["ROAS"].idxmax()]

print("\nBest Performing Campaign")
print("=" * 50)
print("Campaign:", best_campaign["campaign"])
print("Platform:", best_campaign["platform"])
print("ROAS:", round(best_campaign["ROAS"], 2))
print("CTR:", round(best_campaign["CTR"], 2), "%")

# Save analyzed dataset
df.to_csv("data/analyzed_campaigns.csv", index=False)

print("\nAnalyzed dataset saved as data/analyzed_campaigns.csv")