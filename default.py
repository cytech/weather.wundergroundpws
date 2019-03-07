# -*- coding: utf-8 -*-

# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with Kodi; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html


from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from past.utils import old_div
import os, sys, socket, unicodedata, urllib.request, urllib.error, urllib.parse, time, gzip
import datetime
from io import StringIO
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import json

ADDON      = xbmcaddon.Addon()
ADDONNAME  = ADDON.getAddonInfo('name')
ADDONID    = ADDON.getAddonInfo('id')
CWD        = ADDON.getAddonInfo('path').decode("utf-8")
VERSION    = ADDON.getAddonInfo('version')
LANGUAGE   = ADDON.getLocalizedString
RESOURCE   = xbmc.translatePath( os.path.join( CWD, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
PROFILE    = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')
API        = ADDON.getSetting('API')
STATIONNAME= ADDON.getSetting('Location1')
STATIONID  = ADDON.getSetting('Location1id')
FORECASTLAT= ADDON.getSetting('Location1lat')
FORECASTLON= ADDON.getSetting('Location1lon')

sys.path.append(RESOURCE)

from utilities import *
from wunderground import wundergroundapi

FORMAT           = 'json'
DEBUG            = ADDON.getSetting('Debug')
XBMC_PYTHON      = xbmcaddon.Addon(id='xbmc.python').getAddonInfo('version')
WEATHER_ICON     = '%s.png'
WEATHER_WINDOW   = xbmcgui.Window(12600)
LOCALIZE         = xbmc.getLanguage().lower()
SPEEDUNIT        = xbmc.getRegion('speedunit')
TEMPUNIT         = str(xbmc.getRegion('tempunit'),encoding='utf-8')
TIMEFORMAT       = xbmc.getRegion('meridiem')
DATEFORMAT       = xbmc.getRegion('dateshort')
MAXDAYS          = 5

socket.setdefaulttimeout(10)

def log(txt):
    if DEBUG == 'true':
        if isinstance (txt,str):
            txt = txt.decode("utf-8")
        message = u'%s: %s' % (ADDONID, txt)
        xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

def set_property(name, value):
    WEATHER_WINDOW.setProperty(name, value)

def refresh_locations():
    locations = 0
    for count in range(1, 6):
        loc_name = ADDON.getSetting('Location%s' % count)
        if loc_name != '':
            locations += 1
        else:
            ADDON.setSetting('Location%sid' % count, '')
        set_property('Location%s' % count, loc_name)
    set_property('Locations', str(locations))
    log('available locations: %s' % str(locations))

def forecast(loc,locid, loclat, loclon):
    try:
        lang = LANG[LOCALIZE]
    except:
        lang = 'EN'
    opt = 'lang:' + lang
    log('weather location: %s' % locid)
    retry = 0
    while (retry < 6) and (not xbmc.abortRequested):
        query = wundergroundapi(locid, loclat, loclon)

        if query != '':
            retry = 6
        else:
            retry += 1
            xbmc.sleep(10000)
            log('weather download failed')
    log('forecast data: %s' % query)
    data = parse_data(query)
    if data != '' and 'observations' in data and 'error' not in data['observations']:
        properties(data,loc,locid)
    else:
        clear()

def clear():
    set_property('Current.Condition'     , 'N/A')
    set_property('Current.Temperature'   , '0')
    set_property('Current.Wind'          , '0')
    set_property('Current.WindDirection' , 'N/A')
    set_property('Current.Humidity'      , '0')
    set_property('Current.FeelsLike'     , '0')
    set_property('Current.UVIndex'       , '0')
    set_property('Current.DewPoint'      , '0')
    set_property('Current.OutlookIcon'   , 'na.png')
    set_property('Current.FanartCode'    , 'na')
    for count in range (0, MAXDAYS+1):
        set_property('Day%i.Title'       % count, 'N/A')
        set_property('Day%i.HighTemp'    % count, '0')
        set_property('Day%i.LowTemp'     % count, '0')
        set_property('Day%i.Outlook'     % count, 'N/A')
        set_property('Day%i.OutlookIcon' % count, 'na.png')
        set_property('Day%i.FanartCode'  % count, 'na')

def parse_data(response):
    try:
        raw = response.replace('<br>',' ').replace('&auml;','ä') # wu api bugs
        #reply = raw.replace('"-999%"','""').replace('"-9999.00"','""').replace('"-9998"','""').replace('"NA"','""').replace('"--"','""') # wu will change these to null responses in the future
        reply = raw.replace('null', '0')
        data = json.loads(reply)
    except:
        log('failed to parse weather data')
        data = ''
    return data

def properties(data,loc,locid):
# standard properties
    set_property('Current.Location'      , str(data['observations'][0]['stationID']))
    set_property('Current.Temperature'   , str(data['observations'][0]['metric']['temp']))
    set_property('Current.Wind'          , str(data['observations'][0]['metric']['windSpeed']))
    set_property('Current.WindDirection' , str(wind_deg_to_card(data['observations'][0]['winddir'])))
    set_property('Current.Humidity'      , str(data['observations'][0]['humidity']))
    set_property('Current.FeelsLike' , FEELS_LIKE(int(data['observations'][0]['metric']['temp']), data['observations'][0]['metric']['windSpeed'], data['observations'][0]['humidity'], 'c') + TEMPUNIT)
    set_property('Current.UVIndex'       , str(data['observations'][0]['uv']))
    set_property('Current.DewPoint'      , str(data['observations'][0]['metric']['dewpt']))

# forecast properties
    set_property('Forecast.IsFetched'        , 'true')
    set_property('Forecast.City'             , "")
    set_property('Forecast.State'            , "")
    set_property('Forecast.Country'          , "")
    if data['observations'][0]['epoch']:
        update = time.localtime(float(data['observations'][0]['epoch']))
        local = time.localtime(float(data['observations'][0]['epoch']))
        if DATEFORMAT[1] == 'd':
            updatedate = WEEKDAY[update[6]] + ' ' + str(update[2]) + ' ' + MONTH[update[1]] + ' ' + str(update[0])
            localdate = WEEKDAY[local[6]] + ' ' + str(local[2]) + ' ' + MONTH[local[1]] + ' ' + str(local[0])
        elif DATEFORMAT[1] == 'm':
            updatedate = WEEKDAY[update[6]] + ' ' + MONTH[update[1]] + ' ' + str(update[2]) + ', ' + str(update[0])
            localdate = WEEKDAY[local[6]] + ' ' + str(local[2]) + ' ' + MONTH[local[1]] + ' ' + str(local[0])
        else:
            updatedate = WEEKDAY[update[6]] + ' ' + str(update[0]) + ' ' + MONTH[update[1]] + ' ' + str(update[2])
            localdate = WEEKDAY[local[6]] + ' ' + str(local[0]) + ' ' + MONTH[local[1]] + ' ' + str(local[2])
        if TIMEFORMAT != '/':
            updatetime = time.strftime('%I:%M%p', update)
            localtime = time.strftime('%I:%M%p', local)
        else:
            updatetime = time.strftime('%H:%M', update)
            localtime = time.strftime('%H:%M', local)
        set_property('Forecast.Updated'          , updatedate + ' - ' + updatetime)
# current properties
    set_property('Current.LocalTime'         , localtime)
    set_property('Current.LocalDate'         , localdate)
    set_property('Current.IsFetched'         , 'true')
    set_property('Current.WindDegree'        , str(data['observations'][0]['winddir']) + u'°')
    set_property('Current.SolarRadiation'    , str(data['observations'][0]['uv']))
    if 'F' in TEMPUNIT:
        set_property('Current.Pressure'      , str(data['observations'][0]['metric']['pressure']) + ' inHg')
        set_property('Current.Precipitation' , str(data['observations'][0]['metric']['precipRate']) + ' in')
        set_property('Current.HeatIndex'     , str(data['observations'][0]['metric']['heatIndex']) + TEMPUNIT)
        set_property('Current.WindChill'     , str(data['observations'][0]['metric']['windChill']) + TEMPUNIT)
    else:
        set_property('Current.Pressure'      , str(data['observations'][0]['metric']['pressure']) + ' mb')
        set_property('Current.Precipitation' , str(data['observations'][0]['metric']['precipRate']) + ' mm')
        set_property('Current.HeatIndex'     , str(data['observations'][0]['metric']['heatIndex']) + TEMPUNIT)
        set_property('Current.WindChill'     , str(data['observations'][0]['metric']['windChill']) + TEMPUNIT)
    if SPEEDUNIT == 'mph':
        set_property('Current.WindGust'      , str(data['observations'][0]['metric']['windGust']) + ' ' + SPEEDUNIT)
    else:
        set_property('Current.WindGust'      , str(data['observations'][0]['metric']['windGust']) + ' ' + SPEEDUNIT)
# today properties
    set_property('Today.IsFetched'                     , 'true')
    if TIMEFORMAT != '/':
        AM = str(TIMEFORMAT.split('/')[0],encoding='utf-8')
        PM = str(TIMEFORMAT.split('/')[1],encoding='utf-8')
        hour = int(datetime.datetime.fromtimestamp(int(data['sunriseTimeUtc'][0])).strftime('%H')) % 24
        isam = (hour >= 0) and (hour < 12)
        if isam:
            hour = ('12' if (hour == 0) else '%02d' % (hour))
            set_property('Today.Sunrise'               , hour.lstrip('0') + ':' + datetime.datetime.fromtimestamp(int(data['sunriseTimeUtc'][0])).strftime('%M') + ' ' + AM)
        else:
            hour = ('12' if (hour == 12) else '%02d' % (hour-12))
            set_property('Today.Sunrise'               , hour.lstrip('0') + ':' + datetime.datetime.fromtimestamp(int(data['sunriseTimeUtc'][0])).strftime('%M') + ' ' + PM)
        hour = int(datetime.datetime.fromtimestamp(int(data['sunsetTimeUtc'][0])).strftime('%H')) % 24
        isam = (hour >= 0) and (hour < 12)
        if isam:
            hour = ('12' if (hour == 0) else '%02d' % (hour))
            set_property('Today.Sunset'                , hour.lstrip('0') + ':' + datetime.datetime.fromtimestamp(int(data['sunsetTimeUtc'][0])).strftime('%M') + ' ' + AM)
        else:
            hour = ('12' if (hour == 12) else '%02d' % (hour-12))
            set_property('Today.Sunset'                , hour.lstrip('0') + ':' + datetime.datetime.fromtimestamp(int(data['sunsetTimeUtc'][0])).strftime('%M') + ' ' + PM)
    else:
        set_property('Today.Sunrise'                   , datetime.datetime.fromtimestamp(int(data['sunriseTimeUtc'][0])).strftime('%H') + ':' + datetime.datetime.fromtimestamp(int(data['sunriseTimeUtc'][0])).strftime('%M'))
        set_property('Today.Sunset'                    , datetime.datetime.fromtimestamp(int(data['sunsetTimeUtc'][0])).strftime('%H') + ':' + datetime.datetime.fromtimestamp(int(data['sunriseTimeUtc'][0])).strftime('%M'))
# daily properties
    set_property('Daily.IsFetched', 'true')
    for count, item in enumerate(data['dayOfWeek']):
        # if datetime.datetime.now().strftime("%I:%M %p") > "15:00" and count == 0:
        #     count = count + 1
        weathercode = WEATHER_CODES[data['daypart'][0]['iconCode'][2*count]]
        set_property('Daily.%i.LongDay' % (count + 1), item)
        set_property('Daily.%i.ShortDay' % (count+1), item)
        date = datetime.datetime.fromtimestamp(data['validTimeUtc'][count])
        if DATEFORMAT[1] == 'd':
            set_property('Daily.%i.LongDate'         % (count+1), str(date.day) + ' ' + date.month)
            set_property('Daily.%i.ShortDate'        % (count+1), str(date.day) + ' ' + MONTH[date.month])
        else:
            set_property('Daily.%i.LongDate'         % (count+1), str(date.month) + ' ' + str(date.day))
            set_property('Daily.%i.ShortDate'        % (count+1), MONTH[date.month] + ' ' + str(date.day))
        set_property('Daily.%i.Outlook'              % (count+1), str(data['daypart'][0]['wxPhraseLong'][2*count]))
        set_property('Daily.%i.OutlookIcon'          % (count+1), WEATHER_ICON % weathercode)
        set_property('Daily.%i.FanartCode'           % (count+1), str(weathercode))
        if SPEEDUNIT == 'mph':
            set_property('Daily.%i.WindSpeed'        % (count+1), str(data['daypart'][0]['windSpeed'][2*count]) + ' ' + SPEEDUNIT)
        elif SPEEDUNIT == 'Beaufort':
            set_property('Daily.%i.WindSpeed'        % (count+1), KPHTOBFT(data['daypart'][0]['windSpeed'][2*count]))
        else:
            set_property('Daily.%i.WindSpeed'        % (count+1), str(data['daypart'][0]['windSpeed'][2*count]) + ' ' + SPEEDUNIT)
            set_property('Daily.%i.WindDirection'        % (count+1), str(data['daypart'][0]['windDirection'][2*count]))
            set_property('Daily.%i.ShortWindDirection'   % (count+1), str(data['daypart'][0]['windDirectionCardinal'][2*count]))
            set_property('Daily.%i.WindDegree'           % (count+1), str(data['daypart'][0]['windDirection'][2*count]))
            set_property('Daily.%i.Humidity'             % (count+1), str(data['daypart'][0]['relativeHumidity'][2*count]) + '%')
        if 'F' in TEMPUNIT:
            set_property('Daily.%i.HighTemperature'  % (count+1), str(CELSIUStoFAHR(data['daypart'][0]['temperature'][2*count])) + TEMPUNIT)
            set_property('Daily.%i.LowTemperature'   % (count+1), str(CELSIUStoFAHR(data['daypart'][0]['temperature'][2*count + 1])) + TEMPUNIT)
            set_property('Daily.%i.Precipitation'    % (count+1), str(data['daypart'][0]['qpf'][2*count]) + ' in')
        else:
            set_property('Daily.%i.HighTemperature'  % (count+1), str(data['daypart'][0]['temperature'][2*count]) + TEMPUNIT)
            set_property('Daily.%i.LowTemperature'   % (count+1), str(data['daypart'][0]['temperature'][2*count + 1]) + TEMPUNIT)
            set_property('Daily.%i.Precipitation'    % (count+1), str(data['daypart'][0]['qpf'][2*count]) + ' in')

log('version %s started: %s' % (VERSION, sys.argv))
log('lang: %s'    % LOCALIZE)
log('speed: %s'   % SPEEDUNIT)
log('temp: %s'    % TEMPUNIT[1])
log('time: %s'    % TIMEFORMAT)
log('date: %s'    % DATEFORMAT)

set_property('WeatherProvider', ADDONNAME)
set_property('WeatherProviderLogo', xbmc.translatePath(os.path.join(CWD, 'resources', 'banner.png')))

if not API:
    log('no api key provided')
else:
    location = ADDON.getSetting('Location%s' % sys.argv[1])
    locationid = ADDON.getSetting('Location%sid' % sys.argv[1])
    locationlat = ADDON.getSetting('Location%slat' % sys.argv[1])
    locationlon = ADDON.getSetting('Location%slon' % sys.argv[1])
    if (locationid == '') and (sys.argv[1] != '1'):
        location = ADDON.getSetting('Location1')
        locationid = ADDON.getSetting('Location1id')
        locationlat = ADDON.getSetting('Location1lat')
        locationlon = ADDON.getSetting('Location1lon')
        log('trying location 1 instead')
    if not locationid == '':
        forecast(location, locationid, locationlat, locationlon)
    else:
        log('no location found')
        clear()
    refresh_locations()

log('finished')
