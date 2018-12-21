"""
Week 3 practice project template for Python Data Visualization
Read two CSV files and join the resulting tables based on shared FIPS codes
Analyze both data sources for anamolous FIPS codes
"""

import csv



#########################################################
# Provided code for week 3

def print_table(table):
    """
    Echo a nested list to the console
    """
    for row in table:
        print(row)


def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list, each list consisting of one row in the CSV file
    """
       
    with open(file_name, newline='') as csv_file:       # don't need to explicitly close the file using 'with'
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def write_csv_file(csv_table, file_name):
    """
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """
    
    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)

# Part 1 - function that creates a dictionary from a table

def make_dict(table, key_col):
    """
    Input: A 2D table (nested lists) and a column index 'key_col', each list is a row.
    Output: return a dictionary of lists whose keys are entries of 'key_col'
    and whose values are lists consisting of the remaining row entries,
    i.e. 'key_col' entry is popped from the row list.
    """
    dict_of_lists = {}
    for row in table:
        key = row[key_col]
        list_copy = list(row)
        list_copy.pop(key_col)
        dict_of_lists[key] = list_copy
    
    return dict_of_lists



def test_make_dict():
    """
    Some tests for make_dict()
    """
    table1 = [[1, 2], [3, 4], [5, 6]]
    print(make_dict(table1, 0))
    print(make_dict(table1, 1))
    table2 = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
    print(make_dict(table2, 1))
    print(make_dict(table2, 2))
    
##test_make_dict()

# Part 2 - script for merging the CSV files

CANCER_RISK_FIPS_COL = 2
CENTER_FIPS_COL = 0

def merge_csv_files(cancer_csv_file, center_csv_file, joined_csv_file):
    """
    Read two specified CSV files as tables
    Join the these tables by shared FIPS codes
    Write the resulting joined table as the specified file
    Analyze for problematic FIPS codes
    """
    
    # Read in both CSV files
    cancer_data = read_csv_file(cancer_csv_file)
    center_data = read_csv_file(center_csv_file)
    
    # Convert both CSV files to dictionarys
    center_dat_dict = make_dict(center_data, CENTER_FIPS_COL)
    cancer_dat_dict = make_dict(cancer_data, CANCER_RISK_FIPS_COL)

    # Compute joined table, print warning about cancer-risk FIPS codes that are not in USA map   
    combined_list = []

    for key_fip in cancer_dat_dict:      
        if key_fip in center_dat_dict:
            #NOTE: insert the key_fip value into the list in separate line BEFORE list.append,
            #otherwise a "None" is returned if done inside append(), not sure I understand why...
            cancer_dat_dict[key_fip].insert(CANCER_RISK_FIPS_COL, key_fip)
            #adding two lists together with '+'
            combined_list.append(cancer_dat_dict[key_fip] + center_dat_dict[key_fip])          
        else:
            print('Cancer data FIPS code '+ key_fip + ' not in USA map data')
  
    # Print warning about USA map FIPS codes that are not in cancer risk data
    print()
    for key_fip in center_dat_dict:
        if key_fip in cancer_dat_dict:
            continue
        else:
            print('USA map FIPS code '+ key_fip + ' not in cancer data')
   
    # Write joined table
    print()
    print('Writing combined csv file')
    write_csv_file(combined_list, joined_csv_file)
    
    return

merge_csv_files("cancer_risk_trimmed_solution.csv", "USA_Counties_with_FIPS_and_centers.csv", "cancer_risk_joined.csv")

## Part 3 - Explanation for anomalous FIPS codes

## https://www1.udel.edu/johnmack/frec682/fips_codes.html
##
## Output anamolies for cancer risk data
## Puerto Rico, Virgin Island, Statewide, Nationwide - FIPS codes are all not present on USA map
## One specific county (Clifton Forge, VA - 51560) is also not present in USA map.
## According URL above, Clifton Forge was merged with another VA county prior to 2001
##
## Output anamolies for USA map
## State_Line, separator - FIPS codes are all not present in cancer-risk data
## One specific county (Broomfield County - 08014) is also not present in cancer-risk data
## Accoring to URL above, Broomfield County was created in 2001
##
## Implies cancer risk FIPS codes were defined prior to 2001, the USA map FIPS codes were defined after 2001
