# coding=utf-8
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

#aggiungere un campo contatore che vada alla fine del vecchio e sia il primo del nuovo così da unire i transetti
def aggiungo_riga_excel(riga, tabella_eventi):
    fields = ['SEDE_TEC', 'SETE', 'KM_INIZIO', 'KM_FINE', 'DISTANZA', 'LATO_DI_PO']
    cursor = arcpy.da.InsertCursor(tabella_eventi, fields)
    cursor.insertRow(riga)
    del cursor
    return True
# Funzione che controlla la Distanza dall'asse BC (metri) con codice caratteristica S01500_0030
def controllo_distanza(sede_tecnica, media_km, path_csv):
    with open(path_csv, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for riga in csv_reader:
            try:
                KM_FINE = riga['Punto finale SI'].replace(',', '.')
                KM_INI = riga['Punto iniziale SI'].replace(',', '.')
                if float(KM_FINE) > float(KM_INI):
                    if riga["Sede Tecnica"] == sede_tecnica and riga['Codice caratteristica'] == 'S01500_0030' and float(media_km) < float(KM_FINE) and float(media_km) > float(KM_INI):
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
                    # Controllo il binario di corsa di riferimento es: 'Valore car.' =  'LO1336-BC-BC03'
                    if riga["Sede Tecnica"] == sede_tecnica and riga['Codice caratteristica'] == 'S01500_0010' and media_km < float(KM_FINE) and media_km > float(KM_INI):
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
                print('sono in controllo sede tecnica')
                SEDI_TECNICHE.append(riga["Sede Tecnica"])
                sede_tecnica = riga["Sede Tecnica"]
                print(riga['Codice caratteristica'])
                logger.info('Sono in controllo sede_tecnica - '+riga["Sede Tecnica"]+' - Codice Caratteristica - '+riga['Codice caratteristica'])
                with open(path_csv, 'r') as csv_file:
                    csv_reader_2 = csv.DictReader(csv_file, delimiter=';')
                    for riga in csv_reader_2:
                        if riga['Codice caratteristica'] == 'S01500_0020' and riga['Sede Tecnica'] == sede_tecnica:
                            try:
                                print('sono in Codice caratteristica lato di posa' + riga['Sede Tecnica'])
                                KM_INI = riga['Punto iniziale SI'].replace(',', '.')
                                KM_FINE = riga['Punto finale SI'].replace(',', '.')
                                if KM_INI > KM_FINE:
                                    x = KM_INI
                                    KM_INI = KM_FINE
                                    KM_FINE = x
                                media_km = (float(KM_INI) + float(KM_FINE)) / 2
                                sete = controllo_binario(sede_tecnica, media_km, path_csv)
                                print('KM_FINE LATO DI POSA ' + KM_FINE)
                                logger.info('Sono in caratteristica lato di posa - ' +riga['Codice caratteristica'] + ' - Sede Tecnica - ' + riga['Sede Tecnica']+' - KM_FINE LATO DI POSA ' + KM_FINE)
                                risultato = controllo_chilometriche(sede_tecnica, 'S01500_0030', KM_INI, KM_FINE, path_csv)
                            except:
                                arcpy.AddMessage(sys.exc_info()[0])
                                tabella_errori.append(riga['Sede Tecnica'])
                                logger.warning('SONO ENTRATO IN ECCEZIONE SULLA SETE - ' + riga['Sede Tecnica'])
                            if risultato == False:
                                distanza = controllo_distanza(sede_tecnica, media_km, path_csv)
                                try:
                                    riga_tabella = [riga['Sede Tecnica'], sete, KM_INI, KM_FINE, distanza.replace(',', '.'), riga['Valore car.']]
                                    print('riga tabella se non e presente un intervallo minore')
                                    # Tolto riga_excel =
                                    aggiungo_riga_excel(riga_tabella, tabella_eventi)
                                except:
                                    arcpy.AddMessage(sys.exc_info()[0])
                                    tabella_errori.append(riga['Sede Tecnica'])
                            else:
                                KM_INIZIO = KM_INI
                                contatore = 0

                                while risultato != False:
                                    contatore = contatore + 1
                                    print(contatore)
                                    KM_FIN = risultato[0]
                                    try:
                                        riga_tabella = [riga['Sede Tecnica'], sete, float(KM_INIZIO.replace(',', '.')),float(KM_FIN.replace(',', '.')), risultato[1].replace(',', '.'),riga['Valore car.']]
                                        print(riga_tabella)
                                        print('riga tabella se e\' presente un intervallo minore')
                                        aggiungo_riga_excel(riga_tabella, tabella_eventi)
                                        print(KM_FIN)
                                        KM_INIZIO = KM_FIN
                                        risultato = controllo_chilometriche(sede_tecnica, 'S01500_0030', KM_INIZIO, KM_FINE, path_csv)
                                        print(KM_FINE)
                                    except:
                                        arcpy.AddMessage(sys.exc_info()[0])
                                        tabella_errori.append(riga['Sede Tecnica'])
                                        break
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
                                    arcpy.AddMessage(sys.exc_info()[0])
                                    tabella_errori.append(riga['Sede Tecnica'])
                                    break
        return tabella_eventi


def main():
    path_csv = r'C:\MUIF\SINFI\Scarichi\Export_AssetS01500.csv'
    path_db = r'C:\MUIF\SINFI\Versionamento Progetto'
    arcpy.env.overwriteOutput = True
    ### LOG ###
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
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