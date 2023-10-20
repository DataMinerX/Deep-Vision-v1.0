import pandas as pd
from ultralytics import YOLO
from osgeo import gdal
import cv2
import torch
from osgeo import ogr
from osgeo import osr
import os
import datetime
import glob
import shutil
import warnings
warnings.filterwarnings("ignore")
import utm

class Tree:
    def __init__(self,epg):
        zone=epg
        self.cwd=os.getcwd()
        self.model=self.cwd+"\\models\\"
        self.input=self.cwd+"\\geotiffs\\"
        self.output=self.cwd+"\\results\\"
        self.inputEPSG=zone
        self.pixels=[]
        self.utms=[]
        self.csv=None
        self.cwds=[]
    def pixel2coordinates(self,px,geotiff):
        ds = gdal.Open(geotiff)
        xoffset, px_w, rot1, yoffset, px_h, rot2 = ds.GetGeoTransform()
        x1,y1,x2,y2=px
        posX1 = px_w * x1 + rot1 * y1 + xoffset
        posY1 = rot2 * x1 + px_h * y1 + yoffset
        posX2 = px_w * x2 + rot1 * y2 + xoffset
        posY2 = rot2 * x2 + px_h * y2 + yoffset
        posX1 += px_w / 2.0
        posY1 += px_h / 2.0
        posX2 += px_w / 2.0
        posY2 += px_h / 2.0
        x_mid=(posX1+posX2)/2
        y_mid=(posY1+posY2)/2
        return (round(x_mid,2),round(y_mid,2))
    def UTM(self,ll):
        return utm.from_latlon(ll[0],ll[1])
    def  EPSG2WGS84(self,projections):
        temp=[]
        for i in projections:
            pointX,pointY=i
            inputEPSG = self.inputEPSG
            outputEPSG = 4326
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(pointX, pointY)
            inSpatialRef = osr.SpatialReference()
            inSpatialRef.ImportFromEPSG(inputEPSG)
            outSpatialRef = osr.SpatialReference()
            outSpatialRef.ImportFromEPSG(outputEPSG)
            coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
            point.Transform(coordTransform)
            u=(point.GetX(), point.GetY())
            self.cwds.append(u)
            u=self.UTM(u)
            temp.append(u)
        return temp
    def rename_files(self):
        path=self.input
        files = os.listdir(path)
        for index, file in enumerate(files):
            os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index), '.tiff'])))
        print('\n All files renamed')
    def get_filenames(self):
        self.rename_files()
        types = ('*.tif', '*.tiff')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(self.input+files))
        if len(files_grabbed)==0:
            return -1
        return files_grabbed
    def generate_pixels(self):
        files=self.get_filenames()
        date=datetime.datetime.now()
        name=f'{date.day}-{date.month}-{date.year}_ {date.hour} - {date.minute}'
        self.csvname=name
        for file in files:
            # Calcuation of Size of tiff
            img = cv2.imread(file, cv2.IMREAD_COLOR)
            imgsz=img.shape[:2]
            model=YOLO(self.model+'trees.pt')
            temp=[]
            results = model(file,imgsz=imgsz,project="results",name=name,save=True)
            for result in results:
                result= result.boxes.xyxy
                temp=result.tolist()
                for i in temp:
                    t=self.pixel2coordinates(i,file)
                    self.pixels.append(t)
    def lat_long(self):
        self.utms=self.EPSG2WGS84(self.pixels)
    def getcsv(self):
        path=self.cwd+"\\results\\"
        df={}
        lats=[]
        longs=[]
        zones=[]
        symbols=[]
        la=[]
        lo=[]
        for x,y in self.cwds:
            la.append(x)
            lo.append(y)
        for lat,longi,zone,symbol in self.utms:
            lats.append(lat)
            longs.append(longi)
            zones.append(zone)
            symbols.append(symbol)
        df['Easting']=lats
        df['Northing']=longs
        df['Zone']=zones
        df['Symbol']=symbols
        df['Class']='Trees'
        df['Latitude']=la
        df['Longitude']=lo
        df = pd.DataFrame(df)
        df.reset_index(inplace=True)
        df.rename(columns={'index':'id'},inplace=True)
        df.to_csv(path+"tree.csv",index=False)
        print("CVS exported")
        


# def main():
#     tr=Tree()
#     tr.generate_pixels()
#     tr.lat_long()
#     tr.getcsv()

# if __name__=="__main__": 
# 	main()
