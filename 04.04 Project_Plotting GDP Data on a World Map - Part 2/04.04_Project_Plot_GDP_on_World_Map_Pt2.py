"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

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


def codeinfo_dict():
    '''
    Returns the country code data information dictionary
    '''
    codeinfo = {
            "codefile": "isp_country_codes.csv",
            "separator": ",",
            "quote": '"',
            "plot_codes": "ISO3166-1-Alpha-2",
            "data_codes": "ISO3166-1-Alpha-3"
            }
    return codeinfo


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
            row_key = row[keyfield]
            table[row_key] = row

    return table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo dictionary.
    """

    isp_code_dict = read_csv_as_nested_dict(codeinfo['codefile'], codeinfo['plot_codes'],\
                                        codeinfo['separator'], codeinfo['quote'])
    plot_to_isp_codes = {}
    
    for plot_cc in isp_code_dict:
        plot_to_isp_codes[isp_code_dict[plot_cc][codeinfo['plot_codes']]] \
        = isp_code_dict[plot_cc][codeinfo['data_codes']]
    
    return plot_to_isp_codes

### Test build_country_code_converter() ###

#~ codeinfo = codeinfo_dict()

#~ print(build_country_code_converter(codeinfo))

#############################


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes (2 Char)
                       and values are the corresponding country names
                       (e.g. pygal country codes)
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
      
    """
    plot_to_gdp_countries = {}
    plot_cc_not_in_gdp = set()
    
    plot_to_isp_dict = build_country_code_converter(codeinfo)
    
    plot_to_isp_keys_dict = {key.lower():key for key in plot_to_isp_dict} 
    gdp_keys_dict = {key.lower():key for key in gdp_countries}
    
    #~ print('Plot to ISP dict:', plot_to_isp_dict)
    #~ print()
    #~ print('Plot to ISP keys dict:', plot_to_isp_keys_dict)
    #~ print()
    #~ print('GDP Countries dict:', gdp_countries)
    #~ print()
    #~ print('GDP keys dict:', gdp_keys_dict)
    #~ print()
    #~ print('Plot countries:', plot_countries)
    #~ print()    
    
    for plot_cc in plot_countries:
        try:
            # This is rather easy to get lost.  The goal is to test case insensitive country
            # codes from the plot code to the world code to the gdp code.  This makes use
            # of intermediate dictionaries which maps the lower case key to original case key,
            # for both the plot to isp and the gdp country dictionaries.
            if plot_to_isp_dict[plot_to_isp_keys_dict[plot_cc.lower()]].lower() in gdp_keys_dict:
                plot_to_gdp_countries[plot_cc] = gdp_keys_dict[plot_to_isp_dict[plot_to_isp_keys_dict[plot_cc.lower()]].lower()]
            else:
                plot_cc_not_in_gdp.add(plot_cc)
        except:
            plot_cc_not_in_gdp.add(plot_cc)

    return (plot_to_gdp_countries, plot_cc_not_in_gdp)
    

### Test reconcile_countries_by_code ###

#~ codeinfo = codeinfo_dict()
#~ gdpinfo = gdpinfo_dict()
#~ plot_countries = pygal_country_dict()
#~ gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'], \
            #~ gdpinfo['country_code'], gdpinfo['separator'], gdpinfo['quote'])                               
            
#~ print(reconcile_countries_by_code(codeinfo, plot_countries, gdp_data_dict))

#############################


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  
      1. The dictionary maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  
      2. The first set contains the country codes from plot_countries that were not
      found in the GDP data file.  
      3. The second set contains the country codes from plot_countries that were found 
      in the GDP data file, but have no GDP data for the specified year.
    """
    gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_code'],\
                                        gdpinfo['separator'], gdpinfo['quote']) 

    plot_cc_to_gdp_countries = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data_dict)
    
    map_dict = {}
    plot_cc_not_in_gdpdata = plot_cc_to_gdp_countries[1]
    plot_cc_no_gdp = set()
    
    for plot_cc in plot_cc_to_gdp_countries[0]:
        key = plot_cc_to_gdp_countries[0][plot_cc]
        if gdp_data_dict[key][year] == '':
            plot_cc_no_gdp.add(plot_cc)

        else:
            gdp_year_log = math.log10(float(gdp_data_dict[key][year]))
            map_dict[plot_cc] = gdp_year_log
            
    return (map_dict, plot_cc_not_in_gdpdata, plot_cc_no_gdp)
    
### Test build_map_dict_by_code ###

#~ gdpinfo = gdpinfo_dict()
#~ codeinfo = codeinfo_dict()
#~ plot_countries = pygal_country_dict()
#~ year = '2000'
    
#~ print(build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year))


#############################

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    gdp_map_data = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

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
    Test the project code for several years
    """
    gdpinfo = gdpinfo_dict()
    codeinfo = codeinfo_dict()
    pygal_countries = pygal_country_dict()

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


test_render_world_map()
