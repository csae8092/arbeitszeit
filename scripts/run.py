import os
import shutil
import pandas as pd
from utils import gsheet_to_df


out_dir = "out"
shutil.rmtree(out_dir, ignore_errors=True)
os.makedirs(out_dir, exist_ok=True)

shee_id = os.environ.get("SHEET_ID")

df = gsheet_to_df(shee_id)

# Ensure 'Stunden' is in the correct format 'hh:mm:ss'
df["Stunden"] = df["Stunden"].apply(
    lambda x: x if len(x.split(":")) == 3 else x + ":00"
)

# Add new column "month" and populate it from "Tag" using the first ten characters
df["Monat"] = df["Tag"].str[:7]

# Convert 'Stunden' to timedelta
df["Stunden"] = pd.to_timedelta(df["Stunden"])
# Convert 'Stunden' to hours:minutes format
df["Stunden"] = df["Stunden"].dt.total_seconds() / 3600

df.to_csv("data.csv", index=False)

for g, ndf in df.groupby("Monat"):
    f_name = os.path.join(out_dir, f"{g}.csv")
    # Group by 'Projekt' and sum 'Stunden'
    grouped_df = ndf.groupby("Projekt")["Stunden"].sum().reset_index()
    # Convert the result to a list of lists
    result = grouped_df.values.tolist()
    result_sorted = sorted(result, key=lambda x: x[1])
    new_df = pd.DataFrame(result_sorted, columns=["project", "hours"])
    new_df.to_csv(f_name, index=False)
