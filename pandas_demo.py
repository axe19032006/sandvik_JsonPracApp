#To create a dataframe from a list of dictionaries
import pandas as pd

vendors = [
    {"vendor": "Constant Young", "price_usd": 480000, "timeline_weeks": 26, "team_size": 12, "iso_certified": True},
    {"vendor": "Nordmine AB",    "price_usd": 510000, "timeline_weeks": 22, "team_size": 15, "iso_certified": True},
    {"vendor": "DeepRock Ltd",   "price_usd": 445000, "timeline_weeks": 30, "team_size": 9,  "iso_certified": False},
]
pd.set_option('display.max_columns', None) # Shows complete table and doesn't hide it
df = pd.DataFrame(vendors)
print(df)
#To see size of rows and columns-
print(df.shape)
#To list all column names
print(df.columns.tolist())
#For summary stats
print(df.describe())
#To select and print a column
print(df["price_usd"])
#APPLYING MATHEMATICAL OPERATIONS ON COLUMN AND PRINTING MULTIPLE COLUMNS TOGETHER
df["price_k"] = df["price_usd"] / 1000
print(df[["vendor", "price_usd", "price_k"]])