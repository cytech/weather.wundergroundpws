weather.wundergroundpws

KODI 19 MATRIX NOTE
This addon will not work with Kodi 19.
I have forked the Kodi 19 Multi Weather addon by Ronie (available in the default Kodi 19 Weather Repo) and it could use some testing. The Multi Weather addon allows for multiple providers (currently Yahoo, Weatherbit and openweathermaps) so I have added a wundergroundpws provider.
Get it here https://gitlab.com/dalbright/weather.multi

A Kodi weather addon for registered and active Weather Underground personal weather station users.

:+1: If you find this product useful, feel free to buy me a beer: https://paypal.me/cytecheng

To use this addon, you need to enter your personal weather station API key in the addon settings.

To get a free API key:
1) You must have a personal weather station registered and uploading data to Weather Underground
    
    a) Join weather Underground
    
    b) Sign In
    
    c) My Profile -> My Weather Stations
    
    d) Add a New PWS
2) get API key at  https://www.wunderground.com/member/api-keys
3) In Kodi - System - Addons - Install from Zip File (weather.wundergroundpws.zip)
4) In Kodi - System - Services - Weather select Weather UndergroundPWS as Service for weather information
5) -Settings add your API Key
6) -Settings

    Location1 Display Name - ( This can be anything you want)
    
    Location1 StationID - (your station ID  i.e  KCAFOOBARFXX)
    
    Location1 Forecast Latitude - ( 35.317)
    
    Location1 Forecast Longitude - ( -119.125)
    
The StationID collects the data from the PWS and displays in the current observation (top area) in Kodi Weather.

The latitude/longitude defines where the forecast data (Kodi 5 day forecast) is collected

Only English and English(US) languages are defined. All others will fail.

This addon no longer allows for geoip lookup.
You must know the stationid and forecast latitude/longitude beforehand to configure.

