import arcpy
from arcpy import env
from arcpy import management
from arcgisscripting import da
path=r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Teas_Cardinalita.gdb"
env.workspace = path
env.overwriteOutput=True

# Dati di input e variabili e condizioni
#
pozzetti = "VERTICI_ESTREMI_NEAR"
transetti = "TRANSETTI_MIN_50_DIS_ESP_JOIN_VERTEX_COUNT_MAG_NEAR"
out_pozzetti = "pozzetti_inter"
out_transetti = "out_transetti"
tran_card1="tran_card1"
#variabili
arcpy.MakeFeatureLayer_management(transetti, "transetti")
arcpy.CreateFeatureclass_management(path,out_transetti,"POLYLINE","","","",r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Piemonte.gdb\VERTICI_ESTREMI_NEAR")
arcpy.CreateFeatureclass_management(path, tran_card1, "POLYLINE", "", "", "", r"C:\MUIF\SINFI\Versionamento Progetto\SubTest_Piemonte\Piemonte.gdb\VERTICI_ESTREMI_NEAR")

# cerco i pozzetti che intercettano i transetti

with arcpy.da.SearchCursor(pozzetti, ['Shape@']) as cursor:
    conto=0
    conto2=0
    for row in cursor:
        # usa la geometria per la selezione
        pozz = row[0]
        #seleziona la coppia di transetti del pozzo[n]
        sele_transetto = arcpy.SelectLayerByLocation_management("transetti", "INTERSECT", pozz, "", "NEW_SELECTION")
        #arcpy.MakeFeatureLayer_management(sele_transetto, "sele_transetto")
        n = int(arcpy.GetCount_management("transetti").getOutput(0))
        print("la selezione ha {0} oggetti".format(n))
        env.overwriteOutput = True
        #Ordino gli elementi dal più corto al più lungo
        sort_transetto = [["Shape_Length", "ASCENDING"]]
        arcpy.management.Sort("transetti", "sele_transetto_sort", sort_transetto)
        arcpy.MakeFeatureLayer_management("sele_transetto_sort", "sele_transetto_sort_lyr")
        arcpy.management.SelectLayerByAttribute("sele_transetto_sort_lyr", "NEW_SELECTION", "OBJECTID=1")
        if n==0:
            print("Cardinalità 0")
            pass
        elif n == 1:
            conto+=1
            arcpy.management.Append("sele_transetto_sort_lyr", tran_card1, "NO_TEST")
            print("Cardinalità 1 ha un transetto collegato aggiunto {0}".format(conto))
        elif n > 1:
            conto2 += 1
            arcpy.management.Append("sele_transetto_sort_lyr", out_transetti, "NO_TEST")
            print("Cardinalità maggiore di 1 ha più di un transetto collegato {0}".format(conto2))
        arcpy.Delete_management("sele_transetto_lyr")
print("Abbiamo {0} transetti con cardinalità 1 e {1} con cardinalità superiore".format(conto,conto2))
#Tolgo dai transetti quelli che coincidono con quelli con cardinalità maggiore di 1

arcpy.DeleteRows_management(arcpy.SelectLayerByLocation_management(tran_card1, "BOUNDARY_TOUCHES", out_transetti, None, "NEW_SELECTION", "NOT_INVERT"))
#sommo i transetti di cardinalità 1 e maggiore di 1
arcpy.management.Append(out_transetti, tran_card1, "NO_TEST")
arcpy.management.DeleteIdentical("tran_card1", "Shape", None, 0)
#stampo il totale dei transetti
m = arcpy.GetCount_management("tran_card1")
print("Il totale dei transetti sono {0}".format(m))

