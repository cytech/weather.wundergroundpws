# -*- coding: utf-8 -*-

from future import standard_library
standard_library.install_aliases()
import sys, urllib.request, urllib.error, urllib.parse, gzip, base64, traceback
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
from io import StringIO
from io import BytesIO
import json

API = sys.modules[ "__main__" ].API
FORECAST5_URL = 'https://api.weather.com/v3/wx/forecast/daily/5day?geocode={},{}&units=m&language=en-US&format=json&apiKey={}'
CURRENT_PWS_URL = 'https://api.weather.com/v2/pws/observations/current?stationId={}&format=json&units=m&apiKey={}'

def wundergroundapi(locid, loclat, loclon):
    try:
        forecast5_url = FORECAST5_URL.format(loclat,loclon,API)
        forecast5_req = urllib.request.Request(forecast5_url)
        forecast5_req.add_header('Accept-encoding', 'gzip')
        response = urllib.request.urlopen(forecast5_req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            compr = gzip.GzipFile(fileobj=buf)
            forecast5_data = compr.read()
        else:
            forecast5_data = response.read()
        response.close()
    except:
        forecast5_data = ''

    try:
        currentpws_url = CURRENT_PWS_URL.format(locid, API)
        currentpws_req = urllib.request.Request(currentpws_url)
        currentpws_req.add_header('Accept-encoding', 'gzip')
        response = urllib.request.urlopen(currentpws_req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            compr = gzip.GzipFile(fileobj=buf)
            dcurrentpws_ata = compr.read()
        else:
            currentpws_data = response.read()
        response.close()
    except:
        currentpws_data = ''

    #this is python 3.5
    #jsonMerged = {**json.loads(currentpws_data), **json.loads(forecast5_data)}

    a = json.loads(currentpws_data)
    b = json.loads(forecast5_data)
    jsonMerged = merge_two_dicts(a, b)

    data = json.dumps(jsonMerged)

    return data

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
