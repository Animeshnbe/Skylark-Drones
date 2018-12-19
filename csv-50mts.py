#import exifread as ef
import os, os.path 
from PIL import Image
from PIL import ExifTags
import pandas as pd
from sklearn.preprocessing import Imputer
#converting coordinates in exif data to degrees in float type
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

#finding distance between 2 coordinates
from math import sin, cos, sqrt, atan2, radians
def dist(lat, lon, lat1, lon1):
    #radian=degrees*Math.PI/180;
    dlon = radians(lon - lon1)
    dlat = radians(lat - lat1)
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat) * sin(dlon / 2)**2
    c=2*atan2(sqrt(a), sqrt(1-a))*6371000   #radius of earth in mts
    return c

imgs = [] 
valid_images = [".jpg", ".gif", ".png", ".jpeg"] 
  
path="C:/Users/Animesh/Documents/technical_assignment_software_developer_4/software_dev/images/"
for f in os.listdir(path): 
    ext = os.path.splitext(f)[1] 
          
    if ext.lower() not in valid_images: 
        continue
    imgs.append(f) 
 
# Importing the dataset from csv file
dataset = pd.read_csv('assets.csv',header=0)
#X=pd.DataFrame(dataset)
X = dataset.iloc[:, 1:3].values
# Taking care of missing data
imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imputer = imputer.fit(X[:, 1:3])
X[:, 1:3] = imputer.transform(X[:, 1:3])

for row in X:
    lat1=row[1]
    lon1=row[0]
    filteredimg = [] 
    print(lat1,'  ',lon1)
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
                if dist(lat,lon,lat1,lon1) < 50:
                    print(i)
                    filteredimg.append(image)