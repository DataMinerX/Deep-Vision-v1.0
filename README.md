
<img src="https://gdurl.com/ebhK" alt="Logo" width="1000"/>


# Deep Vision v1.0

Deep Vision is an innovative object detection application powered by YOLO (You Only Look Once) technology. My application aims to provide seamless and accurate geospatial insights by detecting and locating trees in large satellite images. With its intelligent preprocessing capabilities, Deep Vision efficiently segments and analyzes satellite imagery, providing latitude and longitude coordinates of detected trees in an easily accessible .csv format.
 

## 1. Key Features :

## A. Precise Object Detection- 
Deep Vision leverages state-of-the-art YOLO technology to detect and identify trees within large TIFF images, ensuring precise and reliable results.

## B. Efficient Preprocessing- 
The app intelligently breaks down large TIFF images into smaller, manageable tiles, streamlining the input for the YOLO model and enhancing overall processing efficiency.

## C. Geospatial Insights- 
By providing latitude and longitude coordinates in the output .csv file, Deep Vision enables users to gain valuable insights into the geographical distribution of trees, facilitating environmental analysis and planning.

## D. User-Friendly Interface- 
Deep Vision is built using the Streamlit framework, providing users with an intuitive and interactive interface for effortlessly uploading, processing, and visualizing satellite images.

## E. User-Friendly Interface- 
Deep Vision is built using the Streamlit framework, providing users with an intuitive and interactive interface for effortlessly uploading, processing, and visualizing satellite images.
## 2. Demo

## A. Pre-Processing
1. Get your .tiff from drone image.
2. Place it in geotiff folder and start run
3. At first,in tiled-geotiff you wil get "tiled-geotiff" of your image.
4. Next, the program will remove all the picture from tiled-geotiff that has >90% white area. 

![Logo](https://gdurl.com/xWwi)


## B. App Overview
1. Part 1

![Logo](https://gdurl.com/VBNf)

2. Part 2

![Logo](https://gdurl.com/ojvz)

## 3. Usage/Examples

```python
git clone https://github.com/your_username/DeepVision.git

cd DeepVision

pip install -r requirements.txt

streamlit run app.py
```
```
# Import necessary libraries
import requests

# Set the API endpoint
url = 'https://api.deepvision.com/upload'

# Define the TIFF image file path
file_path = '/path/to/your/image.tiff'

# Send a POST request to upload the image
files = {'image': open(file_path, 'rb')}
response = requests.post(url, files=files)

# Print the response
print(response.text)

```



## 4. Used By

This project is currently in developmental stage, after execution we have following company that will be using this project:

- Monarch Surveyors & Engineering Consultants Private Limited



## 5. FAQ

#### Python Version?

Answer : 3.9.0

#### Issue with gdal?

Answer: Manual install gdal wheel for your Python version.



## 7. Authors

- [@DataMinerX](https://github.com/DataMinerX)


## 8. License

[MIT](https://choosealicense.com/licenses/mit/)


## 9. Future Development
Deep Vision is committed to continuous improvement and expansion. Our upcoming releases will focus on enhancing user experience, improving performance, and integrating advanced visualization tools for a more comprehensive analysis of geospatial data. We are dedicated to incorporating user feedback and staying at the forefront of technological advancements to ensure that Deep Vision remains an indispensable tool for environmental monitoring and analysis.
