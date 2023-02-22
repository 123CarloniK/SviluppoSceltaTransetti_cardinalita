# coding=utf-8
import datetime
import math
import sys
from cgitb import handler
import arcpy
import json
import csv
import os
import logging
from logging import handlers

def creo_excel():
    path = r'C:\MUIF\SINFI\Versionamento Progetto'


    tabella_eventi = arcpy.CreateTable_management(str(path), "event_table.dbf")
    arcpy.AddField_management(tabella_eventi, "SEDE_TEC", "Text", 50, "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(tabella_eventi, "SETE", "Text", 50, "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(tabella_eventi, "KM_INIZIO", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(tabella_eventi, "KM_FINE", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(tabella_eventi, "DISTANZA", "Text", 50, "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(tabella_eventi, "LATO_DI_PO", "Text", 50, "", "", "", "NULLABLE", "REQUIRED")
    return tabella_eventi

def aggiungo_riga_excel(riga, tabella_eventi):
    fields = ['SEDE_TEC', 'SETE', 'KM_INIZIO', 'KM_FINE', 'DISTANZA', 'LATO_DI_PO']
    cursor = arcpy.da.InsertCursor(tabella_eventi, fields)
    cursor.insertRow(riga)
    del cursor
    return True

def controllo_distanza(sede_tecnica, media_km, path_csv):
    with open(path_csv, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for riga in csv_reader:
            try:
                KM_FINE = riga['Punto finale SI'].replace(',', '.')
                KM_INI = riga['Punto iniziale SI'].replace(',', '.')
                if float(KM_FINE) > float(KM_INI):
                    if riga["Sede Tecnica"] == sede_tecnica and riga[
                        'Codice caratteristica'] == 'S01500_0030' and float(media_km) < float(KM_FINE) and float(media_km) > float(KM_INI):
                        return riga['Valore car. Numerico']
                elif float(KM_FINE) < float(KM_INI):
                    if riga["Sede Tecnica"] == sede_tecnica and riga['Codice caratteristica'] == 'S01500_0030' and media_km > float(KM_FINE) and media_km < float(KM_INI):
                        return riga['Valore car. Numerico']
            except:
                arcpy.AddMessage(sys.exc_info()[0])
                return riga['Sede Tecnica']

def controllo_binario(sede_tecnica, media_km, path_csv):
    with open(path_csv, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for riga in csv_reader:
            try:
                KM_FINE = riga['Punto finale SI'].replace(',', '.')
                KM_INI = riga['Punto iniziale SI'].replace(',', '.')
                if float(KM_FINE) > float(KM_INI):
                    if riga["Sede Tecnica"] == sede_tecnica and riga[
                        'Codice caratteristica'] == 'S01500_0010' and media_km < float(KM_FINE) and media_km > float(KM_INI):
                        return riga['Valore car.']
                elif float(KM_FINE) < float(KM_INI):
                    if riga["Sede Tecnica"] == sede_tecnica and riga['Codice caratteristica'] == 'S01500_0010' and media_km > float(KM_FINE) and media_km < float(KM_INI):
                        return riga['Valore car.']
            except:
                arcpy.AddMessage(sys.exc_info()[0])
                return riga['Sede Tecnica']

def controllo_chilometriche(sede_tecnica, tipologia, km_inizio, km_fine, path_csv):
    with open(path_csv, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        i = km_fine
        caratteristica = ''
        boolean = False
        print('chilometro inizio controllo chilometriche: ' + km_inizio)
        print('chilometro fine controllo chilometriche: ' + km_fine)
        for riga in csv_reader:
            try:
                if riga['Punto iniziale SI'].replace(',', '.') > riga['Punto finale SI'].replace(',', '.'):
                    KM_INI = riga['Punto finale SI'].replace(',', '.')
                    KM_FIN_DISTANZA = riga['Punto iniziale SI'].replace(',', '.')
                elif riga['Sede Tecnica'] == sede_tecnica:
                    KM_FIN_DISTANZA = riga['Punto finale SI'].replace(',', '.')
                    KM_INI = riga['Punto iniziale SI'].replace(',', '.')

                if riga['Sede Tecnica'] == sede_tecnica and riga['Codice caratteristica'] == tipologia and float(
                        km_fine) > float(KM_FIN_DISTANZA) and float(km_inizio) < float(
                    KM_FIN_DISTANZA) and km_fine != KM_FIN_DISTANZA:
                    print(i)
                    if i > KM_FIN_DISTANZA:
                        i = KM_FIN_DISTANZA
                        caratteristica = riga['Valore car. Numerico']
                        boolean = True
            except:
                arcpy.AddMessage(sys.exc_info()[0])
                return riga['Sede Tecnica']
        if boolean == True:
            lista_caratteristiche = [i, caratteristica]
            return lista_caratteristiche
        else:
            return False





def creoExcel(path_csv):
    global tabella_errori
    tabella_errori = []
    tabella_eventi = creo_excel()
    print('sono entrata nel metodo')

    with open(path_csv, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        global SEDI_TECNICHE

        SEDI_TECNICHE = []

        for riga in csv_reader:
            print('Leggo CSV')
            if riga["Sede Tecnica"] not in SEDI_TECNICHE:
                print('sono in controllo sede_tecniche')
                SEDI_TECNICHE.append(riga["Sede Tecnica"])
                sede_tecnica = riga["Sede Tecnica"]
                print(riga['Codice caratteristica'])
                with open(path_csv, 'r') as csv_file:
                    csv_reader_2 = csv.DictReader(csv_file, delimiter=';')
                    for riga in csv_reader_2:
                        if riga['Codice caratteristica'] == 'S01500_0020' and riga['Sede Tecnica'] == sede_tecnica:
                            try:
                                print('sono in caratteristica lato di posa')
                                print(riga['Sede Tecnica'])
                                KM_INI = riga['Punto iniziale SI'].replace(',', '.')
                                KM_FINE = riga['Punto finale SI'].replace(',', '.')
                                if KM_INI > KM_FINE:
                                    x = KM_INI
                                    KM_INI = KM_FINE
                                    KM_FINE = x
                                media_km = (float(KM_INI) + float(KM_FINE)) / 2
                                sete = controllo_binario(sede_tecnica, media_km, path_csv)
                                print('KM_FINE LATO DI POSA ' + KM_FINE)
                                risultato = controllo_chilometriche(sede_tecnica, 'S01500_0030', KM_INI, KM_FINE, path_csv)
                            except:
                                arcpy.AddMessage(sys.exc_info()[0])
                                tabella_errori.append(riga['Sede Tecnica'])
                            if risultato == False:
                                distanza = controllo_distanza(sede_tecnica, media_km, path_csv)
                                try:
                                    riga_tabella = [riga['Sede Tecnica'], sete, KM_INI, KM_FINE, distanza.replace(',', '.'), riga['Valore car.']]
                                    print('riga tabella se non e presente un intervallo minore')
                                    riga_excel = aggiungo_riga_excel(riga_tabella, tabella_eventi)
                                except:
                                    arcpy.AddMessage(sys.exc_info()[0])
                                    tabella_errori.append(riga['Sede Tecnica'])
                            else:
                                KM_INIZIO = KM_INI
                                contatore = 0
                                '''
                                MODIFICATO IL CODICE INTRODUCENDO UN IF ELSE INVECE DI  while risultato != False:
                                Su alcuni dati vedi C:\MUIF\SINFI\Scarichi\Export_AssetS01500_ERR.csv andava in loop infinito
                                '''
                                if risultato != False:
                                    contatore = contatore + 1
                                    print(contatore)
                                    KM_FIN = risultato[0]
                                    try:
                                        riga_tabella = [riga['Sede Tecnica'], sete, float(KM_INIZIO.replace(',', '.')),
                                                        float(KM_FIN.replace(',', '.')), risultato[1].replace(',', '.'),
                                                        riga['Valore car.']]
                                        print(riga_tabella)
                                        print('riga tabella se e\' presente un intervallo minore')
                                        riga_excel = aggiungo_riga_excel(riga_tabella, tabella_eventi)
                                        print(KM_FIN)
                                        KM_INIZIO = KM_FIN
                                        risultato = controllo_chilometriche(sede_tecnica, 'S01500_0030', KM_INIZIO,
                                                                            KM_FINE, path_csv)
                                        print(KM_FINE)
                                    except:
                                        arcpy.AddMessage(sys.exc_info()[0])
                                        tabella_errori.append(riga['Sede Tecnica'])
                                else:
                                    try:
                                        media_km = (float(KM_INIZIO.replace(',', '.')) + float(KM_FINE)) / 2
                                        print(media_km)
                                        distanza = controllo_distanza(sede_tecnica, media_km, path_csv)
                                        print(distanza)
                                    except:
                                        arcpy.AddMessage(sys.exc_info()[0])
                                        tabella_errori.append(riga['Sede Tecnica'])
                                    try:
                                        riga_tabella = [riga['Sede Tecnica'], sete, KM_INIZIO, KM_FINE,
                                                        distanza.replace(',', '.'), riga['Valore car.']]
                                        print(riga_tabella)
                                        riga_excel = aggiungo_riga_excel(riga_tabella, tabella_eventi)
                                        print('riga tabella quando finisce il ciclo')
                                    except:
                                        pass
                                        arcpy.AddMessage(sys.exc_info()[0])
                                        tabella_errori.append(riga['Sede Tecnica'])
        return tabella_eventi

def procedura_cavidotti(n_id, ROUTE_BIN_C_shp, V_ASSET_S16000_shp, output, INFR_RT_ESTENSIONE_L_shp, INFR_RT_dbf,
                        INFR_RT_INFR_RT_TR_dbf, INFR_RT_INFR_RT_TY_dbf, path_csv, CAVIDOTTI_DB):
    try:
        global tabella_errori
        tabella_errori = []

        Campo_univoco_MDR = "SETE"
        # KM_INIZIO_MDR = "KM__INIZIO"
        KM_INIZIO_MDR = "KM_INI"
        # KM_FINE_MDR_ = "KM__FINE"
        KM_FINE_MDR_ = "KM_FIN"
        KM_INIZIO_EV_TABLE = "KM_INIZIO"
        KM_FINE_EV_TABLE = "KM_FINE"
        Field_univoco_EVENT_TABLE = "SETE"
        ROUTE_BIN_C_Layer = "ROUTE_BIN_C_Layer"
        event_table = ""
        CREATE_ROUTES = r'in_memory/CREATE_ROUTES'
        risultato_segmentazione = "Risultato_segmentazione"
        ROUTE_BIN_C = arcpy.CopyFeatures_management(ROUTE_BIN_C_shp, "in_memory\\ROUTE_BIN_C")
        V_ASSET_S16000 = arcpy.CopyFeatures_management(V_ASSET_S16000_shp, "in_memory\\V_ASSET_S16000")

        arcpy.JoinField_management(ROUTE_BIN_C, "SETE", V_ASSET_S16000, "SEDE_TECNICA",
                                   "SEDE_TECNICA; KM_INI; KM_FIN; S16000_0010")
        # arcpy.JoinField_management(ROUTE_BIN_C_shp, "SETE", V_ASSET_S16000_shp, "SEDE_TECNICA", "SEDE_TECNICA; KM_INI; KM_FIN; S16000_0010")
        # arcpy.FeatureClassToShapefile_conversion(ROUTE_BIN_C_shp,output)

        ROUTE_BIN_C_Layer = arcpy.MakeFeatureLayer_management(ROUTE_BIN_C, ROUTE_BIN_C_Layer)
        fields = (arcpy.ListFields(ROUTE_BIN_C_Layer))
        n_record_join = arcpy.GetCount_management(ROUTE_BIN_C_Layer)

        # arcpy.FeatureClassToShapefile_conversion(ROUTE_BIN_C_Layer,r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni') # NON USATA???

        arcpy.SelectLayerByAttribute_management(ROUTE_BIN_C_Layer, "NEW_SELECTION", "S16000_0010 = 'U' OR S16000_0010= 'D'") # PER SVILUPPO
        # arcpy.SelectLayerByAttribute_management(ROUTE_BIN_C_Layer, "NEW_SELECTION", "S16000_0010 = '3' OR S16000_0010= '2'")  # PER PRODUZIONE ???
        # arcpy.SelectLayerByAttribute_management(ROUTE_BIN_C_Layer, "NEW_SELECTION", "MUIF.INE_LIVE_S16000.S16000_0010 ='UNICO' OR MUIF.INE_LIVE_S16000.S16000_0010='DISPARI'") #????????

        ROUTE_BIN_C_Select = arcpy.CopyFeatures_management(ROUTE_BIN_C_Layer, "in_memory\\ROUTE_BIN_C_Select")
        n_record_select = arcpy.GetCount_management(ROUTE_BIN_C_Select)
        arcpy.AddMessage('n_record_select: ' + n_record_select.getOutput(0))

        try:
            arcpy.AddMessage('Create Route completata.')
            event_table = creoExcel(path_csv)
        except Exception as ex:
            arcpy.AddMessage('Errore nella creazione tabella eventi ' + str(ex))

        try:
            arcpy.CreateRoutes_lr(ROUTE_BIN_C_Select, Campo_univoco_MDR, r'in_memory/CREATE_ROUTES', "TWO_FIELDS",
                                  KM_INIZIO_MDR, KM_FINE_MDR_, "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
            n_record_create_routes = arcpy.GetCount_management(ROUTE_BIN_C_Select)
            arcpy.AddMessage('n_record_create_routes: ' + n_record_create_routes.getOutput(0))
        except Exception as ex:
            arcpy.AddMessage('Errore nella funzione di Create Route ' + str(ex))

        # arcpy.FeatureClassToShapefile_conversion(ROUTE_BIN_C_Select,r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni') # NON USATA ???

        try:
            n_record_create_routes = arcpy.GetCount_management(CREATE_ROUTES)
            arcpy.AddMessage('n_record_create_routes: ' + n_record_create_routes.getOutput(0))
            arcpy.AddMessage(
                Campo_univoco_MDR + ' - ' + Field_univoco_EVENT_TABLE + ' - ' + KM_INIZIO_EV_TABLE + ' - ' + KM_FINE_EV_TABLE)

            risultato_segmentazione = arcpy.MakeRouteEventLayer_lr(CREATE_ROUTES, Campo_univoco_MDR, event_table,
                                                                   Field_univoco_EVENT_TABLE + " LINE " + KM_INIZIO_EV_TABLE + " " + KM_FINE_EV_TABLE,
                                                                   risultato_segmentazione, "", "", "", "", "", "", "")
            n_record_segmentazione_dinamica = arcpy.GetCount_management(risultato_segmentazione)
            arcpy.AddMessage('n_record_segmentazione: ' + n_record_segmentazione_dinamica.getOutput(0))
            arcpy.AddMessage('Fine Segmentazione Dinamica')
        except Exception as ex:
            arcpy.AddMessage('Errore nella segmentazione dinamica' + str(ex))
            # arcpy.FeatureClassToShapefile_conversion(segmentazione_dinamica,r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni') # NON USATA ???

        try:
            # arcpy.CopyFeatures_management(risultato_segmentazione, r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni\Risultato_segmentazione_test.shp') # PRODUZIONE
            arcpy.CopyFeatures_management(risultato_segmentazione, r'\\10.233.71.25\sinfi\connessioni\Risultato_segmentazione_test.shp')  # OFFLINE SVILUPPO
            # arcpy.CopyFeatures_management(risultato_segmentazione, r'/opt/arcgisdata/SINFI/connessioni/Risultato_segmentazione_test.shp')  # ONLINE SVILUPPO

            # arcpy.FeatureClassToShapefile_conversion(risultato_segmentazione, r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni') # PRODUZIONE
            arcpy.FeatureClassToShapefile_conversion(risultato_segmentazione, r'\\10.233.71.25\sinfi\connessioni')  # OFFLINE SVILUPPO
            # arcpy.FeatureClassToShapefile_conversion(risultato_segmentazione, r'/opt/arcgisdata/SINFI/connessioni') # ONLINE SVILUPPO

            # cavidotti = r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni\Risultato_segmentazione.shp' # PRODUZIONE
            cavidotti = r'\\10.233.71.25\sinfi\connessioni\Risultato_segmentazione.shp'  # OFFLINE SVILUPPO
            # cavidotti = r'/opt/arcgisdata/SINFI/connessioni/Risultato_segmentazione.shp' # ONLINE SVILUPPO

            # n_record_copy_feature = arcpy.GetCount_management(r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni\Risultato_segmentazione.shp') # PRODUZIONE
            n_record_copy_feature = arcpy.GetCount_management(r'\\10.233.71.25\sinfi\connessioni\Risultato_segmentazione.shp')  # OFFLINE SVILUPPO
            # n_record_copy_feature = arcpy.GetCount_management(r'/opt/arcgisdata/SINFI/connessioni/Risultato_segmentazione.shp') # ONLINE SVILUPPO
            arcpy.AddMessage(
                'n_record segmentazione dinamica feature class to shapefile : ' + n_record_copy_feature.getOutput(0))

            # n_record_copy_man = arcpy.GetCount_management(r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni\Risultato_segmentazione_test.shp') # PRODUZIONE
            n_record_copy_man = arcpy.GetCount_management(r'\\10.233.71.25\sinfi\connessioni\Risultato_segmentazione_test.shp')  # OFFLINE SVILUPPO
            # n_record_copy_man = arcpy.GetCount_management(r'/opt/arcgisdata/SINFI/connessioni/Risultato_segmentazione_test.shp') # ONLINE SVILUPPO
            arcpy.AddMessage('n_record segmentazione dinamica copy feature : ' + n_record_copy_man.getOutput(0))

        except Exception as ex:
            arcpy.AddMessage('Errore nel Feature class To Shapefile della segmentazione ' + str(ex))
            arcpy.AddMessage(sys.exc_info()[0])

        try:
            sete_assenti = copyParallel(cavidotti, ROUTE_BIN_C_Select)
            arcpy.AddMessage('lista sete errori chilometriche: ')
            arcpy.AddMessage(tabella_errori)
            arcpy.AddMessage('lista sete assenti: ')
            arcpy.AddMessage(sete_assenti)
        except Exception as ex:
            arcpy.AddMessage('Errore nel Copy Parallel ' + str(ex))
            arcpy.AddMessage(sys.exc_info()[1])

        try:
            # INFR_RT_ESTENSIONE_L =arcpy.CopyFeatures_management(cavidotti, 'in_memory/INFR_RT_ESTENSIONE_L')
            INFR_RT_ESTENSIONE_L = arcpy.MultipartToSinglepart_management(cavidotti, 'in_memory/INFR_RT_ESTENSIONE_L')
        except Exception as ex:
            arcpy.AddMessage('Errore nel Copy Features per INFR_RT_ESTENSIONE_L ' + str(ex))
            arcpy.AddMessage(sys.exc_info()[1])
        # arcpy.JoinField_management(INFR_RT_ESTENSIONE_L, "SETE", ROUTE_BIN_C_Select , "SETE", "S16000_0010")

        try:
            arcpy.JoinField_management(INFR_RT_ESTENSIONE_L, "SETE", INFR_RT_ESTENSIONE_L_shp, "CLASSREF", "")
            arcpy.JoinField_management(INFR_RT_ESTENSIONE_L, "CLASSREF", INFR_RT_dbf, "CLASSID", "")
            arcpy.JoinField_management(INFR_RT_ESTENSIONE_L, "CLASSREF", INFR_RT_INFR_RT_TR_dbf, "CLASSREF", "")
            arcpy.JoinField_management(INFR_RT_ESTENSIONE_L, "CLASSREF", INFR_RT_INFR_RT_TY_dbf, "CLASSREF", "")

            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "CLASSREF", "'070002_'+str(autoIncrement() )",
                                            "PYTHON_9.3",
                                            "i =0" + "\\ndef autoIncrement():\\n   global i;\\n   iStart = 1\\n   iInterval = 1\\n   if( i == 0 ):\\n      i = iStart\\n   else:\\n     i=i+ iInterval\\n   return i")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "CLASSID", "!CLASSREF!", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "DATA_INI", "datetime.datetime.now( )", "PYTHON_9.3",
                                            "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "FONTE", "'03'", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "INFR_RT_PC", "'01008081000'", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "INFR_RT_ST", "'01'", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "INFR_RT_UT", "'0202'", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "SCALA", "'04'", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "INFR_RT_TR", "'03'", "PYTHON_9.3", "")
            arcpy.CalculateField_management(INFR_RT_ESTENSIONE_L, "INFR_RT_TY", "'04'", "PYTHON_9.3", "")
            INFR_RT_DBF = arcpy.management.CopyRows(INFR_RT_ESTENSIONE_L, 'in_memory\\INFR_RT_DBF')
        except Exception as ex:
            arcpy.AddMessage('Errore nella valorizzazione campi di INFR_RT_ESTENSIONE_L ' + str(ex))
        try:
            # arcpy.Delete_management(r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni\Risultato_segmentazione.shp') # NON USATA ???
            # arcpy.Delete_management(r'\\rfiappmuf17le.rfiservizi.corp\agsgeoproc\SINFI\connessioni\event_table.dbf') # NON USATA ???
            arcpy.DeleteField_management(INFR_RT_ESTENSIONE_L,
                                         "CLASSID_1; CLASSID; DATA_FIN; DATA_INI; FONTE; SCALA; INFR_RT_PC; INFR_RT_ST; INFR_RT_UT; INFR_RT_TR; INFR_RT_TY; Field1; SEDE_TEC; SETE; KM_INIZIO; KM_FINE; DISTANZA; LATO_DI_PO; ORIG_FID; BINARIO; CLASSREF_1; CLASSREF_2")
        except Exception as ex:
            arcpy.AddMessage('Errore nella valorizzazione campi DBF di INFR_RT_ESTENSIONE_L ' + str(ex))
            arcpy.AddMessage(sys.exc_info()[0])

        try:
            arcpy.FeatureClassToShapefile_conversion(INFR_RT_ESTENSIONE_L, output)
            arcpy.DeleteRows_management(CAVIDOTTI_DB)
            # INFR_RT_ESTENSIONE_L_FINALE=os.path.join(output,"INFR_RT_ESTENSIONE_L.shp")
            # INFR_RT_ESTENSIONE_L_Project=arcpy.Project_management(INFR_RT_ESTENSIONE_L,INFR_RT_ESTENSIONE_L_FINALE,"PROJCS['RDN2008_Italy_zone',GEOGCS['GCS_RDN2008',DATUM['D_Rete_Dinamica_Nazionale_2008',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',7000000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',12.0],PARAMETER['Scale_Factor',0.9985],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "", "", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
            arcpy.DeleteField_management(output + "\INFR_RT_ESTENSIONE_L.shp", "CLASSREF_1")
            arcpy.Append_management(INFR_RT_ESTENSIONE_L, CAVIDOTTI_DB, "NO_TEST")
        except Exception as ex:
            arcpy.AddMessage('sono andato in errore creazione shapefile risultato ' + str(ex))

        result = [output + "\INFR_RT_ESTENSIONE_L.shp", INFR_RT_DBF]
        return result
    except Exception as ex:
        data = {}
        data['risultato'] = []
        data['risultato'].append({'procedura': 'INFR_RT', 'risultato': 'FALSE',
                                  'message': 'Si e\' verificato un errore durante l \'esecuzione della procedura'})

        AggiornamentoTabella(tabella_avanzamento, utente, '', 'ERRORE', id_riga_avanzamento, logger)
        arcpy.AddMessage("Scrittura in Tabella avanzamento - ERRORE.")

        print(json.dumps(data))
        arcpy.AddMessage(json.dumps(data))
        arcpy.SetParameterAsText(1, json.dumps(data))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        arcpy.AddMessage(ex)
        logging.error('Errore nella connessione al database ' + 'main(): Error message {} - Line {}'.format(str(ex),
                                                                                                            exc_tb.tb_lineno))
        logger.error('Errore nella connessione al database ' + 'main(): Error message {} - Line {}'.format(str(ex),
                                                                                                           exc_tb.tb_lineno))
        sys.exit(1)


def main():
    path_csv = r'C:\MUIF\SINFI\Scarichi\Export_AssetS01500.csv'
    path_db = r'C:\MUIF\SINFI\Versionamento Progetto'
    arcpy.env.overwriteOutput = True
    ### LOG ###
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logFileName = os.path.join(path_db + '\\INFR_RT_svil.log')
    logHandler = handlers.TimedRotatingFileHandler(logFileName, when='M', interval=1, backupCount=2)
    log_level = ''
    logHandler.setFormatter(formatter)
    if log_level == 'INFO':
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
    elif log_level == 'ERROR':
        handler.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
    logger.addHandler(logHandler)
    logger.info('File log creato con successo!')

    creoExcel(path_csv)
if __name__ == "__main__":
    arcpy.AddMessage("... Inizio procedura ...")

    main()