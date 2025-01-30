import pandas as pd
from utils import gsheet_to_df


shee_id = "1KBdgpzKUX-LgE2-n62j6CLSE7JBedYxi7gXwOAHOPRA"

df = gsheet_to_df(shee_id)
df.to_csv("data.csv", index=False)

# Ensure 'Stunden' is in the correct format 'hh:mm:ss'
df["Stunden"] = df["Stunden"].apply(
    lambda x: x if len(x.split(":")) == 3 else x + ":00"
)

# Convert 'Stunden' to timedelta
df["Stunden"] = pd.to_timedelta(df["Stunden"])
# Convert 'Stunden' to hours:minutes format
df["Stunden"] = df["Stunden"].dt.total_seconds() / 3600

# Group by 'Projekt' and sum 'Stunden'
grouped_df = df.groupby("Projekt")["Stunden"].sum().reset_index()

# Convert the result to a list of lists
result = grouped_df.values.tolist()
result_sorted = sorted(result, key=lambda x: x[1])
new_df = pd.DataFrame(result_sorted, columns=["project", "hours"])
new_df.to_csv("result.csv", index=False)
