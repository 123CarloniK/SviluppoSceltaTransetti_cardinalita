import arcpy
from arcpy import env
from arcpy import management
from arcgisscripting import da
path=r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Piemonte.gdb"
env.workspace = path
env.overwriteOutput=True

# Dati di input e variabili e condizioni

pozzetti = "VERTICI_ESTREMI_NEAR"
transetti = "TRANSETTI_MIN_50_DIS_ESP_JOIN_VERTEX_COUNT_MAG_NEAR"
out_pozzetti = "pozzetti_inter"
Join_Count_2= "Join_Count > 1"
out_transetti = "out_transetti"
#variabili
arcpy.MakeFeatureLayer_management(transetti, "transetti")
arcpy.CreateFeatureclass_management(path,out_transetti,"POLYLINE","","","",r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Piemonte.gdb\VERTICI_ESTREMI_NEAR")
# cerco i pozzetti tra quelli che si intersecano con piu' transetti cioe' quelli con cardinalita' 2

arcpy.SpatialJoin_analysis(pozzetti, transetti, out_pozzetti)
pozzetti_card2= arcpy.management.SelectLayerByAttribute(out_pozzetti, "NEW_SELECTION", Join_Count_2)
arcpy.MakeFeatureLayer_management(pozzetti_card2, "pozzetti_card2")


with arcpy.da.SearchCursor(pozzetti_card2, ['Shape@']) as cursor:
    conto=0
    for row in cursor:
        # usa la geometria per la selezione
        pozz = row[0]
        #seleziona la coppia di transetti del pozzo[n]
        sele_transetto = arcpy.SelectLayerByLocation_management("transetti", "INTERSECT", pozz, "", "NEW_SELECTION")
        arcpy.MakeFeatureLayer_management(sele_transetto, "sele_transetto")
        sort_transetto=[["Shape_Length","ASCENDING"]]
        env.overwriteOutput = True
        arcpy.management.Sort("sele_transetto", "sele_transetto_sort", sort_transetto)
        arcpy.MakeFeatureLayer_management("sele_transetto_sort", "sele_transetto_sort_lyr")
        arcpy.management.SelectLayerByAttribute("sele_transetto_sort_lyr", "NEW_SELECTION", "OBJECTID=1")
        arcpy.management.Append("sele_transetto_sort_lyr", out_transetti, "NO_TEST")
        conto += 1
        print("Ho aggiunto un transetto sono {0}".format(conto))
        arcpy.Delete_management("sele_transetto")

arcpy.DeleteIdentical_management(out_transetti, ["Shape_Length"])






