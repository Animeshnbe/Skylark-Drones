from itertools import groupby
from collections import namedtuple
import os, os.path 
from PIL import Image
from PIL import ExifTags
import csv
def _convert_to_degrees(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)
 
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)
 
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)
 
    return d + (m / 60.0) + (s / 3600.0)

from math import sin, cos, sqrt, atan2, radians
def dist(lat, lon, lat1, lon1):
    #radian=degrees*Math.PI/180;
    dlon = radians(lon - lon1)
    dlat = radians(lat - lat1)
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat) * sin(dlon / 2)**2
    c=2*atan2(sqrt(a), sqrt(1-a))*6371000
    return c

imgs = [] 
valid_images = [".jpg", ".gif", ".png", ".jpeg"] 
  
path="C:/Users/Animesh/Documents/technical_assignment_software_developer_4/software_dev/images/"
for f in os.listdir(path): 
    ext = os.path.splitext(f)[1] 
          
    if ext.lower() not in valid_images: 
        continue
    imgs.append(f) 
 
with open('DJI_0301.srt') as f:
    res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]


header=['Time','Images']
with open('imagelist.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header) # write header
    for sub in res:
        sub = [x.strip() for x in sub]
        number, start_end, *content = sub 
        start, end = start_end.split(' --> ')
        
        lat1=float(content[0].split(',')[1])
        lon1=float(content[0].split(',')[0])
        filteredimg = [] 
        #print(lat1,'  ',lon1)
        for i in imgs: 
            image = Image.open(os.path.join(path, i)) 
            exifDataRaw = image._getexif()
            if exifDataRaw:
                for tag, value in exifDataRaw.items():
                    decodedTag = ExifTags.TAGS.get(tag, tag)
                    if(decodedTag=='GPSInfo'):
                        lat=_convert_to_degrees(value[2])
                        lon=_convert_to_degrees(value[4])
                        if value[1] != "N":
                            lat = 0 - lat
                        if value[3] != "E":
                            lon = 0 - lon
                    else:
                        continue
                    if dist(lat,lon,lat1,lon1) < 35:
                        #print(i)
                        filteredimg.append(image)
                        writer.writerow([start, i])
        #subs.append(Subtitle(number, start, end, content))
