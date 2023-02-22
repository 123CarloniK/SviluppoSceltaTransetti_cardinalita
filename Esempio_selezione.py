# Set the necessary product code
# import arcinfo


# Import the Arcpy Module

import arcpy
from arcpy import env

# Set up the working Environment

env.workspace = r"D:\Travis\Personal\Geoff\Nantucket\Zoning\Backlots\Backlots.gdb"
env.overwriteOutput = True

#Variables
Parcels ="R40_80000sqft"
Structures = "Nantucket_Structres"

arcpy.MakeFeatureLayer_management(parcels,"Parcels_lyr")
arcpy.MakeFeatureLayer_management(Structures,"Struc_Lyr")

Struc_Lyr = "Struc_Lyr"
Parc_Lyr = "Parcels_Lyr"

#Add a field to parcels to be populated with building area
#arcpy.AddField_management("R40_80000sqft","Bldg_Area","DOUBLE")

with arcpy.da.SearchCursor(Parc_Lyr, ['Shape@']) as parcelcursor:
    
    for parcelrow in parcelcursor:

        #get the geometry to use in the spatial selection
        geom = parcelrow[0]

        #select feature from the other layer using the geom variable
        arcpy.SelectLayerByLocation_management(Struc_Lyr, "HAVE_THEIR_CENTER_IN", geom, "", "NEW_SELECTION")

        #get the area of the selected features and sum
        areasum = 0
        with arcpy.da.SearchCursor(Struc_Lyr,['Shape@AREA']) as newcursor:
            for newrow in newcursor:
                areasum = areasum + newrow[0]

        print areasum‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