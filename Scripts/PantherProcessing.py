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


# Sort dataframe for points within bounding box