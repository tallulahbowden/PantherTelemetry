#%%
# Import Packages
import arcpy
from pathlib import Path
import pandas as pd

#%%
# Make relative paths
scriptsPath = Path(__file__).parent
projectPath = scriptsPath.parent
dataPath = projectPath / "Data"
rawPath = dataPath / "Raw"
processedPath = dataPath / "Processed"
scratchPath = projectPath / "Scratch"
docsPath = projectPath / "Docs"
pantherPath = str(rawPath / "Florida_Panther_Telemetry.csv")

#%%
# Set Arcpy workspace
arcpy.env.workspace = str(dataPath)
arcpy.env.overwriteOutput = True

#%%
# Read in panther telemetry csv
panther = pd.read_csv(pantherPath,
                      parse_dates = ['FLGTDATE', 'last_edited_date'],
                      dtype = {'TIME' : str, 'CATNUMBER' : str, 'AGENCY' : str, 'COMMENTS' : str, 'UTM83EAST' : 'Int64', 'UTM83NORTH' : 'Int64'})

# Print dataframe
panther

# %%
# Create mask for points after 12/31/2004
target_date = pd.Timestamp('2004-12-31', tz='UTC')
panther_dates_mask = panther['FLGTDATE'] > target_date
panther_sorted_dates = panther.loc[panther_dates_mask]

# %%
panther_sorted_dates

# %%
# Make a bounding box for Picayune Strand Restoration Project + buffer
northing_max = 2895791
northing_min = 2866902
easting_max = 454934
easting_min = 433050

# Sort dataframe for points within bounding box
panther_area_mask = (panther['UTM83EAST'] < easting_max) & (panther['UTM83EAST'] > easting_min) & (panther['UTM83NORTH'] < northing_max) & (panther['UTM83NORTH'] > northing_min)
panther_sorted_area = panther_sorted_dates.loc[panther_area_mask]
len(panther_sorted_area)

# %%
panther_sorted_area.set_index('TIME').groupby('CATNUMBER').plot(x = 'UTM83EAST', y = 'UTM83NORTH', title = "Tester", legend = False)

# %%
# Get rid of datapoints with incorrect TIME values

# Separate dataframes based on construction period timeframes

# Find other area to act as control