
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_PATH = "tx_houston_2023_01_26_cleaned.csv" 
df = pd.read_csv(CSV_PATH)

#What hour do stops happen most
stops_by_hour = df.groupby("hour").size().sort_index()
print(stops_by_hour)
plt.figure()
stops_by_hour.plot(kind="bar")
plt.title("Traffic Stops by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Stops")
plt.tight_layout()
plt.show()

#Analysis
peak_hour = stops_by_hour.idxmax()
peak_hour_count = int(stops_by_hour.max())
low_hour = stops_by_hour.idxmin()
low_hour_count = int(stops_by_hour.min())

print(f"Peak stop hour: {peak_hour}:00 ({peak_hour_count:,} stops).")
print(f"Lowest stop hour: {low_hour}:00 ({low_hour_count:,} stops).")

top3_hours = stops_by_hour.sort_values(ascending=False).head(3)
print("Top 3 hours:", ", ".join([f"{h}:00 ({int(c):,})" for h, c in top3_hours.items()]))
rush_hours = [7,8,9,16,17,18]
rush_share = stops_by_hour.loc[stops_by_hour.index.isin(rush_hours)].sum() / stops_by_hour.sum()
print(f"Share of stops during common commute hours (7–9am, 4–6pm): {rush_share*100:.2f}%.")

#What day do stops happen the most
weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
stops_by_weekday = df.groupby("weekday").size().reindex(weekday_order)
print(stops_by_weekday)
plt.figure()
stops_by_weekday.plot(kind="bar")
plt.title("Traffic Stops by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Number of Stops")
plt.tight_layout()
plt.show()

#Analysis
peak_day = stops_by_weekday.idxmax()
peak_day_count = int(stops_by_weekday.max())
low_day = stops_by_weekday.idxmin()
low_day_count = int(stops_by_weekday.min())

print(f"Peak weekday: {peak_day} ({peak_day_count:,} stops).")
print(f"Lowest weekday: {low_day} ({low_day_count:,} stops).")

weekend = stops_by_weekday.loc[["Saturday","Sunday"]].sum()
weekday = stops_by_weekday.loc[["Monday","Tuesday","Wednesday","Thursday","Friday"]].sum()
print(f"Weekend vs Weekday: {weekend:,} weekend stops vs {weekday:,} weekday stops "f"({(weekend/(weekend+weekday))*100:.2f}% on weekends).")

#Top districts of traffic stops
top_districts = df["district"].value_counts().head(10)
print(top_districts)
plt.figure()
top_districts.sort_values().plot(kind="barh")
plt.title("Top 10 Districts by Traffic Stops")
plt.xlabel("Number of Stops")
plt.ylabel("District")
plt.tight_layout()
plt.show()

#Analysis
total_stops = len(df)
top1_district = top_districts.index[0]
top1_count = int(top_districts.iloc[0])
top10_share = top_districts.sum() / total_stops

print(f"Top district: {top1_district} ({top1_count:,} stops).")
print(f"Concentration: Top 10 districts account for {top10_share*100:.2f}% of all stops.")

#Speeding Gap: Speed vs Post-speed distribution + percent over limit
df["over_limit"] = df["speed"] - df["posted_speed"]
speed_stats = df["over_limit"].describe()
print(speed_stats)

pct_over = (df["over_limit"] > 0).mean()
print("Percent over limit:", round(pct_over * 100, 2), "%")
plt.figure()
df["over_limit"].dropna().plot(kind="hist", bins=40)
plt.title("Distribution of Speed Minus Posted Speed")
plt.xlabel("MPH Over Limit (Negative = Under)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

#Analysis
speed_df = df.dropna(subset=["speed","posted_speed"]).copy()
speed_df["over_limit"] = speed_df["speed"] - speed_df["posted_speed"]

pct_over = (speed_df["over_limit"] > 0).mean()
median_over = speed_df["over_limit"].median()
p90_over = speed_df["over_limit"].quantile(0.90)

print(f"Speeding prevalence: {pct_over*100:.2f}% of records are above the posted speed.")
print(f"Median (speed - posted): {median_over:.2f} mph.")
print(f"90th percentile (speed - posted): {p90_over:.2f} mph (only 10% exceed this).")
