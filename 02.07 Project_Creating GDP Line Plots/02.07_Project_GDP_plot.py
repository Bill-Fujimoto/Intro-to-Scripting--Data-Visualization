"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal

def isfloat(value):
    """
    Input:
    string to test for float type
    Output:
    Returns True if float type, False if not
    """
    try:
        float(value)
        return True
    except:
        return False

    
def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a DICTIONARY of ORDERED dictionaries where the outer dictionary
      maps the value in the key_field column to the corresponding row in the
      CSV file.  The inner Ordered dictionaries map the field names to the
      field values (as a tuple) for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in an Ordered dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
      
    """
    min_year = int(gdpinfo['min_year'])
    max_year = int(gdpinfo['max_year'])
##    print('GDP data =', gdpdata)

    valid_years = []
    for year, gdp in gdpdata.items():
        #Test if there is valid year and gdp data
        if (year.isdecimal() and isfloat(gdp)):
            #Test year if it is within min and max range
            if (int(year) >= min_year and int(year) <= max_year):
                valid_years.append(year)
            
    valid_years.sort(key=lambda num: int(num))
##    print('Sorted years = ', valid_years)
    plot_values = [(int(year), float(gdpdata[year])) for year in valid_years]

    return plot_values


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    filename = gdpinfo["gdpfile"]
    keyfield = gdpinfo["country_name"]
    separator = gdpinfo["separator"]
    quote = gdpinfo["quote"]
    
    gdpdata_full = read_csv_as_nested_dict(filename, keyfield, separator, quote)
    plot_dict = {}
##    print('GDP keys: ', gdpdata_full.keys())
##    print('Country list: ', country_list)
    for country in country_list:
        if country in gdpdata_full:
            gdpdata = gdpdata_full[country]
##            print('GDP data by country_list: ', gdpdata)
            plot_dict[country] = build_plot_values(gdpinfo, gdpdata)
        else:
            plot_dict[country] = []
##    print('Plot dict: ', plot_dict)
    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_dict = build_plot_dict(gdpinfo, country_list)
    gdp_chart = pygal.XY()

    for country in country_list:
        gdp_chart.add(country, plot_dict[country])
        
    gdp_chart.render_to_file(plot_file)
    return


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"], "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

##test_render_xy_plot()
