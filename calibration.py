"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create october, 16, 2020
    @title: CSV functions
"""

import numpy as np

class Calibration():
    
    VWTS6000 = {
        # Mux ID: 3
        3:  {4:  [-2.98789e-7, 0.039225853, -242.5006592],
             5:  [1.52639e-8, 0.03431087, -228.187216],
             6:  [7.04211e-8, 0.03471572, -227.3231565],
             7:  [-9.87936e-8, 0.036047576, -238.9470578],
             8:  [-1.36463e-7, 0.037995787, -253.7599344],
             13: [-1.99876e-7, 0.03760965, -220.8731282],
             14: [-9.47459e-8, 0.035665594, -236.7894379],
             15: [-1.35683e-7, 0.036854729, -235.1161502]},
        # Mux ID: 4
        4:  {4:  [2.08474e-8, 0.033564626, -223.6222522],
             5:  [-3.12404e-7, 0.03983653, -244.9547066],
             6:  [-2.63468e-7, 0.03867361, -239.253117],
             11: [-5.2847e-8, 0.037371289, -261.509601],
             12: [-1.52665e-7, 0.037543817,-244.5883589],
             13: [-1.58531e-7, 0.036050692, -210.4538973]},
        # Mux ID: 7
        7:  {4:  [-4.66532e-7, 0.043657907, -270.9378536],
             5:  [-4.38558e-7, 0.041729087, -250.4316125],
             6:  [1.51616e-8, 0.036574251, -279.810059],
             7:  [-4.76082e-7, 0.042974268, -255.9242929],
             8:  [-2.99452e-7, 0.039742468, -251.3515976],
             13: [-9.53227e-8, 0.037443901, -242.8079079],
             14: [-1.233e-7, 0.036684294, -240.9130387],
             15: [-2.97906e-7, 0.040114726, -265.6483637]},
        # Mux ID: 8
        8:  {4:  [-3.54882e-7, 0.040337059, -253.3157031],
             5:  [-2.813e-7, 0.041161193, -258.4244976],
             6:  [-3.43888e-7, 0.041002641, -257.2407047],
             11: [-2.66833e-7, 0.038971975, -238.4481713],
             12: [-1.20043e-6, 0.057831838, -311.779984],
             13: [-3.23709e-7, 0.040509445, -240.2341397]},
        # Mux ID: 11
        11: {4:  [-4.2309e-7, 0.04055173, -246.6141863],
             5:  [-4.83518e-7, 0.046254938, -281.8389211],
             6:  [-1.4784e-7, 0.038232489, -250.8263202],
             7:  [-1.89296e-7, 0.036369374, -222.7478814],
             8:  [-1.32633e-8, 0.033276899, -218.3257014],
             13: [-1.70582e-7, 0.036713823, -237.4024472],
             14: [-3.03062e-7, 0.041256792, -260.7602262],
             15: [ 1.36105e-7, 0.032884471, -221.2936402]},
        # Mux ID: 12
        12: {4: [-4.88729e-8, 0.036314166, -254.5576994],
             5: [-1.39758e-6, 0.062096759, -352.7987036],
             6: [-1.49674e-7, 0.035982414, -235.0948592],
             11: [-4.63448e-8, 0.036290834, -229.9578029],
             12: [-7.59517e-8, 0.03755655, -245.6399032],
             13: [-1.46184e-7, 0.036644825, -226.0614626]},
        # Mux ID: 15
        15: {1:  [-2.11601e-7, 0.039820217, -251.6517896],
             2:  [-2.23281e-7, 0.037163667, -231.0169151],
             3:  [-4.00154e-8, 0.034944514, -227.828874],
             8:  [-1.89559e-6, 0.066202064, -327.2442413],
             9:  [-2.05463e-7, 0.035936504, -220.1327198],
             10: [-1.89628e-6, 0.069955263, -350.3308039],
             15: [-7.02214e-7, 0.0477785, -282.1125598],
             16: [-3.6437e-7, 0.041319565, -240.976406]},
        # Mux ID: 16
        16: {1:  [-1.74604e-7, 0.038046792, -244.7712586]},
        # Mux ID: 17
        17: {4:  [-2.07197e-7, 0.037118264, -233.2244804],
             5:  [-2.19825e-9, 0.035348566, -237.568356],
             6:  [-3.90866e-7, 0.042298576, -249.57956],
             7:  [-3.18826e-8, 0.035616745, -249.2119137],
             8:  [-4.35109e-7, 0.044572082, -268.7152509]},
        # Mux ID: 18
        18: {2:  [-3.58366e-7, 0.039449219, -207.7151822],
             6:  [-1.14746e-7, 0.03678056, -224.3130529],
             13: [-3.27516e-7, 0.040808519, -244.8217741]},
        # Mux ID: 19
        19: {1:  [-5.83097e-8, 0.03487002, -216.1738525],
             2:  [-1.63786e-7, 0.03807495, -237.2669056],
             3:  [-2.90318e-7, 0.042138932, -256.0530494],
             4:  [-3.13441e-7, 0.042553775, -279.8647834],
             15: [-1.93478e-7, 0.04000436, -257.442918]},
        # Mux ID: 20
        20: {1:  [-1.41347e-6, 0.060797805, -325.3810089],
             8:  [-6.22927e-7, 0.045315268, -262.2948921],
             9:  [-1.40326e-7, 0.0388211, -253.4445563],
             12: [-3.53588e-7, 0.040869212, -254.1815812]},
        # Mux ID: 21
        21: {5:  [-2.52784e-7, 0.038443437, -223.1980118],
             12: [-9.12718e-8, 0.037669652, -255.4380412],
             15: [-1.10761e-7, 0.037751836, -257.7699651]},
        # Mux ID: 22
        22: {1:  [-2.2043e-8, 0.036610363, -227.8900913],
             2:  [-1.85825e-7, 0.040411907, -260.5421328],
             3:  [-5.89313e-7, 0.044512917, -197.930912],
             4:  [-4.93358e-8, 0.037260898, -226.039765],
             5:  [-1.78662e-7, 0.038046515, -241.5079754],
             8:  [-1.32629e-7, 0.040292832, -284.8988303]},
        # Mux ID: 23
        23: {2:  [-3.87478e-7, 0.040384905, -210.1407981],
             4:  [-4.54671e-7, 0.044138476, -262.1216238]},
        # Mux ID: 24
        24: {5:  [-2.09242e-7, 0.039928226, -255.967896],
             7:  [-2.4051e-7, 0.042028198, -262.5231372]},
        # Mux ID: 26
        26: {3:  [-2.82335e-7, 0.041231588, -241.5843419],
             5:  [-3.66451e-7, 0.042727783, -254.6774709],
             6:  [-3.18697e-7, 0.041241311, -242.2447954]},
        # Mux ID: 28
        28: {6:  [2.77375e-8, 0.034275038, -224.7030972],
             7:  [-3.20939e-7, 0.041638045, -259.0935866],
             12: [-2.50241e-7, 0.041387677, -247.8616957]},
        # Mux ID: 29
        29: {1:  [-3.56457e-7, 0.043418048, -272.1141463],
             3:  [-3.71178e-7, 0.043098353, -256.3350486]}
        }
    
    """ Fatores p/ conversão de dados brutos dos strain-gauges VW2100
    - Formato das variáveis 'VW2100_BATCH5x': [Batch Factor, Gauge Factor]  """
    
    VWS2100_BATCH57 = [0.935, 3.718]
    VWS2100_BATCH58 = [0.924, 3.718]
    
    """ Coeficientes do polinomio de conversão dos sensores PT100 """
    
    PT100_A = 0.0010664
    PT100_B = 2.3419
    PT100_C = -244.83
    
    """ Coeficientes da fórmula de Steinhart & Hart, disponível no site da Geosense """
    
    NTC_A = 1.4051e-3
    NTC_B = 2.369e-4
    NTC_C = 1.019e-7
    
    """ Implementação dos cabeçalhos dos arquivos .CSV """
    MUXactivated = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,29,0]
    
    muxHeader = {
            "mux1":  ["PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100"],
            "mux2":  ["PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable", "Disable", "Disable"],
            "mux3":  ["PT100", "PT100", "PT100", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100"],
            "mux4":  ["VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100"],
            "mux5":  ["VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100"],
            "mux6":  ["PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable", "Disable"],
            "mux7":  ["PT100", "PT100", "PT100", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100"],
            "mux8":  ["VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100"],
            "mux9":  ["VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100"],
            "mux10": ["PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable", "Disable"],
            "mux11": ["PT100", "PT100", "PT100", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100"],
            "mux12": ["VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100"],
            "mux13": ["VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100"],
            "mux14": ["PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable", "Disable"],
            "mux15": ["VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000"],
            "mux16": ["VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable", "Disable", "Disable"],
            "mux17": ["PT100", "PT100", "PT100", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000",  "VWS2100", "VWS2100", "VWS2100", "VWS2100"],
            "mux18": ["VWS2100", "VWTS6000", "PT100", "PT100", "VWS2100", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "PT100", "PT100", "VWS2100", "VWTS6000", "VWS2100", "VWS2100", "VWS2100"],
            "mux19": ["VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWS2100"],
            "mux20": ["VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWTS6000"],
            "mux21": ["VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWTS6000", "VWS2100", "VWS2100", "VWTS6000", "Disable"],
            "mux22": ["VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWTS6000", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "PT100", "Disable", "Disable"],
            "mux23": ["VWS2100", "VWTS6000", "PT100", "VWTS6000", "VWS2100", "VWS2100", "PT100", "PT100", "Disable", "Disable", "Disable", "Disable"],
            "mux24": ["PT100", "PT100", "VWS2100", "VWS2100", "VWTS6000", "PT100", "VWTS6000", "VWS2100", "VWS2100", "PT100", "PT100", "VWS2100", "VWS2100", "PT100", "PT100", "PT100"],
            "mux25": ["VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable", "Disable", "Disable", "Disable", "Disable", "Disable", "Disable", "Disable"],
            "mux26": ["VWS2100", "VWS2100", "VWTS6000", "VWS2100", "VWTS6000", "VWTS6000", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "Disable",  "VWS2100", "VWS2100", "VWS2100", "VWS2100"],
            "mux27": ["VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100", "VWS2100"],
            "mux28": ["PT100", "PT100", "PT100", "VWS2100", "VWS2100", "VWTS6000", "VWTS6000", "PT100", "PT100", "VWS2100", "VWS2100", "VWTS6000", "VWS2100", "VWS2100", "PT100", "PT100"],
            "mux29": ["VWTS6000", "PT100", "VWTS6000", "VWS2100", "VWS2100", "PT100", "PT100", "PT100", "PT100", "PT100", "PT100", "VWS2100", "VWS2100", "PT100", "PT100", "VWS2100"],
        }
    
    G8header = ["Datetime", "ID", "Volt. [V]", "Temp. [°C]"]
    
    aux = []
    
    """ relação de muxs e número de canais """
    
    mux_ch = [8,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,12,16,16,12,16,16,12,16,16,16,12,16,16]

    @staticmethod
    def convertPT100(value):
        try:
            value = float(value)
            # Convertion to Celsius degrees
            convertion = Calibration.PT100_A * value**2 + Calibration.PT100_B * value + Calibration.PT100_C
            return round(convertion, 3)
        except:
            return "erro"
    
    @staticmethod
    def convertVWTS6000(muxId, channel, value):
        try:
            value = float(value)
            VWTS6000_A = Calibration.VWTS6000[muxId][channel][0]
            VWTS6000_B = Calibration.VWTS6000[muxId][channel][1]
            VWTS6000_C = Calibration.VWTS6000[muxId][channel][2]
            # Convertion from Hz to uHz^2
            value = (value**2) * (10**(-3))
            # Convertion to Celsius degrees
            convertion = VWTS6000_A * value**2 + VWTS6000_B * value + VWTS6000_C
            return round(convertion, 3)
        except:
            return "erro"
    
    @staticmethod
    def convertVWS2100(channel, value):
        try:
            value = float(value)
            if channel in [27]:
                VWS2100_BF = Calibration.VWS2100_BATCH58[0]
                VWS2100_GF = Calibration.VWS2100_BATCH58[1]
            else:
                VWS2100_BF = Calibration.VWS2100_BATCH57[0]
                VWS2100_GF = Calibration.VWS2100_BATCH57[1]
            # Convertion to uE
            convertion = ((value**2)/1000) * VWS2100_BF * VWS2100_GF
            return round(convertion, 3)
        except:
            return "erro"
    
    @staticmethod
    def convertChannelA(muxId, channel, value):
        if value != "Dis.":
            convertionType = Calibration.muxHeader["mux%d" % muxId][channel - 1]
            if convertionType == "PT100":
                return Calibration.convertPT100(value)
            elif convertionType == "VWTS6000":
                return Calibration.convertVWTS6000(muxId, channel, value)
            elif convertionType == "VWS2100":
                return Calibration.convertVWS2100(channel, value)
        else:
            return "Dis."
    
    @staticmethod
    def convertChannelB(value):
        try:
            value = float(value)
            # Convertion to Celsius degrees
            convertion = (Calibration.NTC_A + Calibration.NTC_B * np.log(float(value)) 
                             + Calibration.NTC_C * (np.log(float(value))**3))
            convertion = convertion**(-1) - 273.2
            return round(convertion, 3)
        except:
            return "erro"