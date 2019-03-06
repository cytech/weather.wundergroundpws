# -*- coding: utf-8 -*-

from __future__ import division
from builtins import str
from past.utils import old_div
import sys, math
import xbmc

LANGUAGE = sys.modules[ "__main__" ].LANGUAGE

#http://www.wunderground.com/weather/api/d/docs?d=language-support
        # kodi lang name         # wu code
LANG = { 'afrikaans'             : 'AF',
         'albanian'              : 'AL',
         'amharic'               : 'EN', # AM is n/a, use AR or EN?
         'arabic'                : 'AR',
         'armenian'              : 'HY',
         'azerbaijani'           : 'AZ',
         'basque'                : 'EU',
         'belarusian'            : 'BY',
         'bosnian'               : 'CR', # BS is n/a, use CR or SR?
         'bulgarian'             : 'BU',
         'burmese'               : 'MY',
         'catalan'               : 'CA',
         'chinese (simple)'      : 'CN',
         'chinese (traditional)' : 'TW',
         'croatian'              : 'CR',
         'czech'                 : 'CZ',
         'danish'                : 'DK',
         'dutch'                 : 'NL',
         'english'               : 'LI',
         'english (us)'          : 'EN',
         'english (australia)'   : 'LI',
         'english (new zealand)' : 'LI',
         'esperanto'             : 'EO',
         'estonian'              : 'ET',
         'faroese'               : 'DK', # FO is n/a, use DK
         'finnish'               : 'FI',
         'french'                : 'FR',
         'galician'              : 'GZ',
         'german'                : 'DL',
         'greek'                 : 'GR',
         'georgian'              : 'KA',
         'hebrew'                : 'IL',
         'hindi (devanagiri)'    : 'HI',
         'hungarian'             : 'HU',
         'icelandic'             : 'IS',
         'indonesian'            : 'ID',
         'italian'               : 'IT',
         'japanese'              : 'JP',
         'korean'                : 'KR',
         'latvian'               : 'LV',
         'lithuanian'            : 'LT',
         'macedonian'            : 'MK',
         'malay'                 : 'EN', # MS is n/a, use EN
         'malayalam'             : 'EN', # ML is n/a, use EN
         'maltese'               : 'MT',
         'maori'                 : 'MI',
         'mongolian (mongolia)'  : 'MN',
         'norwegian'             : 'NO',
         'ossetic'               : 'EN', # OS is n/a, use EN
         'persian'               : 'FA',
         'persian (iran)'        : 'FA',
         'polish'                : 'PL',
         'portuguese'            : 'BR',
         'portuguese (brazil)'   : 'BR',
         'romanian'              : 'RO',
         'russian'               : 'RU',
         'serbian'               : 'SR',
         'serbian (cyrillic)'    : 'SR',
         'silesian'              : 'PL', # SZL is n/a, use PL or EN?
         'sinhala'               : 'EN', # SI is n/a, use EN?
         'slovak'                : 'SK',
         'slovenian'             : 'SL',
         'spanish'               : 'SP',
         'spanish (argentina)'   : 'SP',
         'spanish (mexico)'      : 'SP',
         'swedish'               : 'SW',
         'tajik'                 : 'FA', # TG is n/a, use FA or EN?
         'tamil (india)'         : 'EN', # TA is n/a, use EN
         'telugu'                : 'EN', # TE is n/a, use EN
         'thai'                  : 'TH',
         'turkish'               : 'TU',
         'ukrainian'             : 'UA',
         'uzbek'                 : 'UZ',
         'vietnamese'            : 'VU',
         'welsh'                 : 'CY'}

                # WU    KODI    description
