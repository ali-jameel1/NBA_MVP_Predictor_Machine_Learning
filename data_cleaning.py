import pandas as pd

# Open and save CSV files to local variables
mvp_stats = pd.read_csv("mvp.csv")
player_stats = pd.read_csv("player.csv")
team_stats = pd.read_csv("team.csv")

# Select the nessesarry columns, and remove unnessesarry columns
mvp_stats = mvp_stats[["Player", "Year", "Pts Won", "Pts Max", "Share"]]
del player_stats["Unnamed: 0"]
del player_stats["Rk"]

# Remove unwanted astricks from the data
player_stats["Player"] = player_stats["Player"].str.replace("*","", regex=False)
team_stats["Team"] = team_stats["Team"].str.replace("*", "", regex=False)

# Define a function that will modify the data so that each player is only shown once per year, showing their total stats
# Rather than being broken down into stats for each team they played on
def single_team(df):
    if df.shape[0]==1:
        return df
    else:
        row = df[df["Tm"]=="TOT"]
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row

player_stats = player_stats.groupby(["Player", "Year"]).apply(single_team)

# Drop unwanted columns
for i in range (2):
    player_stats.index = player_stats.index.droplevel()


# Merge the two data sets based on the player and year
combined = player_stats.merge(mvp_stats, how="outer", on=["Player", "Year"])

# Ensure there are no empty values, if there are, replace it with 0
combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)

team_stats = team_stats[~team_stats["W"].str.contains("Division")].copy()

# Replace team abriviations with the actual team name, for ex LAL -> Los Angles Lakers
nicknames = {}
with open("nicknames.txt") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev,name = line.replace("\n","").split(",")
        nicknames[abbrev] = name
combined["Team"] = combined["Tm"].map(nicknames)

# Merge the team with the player data so that we can now see the teams record for each player
train = combined.merge(team_stats, how="outer",on=["Team", "Year"])

# Set the data to be numeric
train = train.apply(pd.to_numeric, errors='ignore')
train["GB"] = pd.to_numeric(train["GB"].str.replace("—","0")) 

# Save the data to a CSV file
train.to_csv("player_mvp_stats.csv")

# Test to check the 15 highest scoring players over the seasons
highest_scoring = train[train["G"] > 70].sort_values("PTS", ascending=False).head(15)
print(highest_scoring)