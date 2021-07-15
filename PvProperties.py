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
    def appendPvdb(pvdb, local, setor, posicao, nivel, orientacao, sensor):
        if(str(nivel) != "nan"):
            if(sensor in ["PT100", "VWTS6000"]):
                pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}{sensor[0]}:Temp-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                if(sensor == "VWTS6000"):
                    pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}N:Temp-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                else:
                    pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}:Strain{orientacao}-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'uE'}
                    pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}{nivel}:N:Temp-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            else:
                if(sensor in ["PT100", "VWTS6000"]):
                    pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}{sensor[0]}:Temp-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                    if(sensor == "VWTS6000"):
                        pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}N:Temp-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                else:
                    pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}:Strain-Mon"] = {'prec': 3, 'scan': 1, 'unit': 'uE'}
                    pvdb[f"TU-{setor}{local}:SS-Concrete-{posicao}N:Temp-Mon"] ={'prec': 3, 'scan': 1, 'unit': 'C'}
        return pvdb
    
    @staticmethod
    def pvName(mux, canal, ch):
        file = PvProperties.file
        linha = file.loc[((file["Mux"] == mux) & (file["Canal"] == canal))]
        
        if not linha.empty:
            sensor     = cal.muxHeader["mux%d" % mux][canal-1]
            local      = str(linha["Local"].values[0])
            setor      = int(linha["Setor"].values[0])
            posicao    = str(linha["Posição"].values[0]).replace("L", "").replace("P", "")
            nivel      = str(linha["Nível"].values[0])
            orientacao = str(linha["Orientação"].values[0])
            
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
        for i in range((PvProperties.file.shape)[0]):
            local      = PvProperties.file["Local"][i]
            setor      = PvProperties.file["Setor"][i]
            posicao    = PvProperties.file["Posição"][i]
            nivel      = PvProperties.file["Nível"][i]
            orientacao = PvProperties.file["Orientação"][i]
            mux        = PvProperties.file["Mux"][i]
            canal      = PvProperties.file["Canal"][i]
            sensor     = cal.muxHeader["mux%d" % mux][canal-1]
            setor      = ("0" + str(setor)) if setor < 10 else str(setor)
            pvdb       = PvProperties.appendPvdb(pvdb, local, setor, posicao, nivel, orientacao, sensor)
        return pvdb