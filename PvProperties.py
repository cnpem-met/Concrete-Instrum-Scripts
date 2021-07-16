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
    def pvName(mux, canal, ch):
        file = PvProperties.file
        linha = file.loc[((file["Mux"] == mux) & (file["Canal"] == canal))]
        
        if not linha.empty:
            sensor     = cal.muxHeader["mux%d" % mux][canal-1]
            local      = str(linha["Local"].values[0])
            setor      = int(linha["Setor"].values[0])
            setor      = ("0" + str(setor)) if setor < 10 else str(setor)
            posicao    = (str(linha["Posição"].values[0])).replace("L", "").replace("P", "")
            nivel      = str(linha["Nível"].values[0])
            nivel      = "" if nivel == "nan" else nivel
            orientacao = str(linha["Orientação"].values[0])
            orientacao = "" if orientacao == "nan" else orientacao
            
            if((sensor == "PT100" or sensor == "VWTS6000") and ch == "A"):
                return (f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}{sensor[0]}:Temp-Mon")
            if(sensor == "VWTS6000" and ch == "B"):
                return (f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}N:Temp-Mon")
            if(sensor == "VWS2100" and ch == "A"):
                return (f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}:Strain{orientacao}-Mon")
            if(sensor == "VWS2100" and ch == "B"):
                return (f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}N:Temp-Mon")

    @staticmethod
    def pvdb():
        pvdb = {}
        for index, row in PvProperties.file.iterrows():
            mux        = row["Mux"]
            canal      = row["Canal"]
            sensor     = cal.muxHeader["mux%d" % mux][canal-1]
            print(mux, canal, sensor)
            if("PT100" in sensor):
                pvdb[PvProperties.pvName(mux, canal, "A").replace("TU-", "")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            elif ("VWTS6000" in sensor):
                pvdb[PvProperties.pvName(mux, canal, "A").replace("TU-", "")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                pvdb[PvProperties.pvName(mux, canal, "B").replace("TU-", "")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            else:
                pvdb[PvProperties.pvName(mux, canal, "A").replace("TU-", "")] = {'prec': 3, 'scan': 1, 'unit': 'uE'}
                pvdb[PvProperties.pvName(mux, canal, "B").replace("TU-", "")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            print(pvdb)

        return pvdb