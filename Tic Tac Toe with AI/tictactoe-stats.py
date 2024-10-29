import pandas as pd
import re
import matplotlib.pyplot as plt
import os

# Define the path to the game logs file
log_file_path = r'C:\Users\hurnir\OneDrive - Caterpillar\Documents\04. Retail Leads & Insights Consultant\Retail - Ad-hoc Analysis\game_logs.txt'

# Check if the file exists
if not os.path.exists(log_file_path):
    print(f"Error: The file '{log_file_path}' does not exist.")
else:
    # Read the game logs
    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    # Parse the game logs
    data = []
    for line in lines:
        match = re.match(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) - Difficulty: ([\w\s]+) - Winner: (\w+) - First Player: (\w+)', line)
        if match:
            date, time, difficulty, winner, first_player = match.groups()
            data.append([date, time, difficulty, winner, first_player])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Time', 'Difficulty', 'Winner', 'First Player'])

    # Create a pivot table with the count of wins
    win_counts = df.pivot_table(index='Winner', columns='Difficulty', aggfunc='size', fill_value=0)

    # Calculate the total number of games for each difficulty level
    total_games = df['Difficulty'].value_counts()

    # Calculate the percentage of wins
    win_percentages = win_counts.div(total_games, axis=1) * 100

    # Combine the counts and percentages into a single DataFrame
    win_stats = win_counts.astype(str) + ' (' + win_percentages.round(2).astype(str) + '%)'

    print(win_stats)