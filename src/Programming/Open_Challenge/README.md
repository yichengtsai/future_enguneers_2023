# <div align="center"><img src=../../../other/img/logo.jpg></img>2023WRO Future Engineers Fire In Half </div>

## <div align="center">Open Challenge Program Explanation(資格賽程式說明)</div> 

### Open Challenge Flowchart(資格賽程式流程圖)

<img src="./img/open_challenge_flowchart.png" alt="Open Challenge Flowchart" class="center-image" width=100% height="350" >

#### 中文
- 在競賽中，車輛在行進時需要進行對立柱顏色的影像辨識，以實施避障策略。為實現這一目標，我們利用樹莓派支援的鏡頭模組，進行影像辨識功能的開發。同時，我們也使用樹莓派來控制馬達，以及進行光達距離的偵測。所有這些功能都是透過Python語言來實現的，這使得控制過程更加便捷。  
- 我們可以運用MobaXterm工具中的SSH或VNC功能，連線至樹莓派，以Python撰寫車輛控制程式。 
- 此次競賽所需的程式模組如下：time 、pickle、pigpio、smbus、struct、os、math、cv2、threading、numpy、sys、rospy、LaserScan、signal 

#### English
- In the competition, the vehicle needs to perform color image recognition of opposing pillars while moving to implement obstacle avoidance strategies. To achieve this goal, we utilize the Raspberry Pi's supported camera module to develop the image recognition functionality. Simultaneously, we also use the Raspberry Pi to control the motors and perform LiDAR distance detection. All of these functionalities are implemented using the Python language, which makes the control process more convenient.  
- We can utilize the SSH or VNC functionality within the MobaXterm tool to connect to the Raspberry Pi and write vehicle control programs using Python.  
- The required software modules for this competition are as follows: time 、pickle、pigpio、smbus、struct、os、math、cv2、threading、numpy、sys、rospy、LaserScan、signal 


<div align="center">
<table>
  <tr>
    <th>以MobaXterm中SSH編輯程式</th><th>以MobaXterm中VNC編輯程式</th>
  </tr><tr>
    <td><img src="./img/ssh_main.png" alt="ssh_main" width="300"></td>
    <td><img src="./img/vnc_main.png" alt="vnc_main" width="300"></td>
  <tr>
  </tr>
</table>
</div>

### Explanation of Pseudo code Features.(偽程式特色說明)

#### Record the values measured by the color sensor for the track(紀錄顏色感測器測量完的場地數值)

#### 中文
- 我們運用顏色感測器來偵測場地上藍、橘色線條和白色區域的數值，並透過使用 pickle 模組將這些數值進行紀錄。
- 這樣的設計使得我們可以更靈活地適應不同環境下的數值變化，因為我們能夠輕鬆地保存和載入不同場地所需的數值參數。

#### English
- We utilize a color sensor to detect the values of blue, orange lines, and white areas on the field, and we record these values using the pickle module.
- This design allows us to adapt more flexibly to value variations in different environments, as we can easily save and load the required parameter values for different arenas.

- Program code(程式碼):
```
# 讀取顏色感測器當下數值
color_value = color_sensor_value.readluminance()['c']

# 判斷顏色感測器當下數值是否小於low_value變數所記錄的數值
if color_value < low_value:

    # low_value變數紀錄顏色感測器當下數值
    low_value = color_value
```

```
# 將blue_line變數的數值儲存到value字典中，以 'Blue' 為索引鍵
value['Blue'] = blue_line

# 將orange_line變數的數值儲存到value字典中，以 'Orange' 為索引鍵
value['Orange'] = orange_line

# 將white_area變數的數值儲存到value字典中，以 'white' 為索引鍵
value['white'] = white_area

# 將名為value的字典儲存到record_file資料夾的record_linevalue.p文件中
pickle.dump(value, open('record_file/record_linevalue.p', 'wb') ) 
```

### [record_file](./record_file)

#### 中文
record_file這個資料夾裡存取了從detect_HSV.py中辨識紅綠交通標誌的HSV範圍數值和record_venuelinevalue.py中顏色感測器測量完的藍、橘色線的數值。

#### English
The folder "record_file" contains the HSV range values obtained from the recognition of red and green traffic signs in detect_HSV.py, as well as the values measured from the blue and orange lines using the color sensor in record_venuelinevalue.py.

### [detect_HSV.py](./detect_HSV.py)

#### 中文
這個程式碼透過一個界面利用軌道條來調整HSV色彩範圍，進而識別影像中的紅綠交通標誌，之後將不同的HSV範圍透過record_HSVGreen.p和record_HSVRed.p保存到record_file資料夾中供後續使用。

#### English
This code uses a user interface with trackbars to adjust the HSV color ranges and thereby identify red and green traffic signs in the image. Subsequently, it saves the different HSV ranges as record_HSVGreen.p and record_HSVRed.p files in the save_file folder for later use.

### [record_venuelinevalue.py](./record_venuelinevalue.py)

#### 中文
這段程式碼是一個使用顏色感測器讀取到藍、橘色線數值並將結果透過record_linevalue.p儲存到record_file資料夾中。

#### English
This code is a script that uses a color sensor to read the values of blue and orange lines and then stores the results in a file named "record_linevalue.p" in the "record_file" folder.

### [Self_Driving_Car_Function.py](./Self_Driving_Car_Function.py)

#### 中文
這個程式碼是一個函式，透過使用樹梅派(raspberry pi)搭配各種感測器以及鏡頭，達到透過影像處理與控制系統能夠辨識紅綠交通標誌，讀取顏感數值，並能夠控制直流馬達轉速與轉向以及伺服馬達轉向角度。

#### English
This code is a function that utilizes a Raspberry Pi along with various sensors and a camera to achieve the capability of recognizing red and green traffic signs through image processing and control systems. Additionally, it can read color sensor values and control the speed and direction of DC motors as well as the steering angle of servo motors.

### [Open_Challenge.py](./Open_Challenge.py)

#### 中文
這段程式碼是使車輛能與兩側邊牆保持一定距離並透過讀取顏色感測器數值偵測地板上的藍、橘線讓車輛能分辨方向，使車輛能完成任務。

#### English
This code enables the vehicle to maintain a certain distance from both side walls and detect blue and orange lines on the floor using color sensor readings to determine its direction. This allows the vehicle to complete its task.

# <div align="center">![HOME](../../../other/img/Home.jpg)[Return Home](../../../)</div>  
