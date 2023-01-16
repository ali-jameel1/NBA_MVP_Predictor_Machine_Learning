import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# Load in the data and fill any empty values with 0
stats = pd.read_csv("player_mvp_stats.csv", index_col=0)
stats = stats.fillna(0)

# Define relevant factors towards determining MVP
predictors = ["Age", "G", "GS", "MP", "FG", "FGA", 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'W', 'L', 'W/L%',
       'GB', 'PS/G', 'PA/G', 'SRS']

# Define test set and the training set
train = stats[~(stats["Year"] == 2022)]
test = stats[stats["Year"] == 2022]

# Create an instance of ridge regression from the sklearn Ridge class
# Note we set alpha to 0.1 so that we have less of bias (less overfitting)
reg = Ridge(alpha=.1)

# Use all the colums in "predictors" to try and predict the value of share
reg.fit(train[predictors],train["Share"])

# Make predictions based on the predictors list
predictions = reg.predict(test[predictors])
# Create a DataFrame to store the resulted predictions
predictions = pd.DataFrame(predictions, columns=["predictions"], index=test.index)
# Combine the DataFrames to get a new one that stores the player name, share and the prediction
combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
