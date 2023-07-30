from main import calculate_difficulty
from main import iso8601_to_minutes
import numpy as np

# Unit Test iso8601 to minutes function.
assert iso8601_to_minutes('PT1H30M') ==90, 'Should be 90'
assert iso8601_to_minutes('PT1H') ==60, 'Should be 60'
assert iso8601_to_minutes('PT9M') ==9, 'Should be 9'
assert iso8601_to_minutes('PT10H20M') == 620, 'Should be 620'

# Unit Test Calculate difficulty function
assert calculate_difficulty(20, 9)=='Easy', 'Should be Easy'
assert calculate_difficulty(0, 1)=='Easy', 'Should be Easy'
assert calculate_difficulty(20, 10)=='Medium', 'Should be Medium'
assert calculate_difficulty(20, 40)=='Medium', 'Should be Medium'
assert calculate_difficulty(40, 21)=='Hard', 'Should be Hard'
assert calculate_difficulty(20000, 102)=='Hard', 'Should be Hard'
assert calculate_difficulty(np.nan, 102)=='Unknown', 'Should be Unknown'
assert calculate_difficulty(np.nan, np.nan)=='Unknown', 'Should be Unknown'
assert calculate_difficulty(20, np.nan)=='Unknown', 'Should be Unknown'