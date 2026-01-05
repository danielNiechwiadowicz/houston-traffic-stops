import pandas as pd
import numpy as np

CSV_PATH = "tx_houston_2023_01_26.csv" 
OUT_PATH = "tx_houston_2023_01_26_cleaned.csv"

df = pd.read_csv(CSV_PATH)
#Normalizing column names
df.columns = (
    df.columns
      .astype(str)
      .str.strip()
      .str.lower()
)

#Dropping duplicate rows
df = df.drop_duplicates()
if "raw_row_number" in df.columns:
    df = df.drop_duplicates(subset=["raw_row_number"])
    
#Dropping rows that miss critical fields
required = ["date", "time", "district", "outcome"]
for col in required:
    if col not in df.columns:
        raise ValueError(f"Missing required column: '{col}'")

df = df.dropna(subset=required)

#Parsing datetime
df["datetime"] = pd.to_datetime(
    df["date"].astype(str).str.strip() + " " + df["time"].astype(str).str.strip(),
    errors="coerce"
)
df = df.dropna(subset=["datetime"])

#Converting numeric columns
for c in ["lat", "lng", "speed", "posted_speed"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

#Standardizing text columns
text_cols = [
    "location", "geocode_source", "beat", "district",
    "subject_race", "raw_race", "subject_sex",
    "type", "violation", "outcome",
    "vehicle_color", "vehicle_make", "vehicle_model"
]
for c in text_cols:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.lower()
        df.loc[df[c].isin(["nan", "none", "null", ""]), c] = np.nan

#Clean citation_issued into a boolean
if "citation_issued" in df.columns:
    tmp = df["citation_issued"].astype(str).str.strip().str.lower()
    tmp = tmp.replace({
        "y": "yes", "n": "no",
        "true": "yes", "false": "no",
        "1": "yes", "0": "no",
        "t": "yes", "f": "no"
    })
    df.loc[tmp.isin(["yes", "no"]), "citation_issued"] = tmp[tmp.isin(["yes", "no"])]
    df["citation_issued"] = df["citation_issued"].map({"yes": True, "no": False})

#Created analysis fields
df["hour"] = df["datetime"].dt.hour
df["weekday"] = df["datetime"].dt.day_name()
df["month"] = df["datetime"].dt.to_period("M").astype(str)
df["day_night"] = np.where(df["hour"].between(6, 17), "day", "night")

if "subject_race" in df.columns:
    df["race"] = df["subject_race"]
else:
    df["race"] = np.nan

if "raw_race" in df.columns:
    mask = df["race"].isna()
    df.loc[mask, "race"] = df.loc[mask, "raw_race"]

if "race" in df.columns:
    df["race"] = df["race"].replace({
        "black or african american": "black",
        "white (non-hispanic)": "white",
        "hispanic or latino": "hispanic",
        "native hawaiian or other pacific islander": "nhpi",
        "american indian or alaska native": "aian",
    })

print("=== CLEANED DF SHAPE ===")
print(df.shape)

print("\n=== TOP OUTCOMES ===")
if "outcome" in df.columns:
    print(df["outcome"].value_counts(dropna=False).head(20))

print("\n=== TOP DISTRICTS ===")
if "district" in df.columns:
    print(df["district"].value_counts(dropna=False).head(20))

print("\n=== MISSINGNESS (top 12) ===")
print(df.isna().mean().sort_values(ascending=False).head(12))

#Saving clean file
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved cleaned dataset -> {OUT_PATH}")