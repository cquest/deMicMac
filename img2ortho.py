import subprocess
import csv
from pyproj import Proj,transform

# use Micmac to extract GPS data from JPEG exif
subprocess.call("mm3d XifGps2Txt '.*[JPG|jpg]' > /dev/null", shell=True)

# WGS84 proj to local
wgs = Proj(init='epsg:4326')
local = Proj(init='epsg:2154')

# get lat/lon from micmac generated txt file
with open('GpsCoordinatesFromExif.txt') as gpscsv:
    gpsdata = csv.reader(gpscsv, delimiter=' ')
    # save local X/Y to our txt file
    with open('LocalCoordinatesFromExif.txt', mode='w') as localcsv:
        localdata = csv.writer(localcsv, delimiter=' ')
        localdata.writerow(['#F=N','X','Y','Z'])
        for gps in gpsdata:
            x2, y2 = transform(wgs,local,gps[1],gps[2])
            localdata.writerow([gps[0],x2,y2,gps[3]])
