# coding=utf-8
import os
import arcpy
#arcpy.env.workspace = os.getcwd()+ r"C:\MUIF\SINFI\Versionamento Progetto\DATI OUTPUT_ELAB PROTOTIPO.gdb"
arcpy.env.workspace = r"C:\MUIF\SINFI\Versionamento Progetto\DATI OUTPUT_ELAB PROTOTIPO.gdb"
arcpy.env.overwriteOutput=True
# set local variables
pozzetti = "subset_point"
route = "ROUTE_BIN_C_Select_sub"

# find features only within search radius
search_radius = "60 Meters"

# find location nearest features
location = "LOCATION"

# find getting angle of neares features
angle = "ANGLE"

# execute the function

field =['SETE']

#aggiungo il campo controllo
controllo="CONTROLLO"
cor_neg="COR_NEG"
arcpy.AddField_management(pozzetti, controllo, "TEXT", "", "", 1, "", "", "", "")

arcpy.MakeFeatureLayer_management(route, "near_route")
with arcpy.da.SearchCursor("near_route",field) as cursor:
    for row in cursor:
        where_clause = "{0}='{1}'".format(field[0],row[0])

        selecta_route=arcpy.management.SelectLayerByAttribute("near_route","NEW_SELECTION", where_clause)
        where_clause2 = "CONTROLLO IS NULL".format()
        arcpy.MakeFeatureLayer_management(pozzetti, "pozz")
        arcpy.management.SelectLayerByAttribute("pozz", "NEW_SELECTION", where_clause2)
        if where_clause2:
            arcpy.Near_analysis("pozz", selecta_route, search_radius, location, angle)
        else:
            pass
        # eseguo near sui nuovi

        with arcpy.da.UpdateCursor("pozz", ['NEAR_ANGLE', 'CONTROLLO','NEAR_FID']) as cursor2:
            for row2 in cursor2:
                while row2[2] != -1:

                    if row2[0] < 0:
                        row2[0] += 180
                    if row2[1] == "Y":
                        pass
                    else:
                        row2[1] = "Y"
                    cursor2.updateRow(row2)
                    break




        #se non sono lavoarati aggiungi i valori di near
        # arcpy.Near_analysis(pozzi_nuovi, selecta_route, search_radius, location, angle)
        # with arcpy.da.UpdateCursor(pozzi_nuovi,['NEAR_ANGLE','CONTROLLO'] ) as cursor2:
        #     for row2 in cursor2:
        #         if row2[0] < 0:
        #             row2[0] += 180
        #         if row2[1] == "Y":
        #             pass
        #         else:
        #             row2[1] = "Y"
        #         # Update the cursor with the updated list
        #         cursor2.updateRow(row2)
        #arcpy.management.Delete("near_features_lyr")


     # #se non sono lavoarati aggiungi i valori di near
     #    arcpy.Near_analysis(in_features, selecta, search_radius, location, angle)
     #    with arcpy.da.SearchCursor(in_features,'NEAR_ANGLE' ) as cursor3:
     #        for row3 in cursor3:
     #            ro=row3[0]
     #            if ro < 0:
     #                arcpy.CalculateField_management(in_features, 'NEAR_ANGLE', 'NEAR_ANGLE=NEAR_ANGLE+180')
     #            else:
     #
     #
     #                #contassegno come fatte
     #                with arcpy.da.SearchCursor(in_features, controllo) as cursor2:
     #                    for row2 in cursor2:
     #                        if row2[0] == None:
     #                            arcpy.CalculateField_management(in_features, controllo, 'CONTROLLO="Y"')
     #                            print(controllo)
     #                        else:
     #                            pass
     #
     #
     #
     #    #identifica il campo controllo
     #    #
     #
     #    arcpy.management.Delete("near_features_lyr")


