Traffic Stop Patterns Analysis

This project analyzes traffic stop data to identify temporal, geographic, and behavioral patterns in traffic enforcement using Python and pandas.

Data Availability

The dataset used in this project is not included in the repository due to file size
constraints. CSV files are excluded from version control.

To reproduce the analysis:
1. Download the traffic stop dataset from https://openpolicing.stanford.edu/data/.
2. Place the CSV file in the directory.
3. Run `clean.py` to generate the cleaned dataset.
4. Run `analysis.py` to reproduce the results and visualizations.

Key Findings

Temporal Patterns
    
Traffic stops are concentrated in the mid afternoon. The single busiest hour is 3:00 pm, with 58598 stops, followed closely by 2:00 pm and 4:00 pm. In contrast, 4:00 am is the least active hour with only 3602 stops.
Notably, 41.37% of all traffic stops occur during common commute hours (7-9 am and 4-6 pm), suggests enforcement aactivity aligns with periods of high roadway usage rather than late night patrols. 

Weekly Trends
    
Traffic stops peak mid week, with Wednesday recording the highest volume of 114,600 stops. Sunday has the fewest stops if 50638, indicating a strong weekday skew in enforcement activity. Overall, weekday stops account for 81.28% of all traffic stops.

Geographic Concentration
    
Traffic stops are highly concentrated. The single busiest district (District 2) accounts for 90558 stops. The top 10 districts account for 67.03% of all recorded traffic stops, indicating that enforcement activity is focused in a small portion of the city rather than being evenly distributed.

Speeding Behavior
    
Among records with valid speed data, speeding is a dominant factor. The median stop occurs at 15 mph over the speed limit, and 90% of drivers are stopped at 23 mph over the speed limit or less.

Conclusion
    
Analysis shows that enforcement is time dependent, geographically concentrated, and strongly associated with speeding behavior. Stops are most common during weekday afternoons and commute hours, clustered in a limited number of districts, and drivers are often well above speed limits. 

