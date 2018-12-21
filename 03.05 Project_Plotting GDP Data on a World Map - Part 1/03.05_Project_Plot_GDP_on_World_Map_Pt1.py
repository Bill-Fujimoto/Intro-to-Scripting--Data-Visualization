"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def pygal_country_dict():
    '''
    Returns Pygal country code dictionary
    '''
    return pygal.maps.world.COUNTRIES

def gdpinfo_dict():
    '''
    Returns the gdp data information dictionary
    '''
    gdpinfo = {
            "gdpfile": "isp_gdp.csv",
            "separator": ",",
            "quote": '"',
            "min_year": 1960,
            "max_year": 2015,
            "country_name": "Country Name",
            "country_code": "Country Code"
            }
    return gdpinfo
    

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

    
def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  
      1.  The dictionary maps country codes from plot_countries to country names
      from gdp_countries.
      2.  The set contains the country codes from plot_countries that were
      not found in gdp_countries.
    """

    plot_to_gdp_countries = {}
    plot_cc_not_in_gdp = set()
    
    for plot_cc in plot_countries:
        if plot_countries[plot_cc] in gdp_countries:
            plot_to_gdp_countries[plot_cc] = plot_countries[plot_cc]
        else:
            plot_cc_not_in_gdp.add(plot_cc)
    return (plot_to_gdp_countries, plot_cc_not_in_gdp)

### Test reconcile_countries_by_name ###

#~ pygal_countries = pygal_country_dict()
#~ gdpinfo = gdpinfo_dict()
#~ gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'],\
                                        #~ gdpinfo['separator'], gdpinfo['quote'])
#~ print(reconcile_countries_by_name(pygal_countries, gdp_data_dict))

#############################


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  
      1. The dictionary maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  
      2. The first set contains the country codes from plot_countries that were not
      found in the GDP data file.  
      3. The second set contains the country codes from plot_countries that were found 
      in the GDP data file, but have no GDP data for the specified year.
    """
    gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'],\
                                        gdpinfo['separator'], gdpinfo['quote'])
    
    plot_cc_to_gdp_countries = reconcile_countries_by_name(plot_countries, gdp_data_dict)
    
    map_dict = {}
    plot_cc_not_in_gdpdata = plot_cc_to_gdp_countries[1]
    plot_cc_no_gdp = set()
    
    for plot_cc in plot_cc_to_gdp_countries[0]:
        key = plot_cc_to_gdp_countries[0][plot_cc]
        if gdp_data_dict[key][year] == '':
            plot_cc_no_gdp.add(plot_cc)
            #~ print('No GDP data for year', year)
        else:
            gdp_year_log = math.log10(float(gdp_data_dict[key][year]))
            map_dict[plot_cc] = gdp_year_log
            #~ print('Country code: {}; GDP: {:.5f}'.format(plot_cc, gdp_year_log))
            
    return (map_dict, plot_cc_not_in_gdpdata, plot_cc_no_gdp)
    
    
### Test build_map_dict_by_name ###

##gdpinfo = gdpinfo_dict()
##plot_countries = pygal_country_dict()                                   
##year = '2000'
##print(build_map_dict_by_name(gdpinfo, plot_countries, year))

#############################


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    gdp_map_data = build_map_dict_by_name(gdpinfo, plot_countries, year)

    world_gdp_chart = pygal.maps.world.World()
    world_gdp_chart.title = 'GDP as Log10() per Country in the Year '+ year
    world_gdp_chart.add('GDP for '+ year, gdp_map_data[0])
    world_gdp_chart.add('Missing from\nBank GDP Data', gdp_map_data[1])
    world_gdp_chart.add('No GDP Reported', gdp_map_data[2])
    world_gdp_chart.render()
    world_gdp_chart.render_to_file(map_file)
    world_gdp_chart.render_in_browser()
    return


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = gdpinfo_dict()

    # Get pygal country code map
    pygal_countries = pygal_country_dict()
##    print(pygal_countries)
    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
