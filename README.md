
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


## 6. Lessons Learned

What did you learn while building this project? What challenges did you face and how did you overcome them?

Technology Considerations: Discuss the challenges and benefits of integrating various technologies like YOLO, GDAL, Pandas, Rasterio, Streamlit, and Folium. Elaborate on how each library impacted the performance, scalability, and user experience of your application.

Data Handling Challenges: Share the lessons learned from handling large TIFF images, including the preprocessing techniques used and any issues encountered during the data segmentation process. Discuss how you optimized the handling of large data sets for efficient processing.

User Experience Insights: Detail the feedback received during the development and deployment phases, including any usability issues, feature requests, or suggestions for improvements. Discuss how you incorporated user feedback into the design and functionality of your application.

Performance Optimization Strategies: Explain the strategies employed to optimize the performance of your application, such as load time reduction, memory management techniques, and code optimization practices. Reflect on the impact of these strategies on the overall user experience and application efficiency.

Integration Challenges: Share the lessons learned from integrating multiple libraries and frameworks within your application. Discuss any compatibility issues, version conflicts, or other technical challenges that arose during the integration process and how you resolved them.

Scalability Considerations: Discuss the considerations for scaling your application to handle a growing user base and increasing data volumes. Include insights into potential infrastructure changes, data storage solutions, and processing enhancements that may be necessary for future scalability.

User Security and Privacy: Reflect on the importance of ensuring data security and user privacy within your application. Discuss the measures taken to secure user data, prevent unauthorized access, and comply with relevant data protection regulations.

Community Engagement: Document the lessons learned from engaging with the developer community, including the benefits of open-source collaboration, the value of user feedback, and the impact of community contributions on the development of your application.
## 7. Authors

- [@DataMinerX](https://github.com/DataMinerX)


## 8. License

[MIT](https://choosealicense.com/licenses/mit/)


## 9. Future Development
Deep Vision is committed to continuous improvement and expansion. Our upcoming releases will focus on enhancing user experience, improving performance, and integrating advanced visualization tools for a more comprehensive analysis of geospatial data. We are dedicated to incorporating user feedback and staying at the forefront of technological advancements to ensure that Deep Vision remains an indispensable tool for environmental monitoring and analysis.
