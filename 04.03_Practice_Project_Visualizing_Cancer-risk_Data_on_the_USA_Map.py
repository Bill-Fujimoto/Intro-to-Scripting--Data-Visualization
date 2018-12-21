"""
Week 4 practice project solution for Python Data Visualization
Load a county-level PNG map of the USA and plot cancer-risk data at county centers
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import csv



USA_SVG_SIZE = [555, 352]
USA_SVG_SIZE_X = USA_SVG_SIZE[0]
USA_SVG_SIZE_Y = USA_SVG_SIZE[1]
CANCER_RISK_POP_COL = 3
CANCER_RISK_COL = 4
CANCER_RISK_XCOL = 5
CANCER_RISK_YCOL = 6
POP_SCALE = 1/1000000

def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list, each list consisting of one row in the CSV file
    """
       
    with open(file_name, newline='') as csv_file: # don't need to explicitly close the file using 'with'
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table
    

def compute_county_cirle(county_population):
    '''
    Compute the area of plotting circle base on population
    Return computed area
    '''
    area = math.pi * (20 * county_population * POP_SCALE)**1.1
    return area
    

def create_riskmap(colormap, risk_norm):
    '''
    Create and return RGB function in lambda form
    '''
    color_mapper = mpl.cm.ScalarMappable(norm = risk_norm, cmap = colormap)
    return lambda risk : color_mapper.to_rgba(math.log10(risk))


def draw_cancer_risk_map(joined_csv_file_name, map_name, num_counties = None):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """
    cancer_risk_loc = read_csv_file(joined_csv_file_name)
    
    #sort on cancer risk column
    cancer_risk_loc.sort(key=lambda row: float(row[CANCER_RISK_COL]), reverse=True)
    max_risk = math.log10(float(cancer_risk_loc[0][CANCER_RISK_COL]))
    min_risk = math.log10(float(cancer_risk_loc.pop()[CANCER_RISK_COL]))
    #~ max_risk = float(cancer_risk_loc[0][CANCER_RISK_COL])
    #~ min_risk = float(cancer_risk_loc.pop()[CANCER_RISK_COL])
    print('Max risk (log):', max_risk)
    print('Min risk (log):', min_risk)
    
    # Load map image
    map_img = plt.imread(map_name)

    #  Get dimensions of USA map image
    ypixels, xpixels, bands = map_img.shape
    print(xpixels, ypixels, bands)
    
    # Optional code to resize plot as fixed size figure -
    #~ DPI = 50.0                  # adjust this constant to resize your plot
    #~ xinch = xpixels / DPI
    #~ yinch = ypixels / DPI
    #~ plt.figure(figsize=(xinch,yinch))
    
    implot = plt.imshow(map_img)        

    colormap = mpl.cm.jet
    risk_norm = mpl.colors.Normalize(vmin=min_risk, vmax=max_risk)
    
    # This function call returns a Lambda FUNCTION which will be called in the loop:
    risk_map = create_riskmap(colormap, risk_norm)
    
    for row in cancer_risk_loc[0:num_counties]:
        x = float(row[CANCER_RISK_XCOL])*xpixels/USA_SVG_SIZE_X
        y = float(row[CANCER_RISK_YCOL])*ypixels/USA_SVG_SIZE_Y
        area = compute_county_cirle(int(row[CANCER_RISK_POP_COL]))
        colors = risk_map(float(row[CANCER_RISK_COL]))
        plt.scatter(x, y, s = area, c = colors)
        
    # Plot USA map
    plt.show()

draw_cancer_risk_map("cancer_risk_joined.csv", "USA_Counties_1000x634.png", 200)
  

