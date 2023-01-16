import requests
import time
from cfscrape import create_scraper
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

# Define years for dataset
years = list(range(1991, 2023)) 

# Define url's that will be later used to retrieve data
mvp_stats_url = "https://www.basketball-reference.com/awards/awards_{}.html"
player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"
 
# Create a scraper object
scraper = create_scraper()

# Retrieve and save the data for all MVP's in dataset
for year in years:
    # Add in the year to the url so that we are getting a new year every loop iteration
    url = mvp_stats_url.format(year)
    # Make the request to the website using the scraper object
    response = scraper.get(url)

    # Save the retrieved html data in a file
    with open("mvp/{}.html".format(year), "w+") as f:
        f.write(response.text)


# Retrieve and save the data for all players's in dataset
for year in years:
    # Add in the year to the url so that we are getting a new year every loop iteration
    url = player_stats_url.format(year)
    # Make the request to the website using the scraper object
    response = scraper.get(url)
    
    # Save the retrieved html data in a file
    with open("player_data/{}.html".format(year), "w+") as f:
        f.write(response.text)


# Retrieve and save the data for all players's in dataset
for year in years:
    # Add in the year to the url so that we are getting a new year every loop iteration
    url = team_stats_url.format(year)
    # Make the request to the website using the scraper object
    response = scraper.get(url)
    
    # Save the retrieved html data in a file
    with open("team/{}.html".format(year), "w+") as f:
        f.write(response.text)


mvp_samples_collection = []

for year in years:
    with open("mvp/{}.html".format(year)) as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    soup.find("tr", class_="over_header").decompose()
    mvp_table = soup.find(id="mvp")
    mvp_data = pd.read_html(str(mvp_table))[0]
    mvp_data["Year"] = year
    mvp_samples_collection.append(mvp_data)

mvps = pd.concat(mvp_samples_collection)

mvps.to_csv("mvps.csv")

driver = webdriver.Chrome(executable_path="/Users/alijameel/chromedriver")

for year in years:
    url = player_stats_url.format(year)
    
    driver.get(url)
    driver.execute_script("window.scrollTo(1,10000)")
    time.sleep(2)
    
    with open("player_data/{}.html".format(year), "w+") as f:
        f.write(driver.page_source)

dfs = []
for year in years:
    with open("player_data/{}.html".format(year)) as f:
        page = f.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    player_table = soup.find_all(id="per_game_stats")[0]
    player_df = pd.read_html(str(player_table))[0]
    player_df["Year"] = year
    dfs.append(player_df)

players = pd.concat(dfs)

players.to_csv("players.csv")

dfs = []
for year in years:
    with open("team/{}.html".format(year)) as f:
        page = f.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    e_table = soup.find_all(id="divs_standings_E")[0]
    e_df = pd.read_html(str(e_table))[0]
    e_df["Year"] = year
    e_df["Team"] = e_df["Eastern Conference"]
    del e_df["Eastern Conference"]
    dfs.append(e_df)
    
    w_table = soup.find_all(id="divs_standings_W")[0]
    w_df = pd.read_html(str(w_table))[0]
    w_df["Year"] = year
    w_df["Team"] = w_df["Western Conference"]
    del w_df["Western Conference"]
    dfs.append(w_df)
    
teams = pd.concat(dfs)

teams.to_csv("teams.csv")