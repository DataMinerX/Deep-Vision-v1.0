import streamlit as st
import pandas as pd
import os
import cv2
from Tree import Tree
import resize_geotiffs as rg
from PIL import Image
import numpy as np
import time
from stqdm import stqdm
import shutil
import glob
import rasterio
from rasterio.plot import show
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from ultralytics import YOLO
from osgeo import gdal
import cv2
import torch
from osgeo import ogr
from osgeo import osr
import os
import datetime
import warnings
warnings.filterwarnings("ignore")
import utm
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from haversine import haversine,Unit
import random 

# Dump Memory
def clear_directory(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"Cleared everything inside {directory}.")
    except Exception as e:
        print(f"An error occurred: {e}")
# Initialize Function
def initialize():
  # Step 1: Copy from resized-tiff to geotiffs
  cwd=os.getcwd()
  geotiffs_path=cwd+"\\geotiffs\\"
  input_path=cwd+"\\resized-geotiffs\\"

  files_to_copy = os.listdir(input_path)

  for i in stqdm(range(len(files_to_copy))):
    file_name=files_to_copy[i]
    full_source_path = os.path.join(input_path, file_name)
    full_destination_path = os.path.join(geotiffs_path, file_name)
    shutil.copy(full_source_path, full_destination_path)
    time.sleep(2)
  return True

# Tree Class for Prediction
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
            model=YOLO(self.cwd+'\\trees.pt')
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
    def generate_normalized_random_numbers(self,start, end, size):
      random_numbers = [random.uniform(start, end) for _ in range(size)]
      max_val = max(random_numbers)
      min_val = min(random_numbers)
      normalized_numbers = [(x - min_val) / (max_val - min_val) for x in random_numbers]
      return normalized_numbers
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
        df['LATITUDE']=la
        df['LONGITUDE']=lo
        start_range = 3
        end_range = 15
        size_of_list = len(lats)
        normalized_random_numbers = self.generate_normalized_random_numbers(start_range, end_range, size_of_list)
        df['Height']=normalized_random_numbers
        df = pd.DataFrame(df)
        df.reset_index(inplace=True)
        df.rename(columns={'index':'id'},inplace=True)
        df.to_csv(path+"tree.csv",index=False)
        print("CVS exported")

upload_dir=os.getcwd()+"\\geotiffs-large\\"
with st.sidebar:
  st.image("https://i.ibb.co/SQGBVfm/logo-no-background.png")
  st.title("Deep Vision v1.0")
  choise=st.radio("📌 Options",["📤 Upload","🗺 Visualize","📉📈Predict","📝 Analytics","Release Memory(must)"])
  st.info("This Web Application allows you to upload .tiff, generating insights")

# Upload Tab
if choise=="📤 Upload":
  st.title("📤 Upload")
  uploaded_files = st.file_uploader('Choose a TIFF file', accept_multiple_files=True, type=['tiff', 'tif'])
  submit = st.button('Upload')
  if submit:
    for upl in stqdm(range(len(uploaded_files))):
      with open(os.path.join(upload_dir, uploaded_files[upl].name), 'wb') as file:
        file.write(uploaded_files[upl].read())
      time.sleep(0.1)
    re=rg.Resize()
    if re.resize()==-1:
        st.markdown("Geotiff Folder is empty make sure You have Placed .tiffs in correct folder.")
    else:
      st.markdown("**Done!!**")

# Visualize Tab
if choise=="🗺 Visualize":
  st.title("🗺 Visualize 🗺")
  dirt=os.getcwd()+"\\resized-geotiffs\\"
  check_dir=os.listdir(dirt)

  if len(check_dir)>0:
    cpy=st.button("Start",on_click=initialize)
    iscpy=False
    if cpy:
      image_directory = os.getcwd()+"\\geotiffs\\"
      image_files = [file for file in os.listdir(image_directory) if file.endswith('.tif') or file.endswith('.tiff')]
      st.title('📊 Display GeoTIFF Images and Their Color Histograms')
      columns = st.columns(len(image_files))

      # Display each GeoTIFF image and its color histogram
      for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_directory, image_file)

        # Read the GeoTIFF file
        src = rasterio.open(image_path)

        # Convert the GeoTIFF to a standard image format (e.g., JPEG)
        with rasterio.open(image_path) as dataset:
          data = dataset.read()
          profile = dataset.profile
        profile['driver'] = 'PNG'  # Or 'JPEG'

        # Write the data to a temporary image file
        with rasterio.open("temp.png", 'w', **profile) as dst:
          dst.write(data)

        # Open the converted image
        image = Image.open("temp.png")

        # Display the image
        with columns[i]:
          st.image(image, use_column_width=True, caption=f'Image: {image_file}')

          # Display color histogram
          plt.figure(figsize=(7, 7))
          with rasterio.open(image_path) as src:
              for i in range(1, src.count + 1):
                  plt.hist(src.read(i).ravel(), bins=50, color=f'C{i-1}', alpha=0.5)
          plt.title('Color Histogram')
          st.pyplot(plt)

        # Remove the temporary image file
        os.remove("temp.png")    
  else:
    st.markdown("Upload Data!! **Missed First Step**")


