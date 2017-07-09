# deMicMac

Work in Progress !!!!

## img2ortho.py

Current progress:
- extracts GPS location from EXIF in each JPG/jpg file in the current folder
- reproject WGS84 to local projection (default EPSG:2154 / Lambert93)
- generates txt file expected by MicMac
- launch Micmac steps: Tapioca, Tapas, CentreBascule, Malt, Tanwy
- convert huge uncompressed generated ortho tiff to compressed one with nodata in local projection
