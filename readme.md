# Recipes ETL

This Python script performs an Extract, Transform, and Load (ETL) process on the bi_recipes.json file to filter and process recipes with "Chilies" as an ingredient. It calculates the difficulty of each recipe based on prepTime and cookTime and saves the results in CSV files.

## Requirements

- Python 3.x
- pandas
- numpy
- request

## Installation

1. Clone this repository to your local machine:

git clone https://github.com/furqansaqib/recipes-etl

2. Now, open recipes-etl directory and open Anaconda/command prompt in this directory.

3. Run the following code to run ETL:
python recipes-etl/main.py

4. To run Test cases unit_test_cases.py file is created which should throw an error if any test case written in it is failing.

## Note

1. The ETL process will handle variations in the spelling of "Chilies" and its singular form.
2. The ETL process ensures that the resulting "Chilies.csv" file has no duplicates.
3. The "Results.csv" file will contain 3 rows, each with the average total time aggregated at different difficulty levels.
4. unit_test_case.py file has unit test cases written for iso8601_to_minutes() and calculate_difficulty() functions.

### Please feel free to contact me in case you are facing any challenge to run the ETL :smile: