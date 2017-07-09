import subprocess
import csv
from pyproj import Proj,transform

print("Extract GPS data from EXIF")
subprocess.call("mm3d XifGps2Txt '.*[JPG|jpg]' > img2ortho.log", shell=True)

# WGS84 proj to local
wgs = Proj(init='epsg:4326')
local = Proj(init='epsg:2154')

# get lat/lon from micmac generated txt file
with open('GpsCoordinatesFromExif.txt') as gpscsv:
    gpsdata = csv.reader(gpscsv, delimiter=' ')
    print("Reproject to local X/Y")
    with open('LocalCoordinatesFromExif.txt', mode='w') as localcsv:
        localdata = csv.writer(localcsv, delimiter=' ')
        localdata.writerow(['#F=N','X','Y','Z'])
        for gps in gpsdata:
            x2, y2 = transform(wgs,local,gps[1],gps[2])
            localdata.writerow([gps[0],x2,y2,gps[3]])


print("Micmac: OriConvert")
subprocess.call('mm3d OriConvert OriTxtInFile LocalCoordinatesFromExif.txt gps NameCple=FileImagesNeighbour.xml >> img2ortho.log', shell=True)

print("Micmac: Tapioca > search for similarities between images")
subprocess.call('mm3d Tapioca MulScale .*.JPG 300 1200 ExpTxt=0 >> img2ortho.log', shell=True)
print("Micmac: Tapas")
subprocess.call('mm3d Tapas RadialBasic .*.JPG Out=Arbitrary ExpTxt=0 >> img2ortho.log', shell=True)
print("Micmac: CenterBascule > convert relative position to local projection")
subprocess.call('mm3d CenterBascule ".*.JPG" Arbitrary gps local >> img2ortho.log', shell=True)
print("Micmac: Malt")
subprocess.call('mm3d Malt Ortho .*.JPG local NbVI=2 DirTA=TA EZA=1 >> img2ortho.log', shell=True)
print("Micmac: Tanwy")
subprocess.call('mm3d Tawny Ortho-MEC-Malt/ Out=OrthoMosaique.tif >> img2ortho.log', shell=True)

print("gdal_translate & final info")
subprocess.call('gdal_translate Ortho-MEC-Malt/OrthoMosaique.tif ortho.tif -co TILED=YES -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=YCBCR -a_nodata "0 0 0" -a_srs EPSG:2154; gdalinfo ortho.tif', shell=True)

#print("Micmac: AperiCloud")
#subprocess.call('mm3d AperiCloud .*.JPG local Out=AperiCloud.ply ExpTxt=0 >> img2ortho.log', shell=True)