WEATHER_CODES = {0: '0',  # Tornado	Forecast	Night + Day
                 1: '1',  # Tropical Storm	Forecast + Observations	Night + Day
                 2: '2',  # Hurricane	Forecast	Night + Day
                 3: '3',  # Strong Storms	Forecast	Night + Day
                 4: '4',  # Thunder and Hail	Forecast + Observations	Night + Day
                 5: '5',  # Rain to Snow Showers	Forecast + Observations	Night + Day
                 6: '6',  # Rain / Sleet	Forecast + Observations	Night + Day
                 7: '7',  # Wintry Mix Snow / Sleet	Forecast + Observations	Night + Day
                 8: '8',  # Freezing Drizzle	Forecast + Observations	Night + Day
                 9: '9',  # Drizzle	Forecast + Observations	Night + Day
                 10: '10',  # Freezing Rain	Forecast + Observations	Night + Day
                 11: '11',  # Light Rain	Forecast + Observations	Night + Day
                 12: '12',  # Rain	Forecast + Observations	Night + Day
                 13: '13',  # Scattered Flurries	Forecast + Observations	Night + Day
                 14: '14',  # Light Snow	Forecast + Observations	Night + Day
                 15: '15',  # Blowing / Drifting Snow	Forecast + Observations	Night + Day
                 16: '16',  # Snow	Forecast + Observations	Night + Day
                 17: '17',  # Hail	Forecast + Observations	Night + Day
                 18: '18',  # Sleet	Forecast + Observations	Night + Day
                 19: '19',  # Blowing Dust / Sandstorm	Forecast + Observations	Night + Day
                 20: '20',  # Foggy	Forecast + Observations	Night + Day
                 21: '21',  # Haze / Windy	Forecast + Observations	Night + Day
                 22: '22',  # Smoke / Windy	Forecast + Observations	Night + Day
                 23: '23',  # Breezy	Forecast	Night + Day
                 24: '24',  # Blowing Spray / Windy	Forecast + Observations	Night + Day
                 25: '25',  # Frigid / Ice Crystals	Forecast + Observations	Night + Day
                 26: '26',  # Cloudy	Forecast + Observations	Night + Day
                 27: '27',  # Mostly Cloudy	Forecast + Observations	Night + Day
                 28: '28',  # Mostly Cloudy	Forecast + Observations	Day
                 29: '29',  # Partly Cloudy	Forecast + Observations	Night
                 30: '30',  # Partly Cloudy	Forecast + Observations	Day
                 31: '31',  # Clear	Forecast + Observations	Night
                 32: '32',  # Sunny	Forecast + Observations	Day
                 33: '33',  # Fair / Mostly Clear	Forecast + Observations	Night
                 34: '34',  # Fair / Mostly Sunny	Forecast + Observations	Day
                 35: '35',  # Mixed Rain & Hail	Forecast	Day
                 36: '36',  # Hot	Forecast	Day
                 37: '37',  # Isolated Thunderstorms	Forecast	Day
                 38: '38',  # Thunderstorms	Forecast + Observations	Night + Day
                 39: '39',  # Scattered Showers	Forecast	Day
                 40: '40',  # Heavy Rain	Forecast + Observations	Night + Day
                 41: '41',  # Scattered Snow Showers	Forecast	Day
                 42: '42',  # Heavy Snow	Forecast + Observations	Night + Day
                 43: '43',  # Blizzard	Forecast	Night + Day
                 44: 'na',  # Not Available (N/A)	Forecast	Night + Day
                 45: '45',  # Scattered Showers	Forecast	Night
                 46: '46',  # Scattered Snow Showers	Forecast	Night
                 47: '47',  # Scattered Thunderstorms	Forecast + Observations	Night + Day
                 }

MONTH = { 1  : xbmc.getLocalizedString(51),
          2  : xbmc.getLocalizedString(52),
          3  : xbmc.getLocalizedString(53),
          4  : xbmc.getLocalizedString(54),
          5  : xbmc.getLocalizedString(55),
          6  : xbmc.getLocalizedString(56),
          7  : xbmc.getLocalizedString(57),
          8  : xbmc.getLocalizedString(58),
          9  : xbmc.getLocalizedString(59),
          10 : xbmc.getLocalizedString(60),
          11 : xbmc.getLocalizedString(61),
          12 : xbmc.getLocalizedString(62)}

WEEKDAY = { 0  : xbmc.getLocalizedString(41),
            1  : xbmc.getLocalizedString(42),
            2  : xbmc.getLocalizedString(43),
            3  : xbmc.getLocalizedString(44),
            4  : xbmc.getLocalizedString(45),
            5  : xbmc.getLocalizedString(46),
            6  : xbmc.getLocalizedString(47)}

SEVERITY = { 'W' : LANGUAGE(32510),
             'A' : LANGUAGE(32511),
             'Y' : LANGUAGE(32512),
             'S' : LANGUAGE(32513),
             'O' : LANGUAGE(32514),
             'F' : LANGUAGE(32515),
             'N' : LANGUAGE(32516),
             'L' :'', # no idea
             ''  : ''}

