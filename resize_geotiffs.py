from osgeo import ogr
from osgeo import osr
import os
import glob
from osgeo import gdal

# cwd=os.getcwd()

# gettiffs=cwd+"\\geotiffs\\"
# output=cwd+"\\resized-geotiffs\\"
# files=os.listdir(gettiffs)

# for file in files:
#     path=gettiffs+file
#     op=output+file
#     dsRe=gdal.Warp(op,path,width=640,height=640)
# print('Done!!')

class Resize:
    def __init__(self):
        self.cwd=os.getcwd()
        self.gettiffs=self.cwd+"\\geotiffs-large\\"
        self.output=self.cwd+"\\resized-geotiffs\\"
    def resize(self):
        files=os.listdir(self.gettiffs)
        if len(files)==0:
            return -1
        for file in files:
            path=self.gettiffs+file
            op=self.output+file
            dsRe=gdal.Warp(op,path,width=640,height=640)
        return 1

# def main():
#     re=Resize()
#     if re.resize()==-1:
#         print("Geotiff Folder is empty make sure You have Placed .tiffs in correct folder.")

# if __name__=="__main__": 
#     main() 
        
        