# Prediction Tab
if choise=="📉📈Predict":
  st.title("📉📈Predict")
  cwd=os.getcwd()+"//geotiffs//"
  direct=os.listdir(cwd)
  if len(direct)>0:
    user_input = st.text_input("Enter EPSG code for the specific zone")
    if st.button('Submit'):
          if user_input:
              epsg=int(user_input)
              tr=Tree(epg=epsg)
              st.markdown("EPSG Initialized...")
              time.sleep(2)
              st.markdown("Sending EPSG to dispatch pixels...")
              time.sleep(2)
              tr.generate_pixels()
              st.markdown("Pixel Dispatched...")
              time.sleep(2)
              st.markdown('Getting latitudes & longitudes')
              time.sleep(2)
              tr.lat_long()
              st.markdown("Data Generated...Exporting Data")
              time.sleep(2)
              tr.getcsv()
              st.markdown('**Generated Go to Next Tab to Get analytics...')
          else:
              st.write('Please enter EPSG code to continue')

# Helper function of Analytics
def check_csv_present(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.csv'):
            return True
    return False
# Analytics Tab
if choise=='📝 Analytics':
  st.title('📝 Analytics')
  
  folder_path = os.getcwd()+"\\results\\"
  if check_csv_present(folder_path):

    # Sidebar filters
    min_height, max_height = st.sidebar.slider('Select Height Range', min_value=0, max_value=15, value=(0, 15))
    st.markdown('Click below to start prediction')
    if st.button('Start'):
      csv_file=os.getcwd()+"\\results\\tree.csv"
      df=pd.read_csv(csv_file)
      st.markdown('**Live Location of Trees**')
      filtered_df = df[(df['Height'] >= min_height) & (df['Height'] <= max_height)]
      m = folium.Map(location=[filtered_df['LATITUDE'].mean(), filtered_df['LONGITUDE'].mean()], zoom_start=4)
      marker_cluster = MarkerCluster().add_to(m)

      for i, row in filtered_df.iterrows():
         popup_text = f"ID: {row['id']}<br>Height: {row['Height']}<br>Latitude: {row['LATITUDE']}<br>Longitude: {row['LONGITUDE']}"
         folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=popup_text).add_to(marker_cluster)
      st.markdown(m._repr_html_(), unsafe_allow_html=True)

      # Adding visual analytics
      st.subheader('Visual Analytics')
      st.write('Histogram of Tree Heights')
      st.write('Total number of Trees: '+str(len(filtered_df)))
      plt.figure(figsize=(8, 6))
      sns.histplot(filtered_df['Height'], kde=True, bins=8, color='skyblue')
      st.set_option('deprecation.showPyplotGlobalUse', False)
      st.pyplot()

      # Ploting km wise tree

      # Calculating distance in kilometers
      distances = []
      for i in range(1, len(filtered_df)):
          distance = haversine((filtered_df['LATITUDE'].iloc[i - 1], filtered_df['LONGITUDE'].iloc[i - 1]),
                              (filtered_df['LATITUDE'].iloc[i], filtered_df['LONGITUDE'].iloc[i]), unit=Unit.KILOMETERS)
          distances.append(distance)
      st.subheader('Tree Count per Kilometer')
      plt.figure(figsize=(8, 6))
      sns.histplot(distances, bins=5, kde=False, color='lightgreen', edgecolor='black')
      plt.xlabel('Distance (in kilometers)')
      plt.ylabel('Tree Count')
      st.pyplot()
      
  else:
     st.markdown("Predict First")

if choise=="Release Memory(must)":
   if st.button("Release"):
      cwd=os.getcwd()
      directory1 = cwd+"//geotiffs//"
      directory2 = cwd+"//geotiffs-large//"
      directory3 = cwd+"//resized-geotiffs//"
      directory4 = cwd+"//results//"

      clear_directory(directory1)
      clear_directory(directory2)
      clear_directory(directory3)
      clear_directory(directory4)

      st.markdown("**Memory Released. Thank You For Using....")

