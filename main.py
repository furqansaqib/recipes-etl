import requests
import pandas as pd
import numpy as np

def calculate_difficulty(prep_time, cook_time):
    total_time = prep_time + cook_time

    if total_time > 60:
        return 'Hard'
    elif 30 <= total_time <= 60:
        return 'Medium'
    elif total_time < 30:
        return 'Easy'
    else:
        return 'Unknown'
    
def iso8601_to_minutes(duration):
    if isinstance(duration, str) and duration.startswith('PT'):
        minutes = 0
        time_str = duration[2:]
        if 'H' in time_str:
            hours, time_str = time_str.split('H')
            minutes += int(hours) * 60
        if 'M' in time_str:
            minutes_str = time_str.rstrip('M')
            minutes += int(minutes_str)
        return minutes
    return None

def download_file(url, output_path):
    try:
        response = requests.get(url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"File '{output_path}' downloaded successfully.")
    except Exception as e:
        print(f"Error occurred while downloading '{output_path}': {str(e)}")

def main():

    # Step 1: Download the bi_recipes.json file
    file_url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
    download_file(file_url, "bi_recipes.json")

    try:
        # Step 2: Read and process the bi_recipes.json file
        recipes_chilies = pd.DataFrame(columns=["name", "ingredients", "url", "image", "cookTime", "recipeYield", "datePublished", "prepTime", "description", "difficulty"])
        recipes_stg = pd.read_json(file_url, lines=True)

        # Step 3: Filter Chilies based recipes
        pattern = r'(chile|chili|chilies|chiles)\w*'
        recipes_chilies_stg = recipes_stg[recipes_stg['ingredients'].str.contains(pattern, case=False)]
        recipes_chilies = pd.concat([recipes_chilies, recipes_chilies_stg], ignore_index=True)

        # Step 4: Convert prepTime and cookTime into minutes format
        recipes_chilies['prepTime'] = recipes_chilies['prepTime'].apply(iso8601_to_minutes)
        recipes_chilies['cookTime'] = recipes_chilies['cookTime'].apply(iso8601_to_minutes)

        # Step 5: Calculate difficulty of each recipe
        recipes_chilies['difficulty'] = recipes_chilies.apply(lambda row: calculate_difficulty(row['prepTime'], row['cookTime']), axis=1)

        # Step 6: Remove newline characters and do data cleaning to load data into CSV in a readable format
        recipes_chilies['ingredients'] = recipes_chilies['ingredients'].replace('\\n', '', regex=True)
        recipes_chilies['ingredients'] = recipes_chilies['ingredients'].str.replace('\\xa0', '', regex = True)
        recipes_chilies['description'] = recipes_chilies['description'].str.strip()

        # Step 7: Drop Duplicates 
        recipes_chilies = recipes_chilies.drop_duplicates(subset=recipes_chilies.columns.difference([recipes_chilies.index.name]))

        # Step 8: Create Chilies CSV with | as a separator"
        recipes_chilies.to_csv("Chilies.csv", index=False, sep='|', encoding='utf-16')

        # Step 9: Calculate Average time for each difficulty
        recipes_chilies_filtered = recipes_chilies[recipes_chilies['difficulty'] != 'Unknown']
        avg_total_time = recipes_chilies_filtered.groupby('difficulty').agg({'prepTime': 'sum', 'cookTime': 'sum'})
        total_rows = recipes_chilies_filtered['difficulty'].value_counts()
        avg_total_time['AverageTotalTime'] = (avg_total_time['prepTime'] + avg_total_time['cookTime']) / total_rows
        avg_total_time.reset_index(inplace=True)
        avg_total_time.drop(['prepTime', 'cookTime'], axis=1, inplace=True)

        # Step 10: Creates Result CSV with | as a separator
        avg_total_time.to_csv("Results.csv", sep="|", index=False)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
