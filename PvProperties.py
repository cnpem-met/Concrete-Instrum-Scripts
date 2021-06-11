# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:44:26 2020

@author: leona
"""

import pandas as pd
from calibration import Calibration as cal

class PvProperties():
    
    file = pd.read_excel("pvs.xlsx")
    
    @staticmethod
    def appendPvdb(pvdb, tipo, placa, posicao, nivel, canal, sensor):
        if(str(nivel) != "nan"):
            if sensor == "PT100":
                pvdb["%s:%s:TEMP:%s%s:RTD" % (tipo, placa, posicao, nivel)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            elif sensor == "VWS2100":
                pvdb["%s:%s:STRAIN:%s%s" % (tipo, placa, posicao, nivel)] = {'prec': 3, 'scan': 1, 'unit': 'uE'}
                pvdb["%s:%s:TEMP:%s%s:NTC" % (tipo, placa, posicao, nivel)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            else:
                pvdb["%s:%s:TEMP:%s%s:VW" % (tipo, placa, posicao, nivel)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                pvdb["%s:%s:TEMP:%s%s:NTC" % (tipo, placa, posicao, nivel)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
        else:
            if sensor == "PT100":
                pvdb["%s:%s:TEMP:%s:RTD:%s" % (tipo, placa, posicao, canal)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            elif sensor == "VWS2100":
                pvdb["%s:%s:STRAIN:%s:%s" % (tipo, placa, posicao, canal)] = {'prec': 3, 'scan': 1, 'unit': 'uE'}
                pvdb["%s:%s:TEMP:%s:NTC:%s" % (tipo, placa, posicao, canal)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            else:
                pvdb["%s:%s:TEMP:%s:VW:%s" % (tipo, placa, posicao, canal)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                pvdb["%s:%s:TEMP:%s:NTC:%s" % (tipo, placa, posicao, canal)] = {'prec': 3, 'scan': 1, 'unit': 'C'}
        return pvdb
    
    @staticmethod
    def pvName(mux, canal, ch):
        file = PvProperties.file
        linha = file.loc[((file["mux"] == mux) & (file["canal"] == canal))]
        if not linha.empty:
            sensor = cal.muxHeader["mux%d" % mux][canal-1]
            tipo = linha["tipo"].values[0]
            placa = linha["placa"].values[0]
            posicao = linha["posicao"].values[0]
            nivel = linha["nivel"].values[0]
            
            if(str(nivel) != "nan"):
                if sensor == "PT100":
                    return ("%s:%s:TEMP:%s%s:RTD" % (tipo, placa, posicao, nivel))
                elif sensor == "VWS2100":
                    if ch == "A":
                        return ("%s:%s:STRAIN:%s%s" % (tipo, placa, posicao, nivel))
                    else:
                        return ("%s:%s:TEMP:%s%s:NTC" % (tipo, placa, posicao, nivel))
                else:
                    if ch == "A":
                        return ("%s:%s:TEMP:%s%s:VW" % (tipo, placa, posicao, nivel))
                    else:
                        return ("%s:%s:TEMP:%s%s:NTC" % (tipo, placa, posicao, nivel))
            else:
                if sensor == "PT100":
                    return ("%s:%s:TEMP:%s:RTD:%s" % (tipo, placa, posicao, canal))
                elif sensor == "VWS2100":
                    if ch == "A":
                        return ("%s:%s:STRAIN:%s:%s" % (tipo, placa, posicao, canal))
                    else:
                        return ("%s:%s:TEMP:%s:NTC:%s" % (tipo, placa, posicao, canal))
                else:
                    if ch == "A":
                        return ("%s:%s:TEMP:%s:VW:%s" % (tipo, placa, posicao, canal))
                    else:
                        return ("%s:%s:TEMP:%s:NTC:%s" % (tipo, placa, posicao, canal))
        else:
            return "Dis."

    @staticmethod
    def pvdb():
        pvdb = {}
        for i in range((PvProperties.file.shape)[0]):
            tipo = PvProperties.file["tipo"][i]
            placa = PvProperties.file["placa"][i]
            posicao = PvProperties.file["posicao"][i]
            nivel = PvProperties.file["nivel"][i]
            mux = PvProperties.file["mux"][i]
            canal = PvProperties.file["canal"][i]
            sensor = cal.muxHeader["mux%d" % mux][canal-1]
            pvdb = PvProperties.appendPvdb(pvdb, tipo, placa, posicao, nivel, canal, sensor)
        return pvdb