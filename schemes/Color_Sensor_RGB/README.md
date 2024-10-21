# <div align="center"><img src=../../other/img/logo.jpg></img>2023WRO Future Engineers Fire In Half </div>
## <div align="center">TCS34725 Color sensor of Introduction(TCS34725 顏色感測器介紹)</div> 

<div align="center"><img src="./img/TCS34725_RGB.png" alt="D100 Lidar" width="300"></div> 

### 中文
在比賽中，偵測場地上的橘色線與藍色線對我們的機型來說也是非常重要的一環。透過感測這些線的顏色，我們的機型可以判斷是要往順時針跑還是逆時針跑，進而順利完成任務。此外，我們還可以利用這些感測器計算測到線的次數，從而得知機型跑了多少圈，這有助於我們更好地掌握進度。  

TCS34725是我們選擇的色彩感測器，具有以下特點：  
1.高精度色彩感測：能夠準確辨識和測量顏色。  
2.數位輸出：通過 I2C 介面輸出數位色彩資訊，方便與我們的Raspberry Pi 4進行連接和後續處理。  
3.抗紅外線干擾：有效消除紅外線對測量結果的影響，提供更準確的色彩感測。  
4.節能省電：具備低功耗模式，有助於節省能源和延長使用壽命。  
5.小型輕便：體積小巧，適合我們的機型設計。  

__基於以上特點，我們決定使用TCS34725色彩感測器來偵測橘色線與藍色線，以確保我們的機型在比賽中能夠運行順利且準確無誤。__

### English
During the competition, detecting the orange and blue lines on the track is crucial for our robot's performance. By detecting the color of the first line encountered, our robot can determine whether to run clockwise or counterclockwise. Additionally, we can utilize this information to count the number of times the robot crosses the lines, helping us keep track of the laps completed and facilitating the completion of the mission.

The TCS34725 Color Sensor RGB possesses the following features:  
1.High-precision color sensing: It excels in color recognition and measurement capabilities.  
2.Digital output: It provides digital color information through the I2C interface, making it easy to connect to our Raspberry Pi 4 for further processing.  
3.Infrared interference resistance: It effectively eliminates the impact of infrared light on the measurement results, ensuring more accurate color sensing.  
4.Energy-efficient: The sensor has a low-power mode, contributing to energy conservation and prolonging its lifespan.  
5.Compact and lightweight: Its small size and lightweight design make it a suitable choice for our robot's integration.  

__Given these features, we have made the decision to use the TCS34725 Color Sensor RGB as our sensor for detecting the orange and blue lines on the track.__
# <div align="center">![HOME](../../other/img/Home.jpg)[Return Home](../../)</div>  

