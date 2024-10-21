# <div align="center"><img src=../../other/img/logo.jpg></img>2023WRO Future Engineers Fire In Half </div>
# <div align="center">OpenCV of Introduction</div>


![image](./img/opencv.png)

## 中文介紹
- OpenCV（全稱Open Source Computer Vision Library）是一個開源的計算機視覺庫，旨在提供一系列用於處理圖像和視頻的功能。它最初由Intel於1999年開發，並在後來得到了廣泛的社區支持和貢獻。OpenCV支持多個編程語言，如C++、Python、Java等，使其可以在不同平台上運行。  
- OpenCV提供了大量的圖像處理和計算機視覺算法，包括圖像濾波、特徵檢測、目標識別、物體跟踪、人臉識別、機器學習等功能。它的廣泛應用領域包括計算機視覺研究、機器人技術、自動駕駛、安防監控、醫學圖像處理等。
- OpenCV的優勢在於其開源自由的特性，使得研究人員、開發者和學生都可以免費使用和修改代碼。它還具有強大的社區支持，用戶可以在社區中獲得幫助、交流經驗和分享成果。

## English of Introduction
- OpenCV (Open Source Computer Vision Library) is an open-source computer vision library designed to provide a set of functions for image and video processing. It was originally developed by Intel in 1999 and has since gained extensive community support and contributions. OpenCV supports multiple programming languages, such as C++, Python, Java, allowing it to run on various platforms.

- OpenCV offers a wide range of image processing and computer vision algorithms, including image filtering, feature detection, object recognition, object tracking, face detection, machine learning, and more. Its diverse applications include computer vision research, robotics, autonomous driving, surveillance and security, medical image processing, among others.

- One of the key advantages of OpenCV is its open-source and free nature, enabling researchers, developers, and students to use and modify the code without any cost. It also benefits from a strong community support system, where users can seek help, exchange experiences, and share their accomplishments.


## installation steps(安裝步驟)
### 中文
步驟 1:先安裝好作業系統。  
可參考 安裝Linux 在Raspberry Pi4。

步驟2:更新當前安裝的軟體。
```
$ sudo apt-get update
$ sudo apt-get upgrate
```
步驟3:安裝 OpenCV 編譯所需的軟體。  
```
$ sudo apt-get install cmake build-essential pkg-config git
`````
步驟4:安裝常用圖像和視頻格式的支援軟體。  
```
$ sudo apt-get install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394–22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
```
步驟5:安裝 OpenCV 界面所需的軟體。  
```
$ sudo apt-get install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
```
步驟6:安裝提高 OpenCV 運行速度的軟體。  
```
$ sudo apt-get install libatlas-base-dev liblapacke-dev gfortran
```
步驟7:安裝 Python。  
```
$ sudo apt-get install python3-dev python3-pip python3-numpy
### English
```
### English
Step 1: Install the operating system first.
You can refer to "Installing Linux on Raspberry Pi 4."

Step 2: Update the currently installed software.
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
Step 3: Install the required software for compiling OpenCV.
```
$ sudo apt-get install cmake build-essential pkg-config git
```
Step 4: Install the support software for common image and video formats.
```
$ sudo apt-get install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394–22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
```
Step 5: Install the required software for OpenCV's user interface.
```
$ sudo apt-get install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
```
Step 6: Install software to enhance OpenCV's performance.
```
$ sudo apt-get install libatlas-base-dev liblapacke-dev gfortran
```
Step 7: Install Python.
```
$ sudo apt-get install python3-dev python3-pip python3-numpy
```


# <div align="center">![HOME](../../other/img/Home.jpg)[Return Home](../../)</div>  
