import pandas as pd

# Vendor data (your extracted proposals)
vendors = [
    {"vendor": "Constant Young", "price_usd": 480000, "timeline_weeks": 26, "team_size": 12, "iso_certified": True},
    {"vendor": "Nordmine AB",    "price_usd": 510000, "timeline_weeks": 22, "team_size": 15, "iso_certified": True},
    {"vendor": "DeepRock Ltd",   "price_usd": 445000, "timeline_weeks": 30, "team_size": 9,  "iso_certified": False},
]

df = pd.DataFrame(vendors)

print("=== RAW VENDOR DATA ===")
print(df)
print()

# STEP 1: Price Score (lower price = higher score, out of 100)
# Formula: the cheapest vendor gets 100, the most expensive gets 0
max_price = df["price_usd"].max()
min_price = df["price_usd"].min()
df["price_score"] = 100 * (max_price - df["price_usd"]) / (max_price - min_price)

print("=== STEP 1: PRICE SCORES ===")
print(df[["vendor", "price_usd", "price_score"]])
print()

# STEP 2: Timeline Score (lower timeline = higher score, out of 100)
# Formula: the fastest vendor gets 100, the slowest gets 0
max_timeline = df["timeline_weeks"].max()
min_timeline = df["timeline_weeks"].min()
df["timeline_score"] = 100 * (max_timeline - df["timeline_weeks"]) / (max_timeline - min_timeline)

print("=== STEP 2: TIMELINE SCORES ===")
print(df[["vendor", "timeline_weeks", "timeline_score"]])
print()

# STEP 3: Certification Bonus (is the vendor ISO certified?)
# 5 bonus points if yes, 0 if no
df["cert_bonus"] = df["iso_certified"].apply(lambda x: 5 if x else 0)

print("=== STEP 3: CERTIFICATION BONUS ===")
print(df[["vendor", "iso_certified", "cert_bonus"]])
print()

# STEP 4: Combined Weighted Score
# How much does each metric matter?
# 50% price (most important), 30% timeline, 20% certification
df["total_score"] = (0.5 * df["price_score"]) + (0.3 * df["timeline_score"]) + (0.2*df["cert_bonus"])

print("=== STEP 4: COMBINED SCORE (50% price + 30% timeline + 20% cert) ===")
print(df[["vendor", "price_score", "timeline_score", "cert_bonus", "total_score"]])
print()

# STEP 5: Rank by score (best first)
ranked = df.sort_values("total_score", ascending=False)

print("=== FINAL RANKING ===")
print(ranked[["vendor", "price_usd", "timeline_weeks", "iso_certified", "total_score"]])
print()

print("=== WINNER ===")
winner = ranked.iloc[0]
print(f"Best proposal: {winner['vendor']} with score {winner['total_score']:.1f}")