def MOONPHASE(age, percent):
    if (percent == 0) and (age == 0):
        phase = LANGUAGE(32501)
    elif (age < 17) and (age > 0) and (percent > 0) and (percent < 50):
        phase = LANGUAGE(32502)
    elif (age < 17) and (age > 0) and (percent == 50):
        phase = LANGUAGE(32503)
    elif (age < 17) and (age > 0) and (percent > 50) and (percent < 100):
        phase = LANGUAGE(32504)
    elif (age > 0) and (percent == 100):
        phase = LANGUAGE(32505)
    elif (age > 15) and (percent < 100) and (percent > 50):
        phase = LANGUAGE(32506)
    elif (age > 15) and (percent == 50):
        phase = LANGUAGE(32507)
    elif (age > 15) and (percent < 50) and (percent > 0):
        phase = LANGUAGE(32508)
    else:
        phase = ''
    return phase

def KPHTOBFT(spd):
    if (spd < 1.0):
        bft = '0'
    elif (spd >= 1.0) and (spd < 5.6):
        bft = '1'
    elif (spd >= 5.6) and (spd < 12.0):
        bft = '2'
    elif (spd >= 12.0) and (spd < 20.0):
        bft = '3'
    elif (spd >= 20.0) and (spd < 29.0):
        bft = '4'
    elif (spd >= 29.0) and (spd < 39.0):
        bft = '5'
    elif (spd >= 39.0) and (spd < 50.0):
        bft = '6'
    elif (spd >= 50.0) and (spd < 62.0):
        bft = '7'
    elif (spd >= 62.0) and (spd < 75.0):
        bft = '8'
    elif (spd >= 75.0) and (spd < 89.0):
        bft = '9'
    elif (spd >= 89.0) and (spd < 103.0):
        bft = '10'
    elif (spd >= 103.0) and (spd < 118.0):
        bft = '11'
    elif (spd >= 118.0):
        bft = '12'
    else:
        bft = ''
    return bft

def CELSIUStoFAHR(temp):
    if temp is None:
        return 'na'
    return 9/5 * temp + 32

def wind_deg_to_card(deg):
    arr = ['NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
    return arr[int(abs((deg - 11.25) % 360) / 22.5)]

def FEELS_LIKE(T, V=0, R=0, ext=''):
    if T <= 10 and V >= 8:
        FeelsLike = WIND_CHILL(T, V)
    elif T >= 26:
        FeelsLike = HEAT_INDEX(T, R)
    else:
        FeelsLike = T
    if ext == 'F':
        FeelsLike = FeelsLike * 1.8 + 32
    return str(int(round(FeelsLike)))

#### thanks to FrostBox @ http://forum.kodi.tv/showthread.php?tid=114637&pid=937168#pid937168
def WIND_CHILL(T, V):
    FeelsLike = ( 13.12 + ( 0.6215 * T ) - ( 11.37 * V**0.16 ) + ( 0.3965 * T * V**0.16 ) )
    return FeelsLike

### https://en.wikipedia.org/wiki/Heat_index
def HEAT_INDEX(T, R):
    T = T * 1.8 + 32 # calaculation is done in F
    FeelsLike = -42.379 + (2.04901523 * T) + (10.14333127 * R) + (-0.22475541 * T * R) + (-0.00683783 * T**2) + (-0.05481717 * R**2) + (0.00122874 * T**2 * R) + (0.00085282 * T * R**2) + (-0.00000199 * T**2 * R**2)
    FeelsLike = (FeelsLike - 32) / 1.8 # convert to C
    return FeelsLike

#### thanks to FrostBox @ http://forum.kodi.tv/showthread.php?tid=114637&pid=937168#pid937168
def DEW_POINT(Tc=0, RH=93, ext='', minRH=( 0, 0.075 )[ 0 ]):
    Es = 6.11 * 10.0**( 7.5 * Tc / ( 237.7 + Tc ) )
    RH = RH or minRH
    E = old_div(( RH * Es ), 100)
    try:
        DewPoint = old_div(( -430.22 + 237.7 * math.log( E ) ), ( -math.log( E ) + 19.08 ))
    except ValueError:
        DewPoint = 0
    if ext == 'F':
        DewPoint = DewPoint * 1.8 + 32
    return str(int(round(DewPoint)))