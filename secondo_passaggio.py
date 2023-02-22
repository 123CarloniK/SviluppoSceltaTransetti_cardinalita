import arcpy
from arcpy import env
from arcpy import management
from arcgisscripting import da
path=r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Teas_Cardinalita.gdb"
env.workspace = path
env.overwriteOutput=True

# Dati di input e variabili e condizioni
#
pozzetti = "pozzetti_inter"
transetti = "out_transetti"
out_pozzetti = "pozzetti_new"
#Join_Count= "Join_Count_1 > 1"
out_transetti = "transetti_new"
tran_card1="tran_card1"
#variabili
arcpy.MakeFeatureLayer_management(transetti, "transetti")
arcpy.CreateFeatureclass_management(path,out_transetti,"POLYLINE","","","",r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Piemonte.gdb\VERTICI_ESTREMI_NEAR")
# cerco i pozzetti tra quelli che si intersecano con piu' transetti cioe' quelli con cardinalita' 2

arcpy.SpatialJoin_analysis(pozzetti, transetti, out_pozzetti)
#pozzetti_card2= arcpy.management.SelectLayerByAttribute(out_pozzetti, "NEW_SELECTION", Join_Count)
#arcpy.MakeFeatureLayer_management(pozzetti_card2, "pozzetti_card2")


with arcpy.da.SearchCursor(out_pozzetti, ['Shape@']) as cursor:
    conto=0
    for row in cursor:
        # usa la geometria per la selezione
        pozz = row[0]
        #seleziona la coppia di transetti del pozzo[n]
        sele_transetto = arcpy.SelectLayerByLocation_management("transetti", "INTERSECT", pozz, "", "NEW_SELECTION")
        #arcpy.MakeFeatureLayer_management(sele_transetto, "sele_transetto")
        n = int(arcpy.GetCount_management("transetti").getOutput(0))
        print("la selezione ha {0} oggetti".format(n))
        env.overwriteOutput = True
        sort_transetto = [["Shape_Length", "ASCENDING"]]
        arcpy.management.Sort("transetti", "sele_transetto_sort", sort_transetto)
        arcpy.MakeFeatureLayer_management("sele_transetto_sort", "sele_transetto_sort_lyr")
        arcpy.management.SelectLayerByAttribute("sele_transetto_sort_lyr", "NEW_SELECTION", "OBJECTID=1")
        if n==0:
            pass
        elif n==1:
            arcpy.CreateFeatureclass_management(path,tran_card1,"POLYLINE","","","",r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Piemonte.gdb\VERTICI_ESTREMI_NEAR")
            arcpy.management.Append("sele_transetto_sort_lyr", tran_card1, "NO_TEST")
            arcpy.Delete_management("sele_transetto")
        elif n > 1:
            arcpy.management.Append("sele_transetto_sort_lyr", out_transetti, "NO_TEST")
            arcpy.Delete_management("sele_transetto")
            conto += 1
            print("Ho aggiunto un transetto sono {0}".format(conto))

sele_out=arcpy.SelectLayerByLocation_management(out_transetti, "INTERSECT", tran_card1, "", "NEW_SELECTION")
arcpy.DeleteRows_management(sele_out)
arcpy.DeleteIdentical_management(out_transetti, ["Shape_Length"])

