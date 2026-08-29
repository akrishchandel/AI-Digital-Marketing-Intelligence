import pandas as pd

# Load analyzed dataset
df = pd.read_csv("data/analyzed_campaigns.csv")

print("\n" + "=" * 60)
print("CAMPAIGN PERFORMANCE ANALYSIS")
print("=" * 60)

# --------------------------------------------------
# 1. Best Campaign
# --------------------------------------------------

best_campaign = df.loc[df["ROAS"].idxmax()]

print("\n🏆 BEST CAMPAIGN")
print("-" * 40)
print("Campaign:", best_campaign["campaign"])
print("Platform:", best_campaign["platform"])
print("ROAS:", round(best_campaign["ROAS"], 2))
print("CTR:", round(best_campaign["CTR"], 2), "%")
print("Conversion Rate:", round(best_campaign["Conversion_Rate"], 2), "%")


# --------------------------------------------------
# 2. Worst Campaign
# --------------------------------------------------

worst_campaign = df.loc[df["ROAS"].idxmin()]

print("\n📉 WORST CAMPAIGN")
print("-" * 40)
print("Campaign:", worst_campaign["campaign"])
print("Platform:", worst_campaign["platform"])
print("ROAS:", round(worst_campaign["ROAS"], 2))
print("CTR:", round(worst_campaign["CTR"], 2), "%")


# --------------------------------------------------
# 3. Platform Analysis
# --------------------------------------------------

platform_analysis = df.groupby("platform").agg({
    "spend": "sum",
    "revenue": "sum",
    "clicks": "sum",
    "conversions": "sum",
    "impressions": "sum"
}).reset_index()

# Calculate platform metrics
platform_analysis["CTR"] = (
    platform_analysis["clicks"] /
    platform_analysis["impressions"]
) * 100

platform_analysis["Conversion_Rate"] = (
    platform_analysis["conversions"] /
    platform_analysis["clicks"]
) * 100

platform_analysis["ROAS"] = (
    platform_analysis["revenue"] /
    platform_analysis["spend"]
)

print("\n📱 PLATFORM PERFORMANCE")
print("-" * 60)

print(
    platform_analysis[
        [
            "platform",
            "spend",
            "revenue",
            "CTR",
            "Conversion_Rate",
            "ROAS"
        ]
    ].round(2)
)


# --------------------------------------------------
# 4. Best Platform
# --------------------------------------------------

best_platform = platform_analysis.loc[
    platform_analysis["ROAS"].idxmax()
]

print("\n🥇 BEST PLATFORM")
print("-" * 40)

print("Platform:", best_platform["platform"])
print("ROAS:", round(best_platform["ROAS"], 2))
print("CTR:", round(best_platform["CTR"], 2), "%")
print(
    "Conversion Rate:",
    round(best_platform["Conversion_Rate"], 2),
    "%"
)


# --------------------------------------------------
# 5. Save platform analysis
# --------------------------------------------------

platform_analysis.to_csv(
    "data/platform_analysis.csv",
    index=False
)

print("\n✅ Platform analysis saved!")
print("File: data/platform_analysis.csv")