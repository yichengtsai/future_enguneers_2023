# Import necessary modules(匯入所需模組)
import cv2 # OpenCV影像辨識模組
import struct # 處理二進位數據的模組
import smbus # 控制I2C總線的模組
import threading # 多線程編程模組
import math # 數學運算模組
import os # 訪問和操作系統模組
import pigpio # 樹莓派 GPIO控制
import numpy as np # 多維陣列與數據處理
import time # 時間模組
import pickle # 序列化和反序列化模組
  
RADIAN_TO_DEGREES = 360/(math.pi *2)
pi = pigpio.pi()

#==========Setting up the pin configuration for each device(各裝置腳位設定)==========
Motor_IN1_pin = 6  
Motor_IN2_pin = 13 
Motor_PWM_pin = 19
Servo_pin = 21     
Red_LED_pin = 22  
Green_LED_pin = 27 
Button_pin = 26    

#==========Vehicle Parameters Configuration(車輛參數設定)==========
# Fine-tuning the servo motor to the center position(伺服馬達置中微調)
servo_offset = -13   

# Setting the DC motor for forward and reverse rotation(直流馬達前、後轉反向設定)
reverse = False    

# Setting the servo motor's turning limit angles(伺服馬達轉彎極限角度設定)
servo_range = 40                

# The minimum recognizable area of the traffic sign(交通標誌最小可辨識面積)
block_detect_min_area = 550     

 # Masking the black areas in the image frame(影像畫面黑色屏蔽範圍)
image_black_area = 260         

 # Adjusting the brightness of the image screen(影像畫面亮度調整)
camera_BRIGHTNESS = 55         
#================================

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, out_min, out_max):
    return out_min if x < out_min else out_max if x > out_max else x
  
# Get the I2C bus(獲取I2C匯流排)
bus = smbus.SMBus(1)

# I2C address of the color sensor
TCS34725_DEFAULT_ADDRESS = 0x29

# TCS34725 Enable Register Configuration
TCS34725_REG_ENABLE_SAI = 0x40 # Sleep After Interrupt
TCS34725_REG_ENABLE_AIEN = 0x10 # ALS Interrupt Enable
TCS34725_REG_ENABLE_WEN = 0x08 # Wait Enable
TCS34725_REG_ENABLE_AEN = 0x02 # ADC Enable
TCS34725_REG_ENABLE_PON = 0x01 # Power ON

# TCS34725 Time Register Configuration
TCS34725_REG_ATIME_2_4 = 0xFF # Atime = 2.4 ms, Cycles = 1
TCS34725_REG_ATIME_24 = 0xF6 # Atime = 24 ms, Cycles = 10
TCS34725_REG_ATIME_101 = 0xDB # Atime = 101 ms, Cycles = 42
TCS34725_REG_ATIME_154 = 0xC0 # Atime = 154 ms, Cycles = 64
TCS34725_REG_ATIME_700 = 0x00 # Atime = 700 ms, Cycles = 256
TCS34725_REG_WTIME_2_4 = 0xFF # Wtime = 2.4 ms
TCS34725_REG_WTIME_204 = 0xAB # Wtime = 204 ms
TCS34725_REG_WTIME_614 = 0x00 # Wtime = 614 ms

# TCS34725 Register Settings
TCS34725_COMMAND_BIT = 0x80
TCS34725_REG_ENABLE = 0x00 # Enables states and interrupts
TCS34725_REG_ATIME = 0x01 # RGBC integration time
TCS34725_REG_WTIME = 0x03 # Wait time
TCS34725_REG_CONFIG = 0x0D # Configuration register
TCS34725_REG_CONTROL = 0x0F # Control register
TCS34725_REG_CDATAL = 0x14 # Clear/IR channel low data register
TCS34725_REG_CDATAH = 0x15 # Clear/IR channel high data register
TCS34725_REG_RDATAL = 0x16 # Red ADC low data register
TCS34725_REG_RDATAH = 0x17 # Red ADC high data register
TCS34725_REG_GDATAL = 0x18 # Green ADC low data register
TCS34725_REG_GDATAH = 0x19 # Green ADC high data register
TCS34725_REG_BDATAL = 0x1A # Blue ADC low data register
TCS34725_REG_BDATAH = 0x1B # Blue ADC high data register

# TCS34725 Gain Configuration
TCS34725_REG_CONTROL_AGAIN_1 = 0x00 # 1x Gain
TCS34725_REG_CONTROL_AGAIN_4 = 0x01 # 4x Gain
TCS34725_REG_CONTROL_AGAIN_16 = 0x02 # 16x Gain
TCS34725_REG_CONTROL_AGAIN_60 = 0x03 # 60x Gain

# Define the TCS34725 class for reading color sensor values(定義TCS34725類別，用於讀取顏色感測器數值)
class TCS34725():
    def __init__(self):
        self.enable_selection()
        self.time_selection()
        self.gain_selection()

    def enable_selection(self):
        """Select the ENABLE register configuration from the given provided values"""
        ENABLE_CONFIGURATION = (TCS34725_REG_ENABLE_AEN | TCS34725_REG_ENABLE_PON)
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_ENABLE | TCS34725_COMMAND_BIT, ENABLE_CONFIGURATION)

    def time_selection(self):
        """Select the ATIME register configuration from the given provided values"""
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_ATIME | TCS34725_COMMAND_BIT, TCS34725_REG_ATIME_2_4)

        """Select the WTIME register configuration from the given provided values"""
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_WTIME | TCS34725_COMMAND_BIT, TCS34725_REG_WTIME_2_4)

    def gain_selection(self):
        """Select the gain register configuration from the given provided values"""
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_CONTROL | TCS34725_COMMAND_BIT, TCS34725_REG_CONTROL_AGAIN_1)

    def readluminance(self):
        """Read data back from TCS34725_REG_CDATAL(0x94), 8 bytes, with TCS34725_COMMAND_BIT, (0x80)
        cData LSB, cData MSB, Red LSB, Red MSB, Green LSB, Green MSB, Blue LSB, Blue MSB"""
        data = bus.read_i2c_block_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_CDATAL | TCS34725_COMMAND_BIT, 8)

        cData = data[1] * 256 + data[0]
        red = data[3] * 256 + data[2]
        green = data[5] * 256 + data[4]
        blue = data[7] * 256 + data[6]
      
        luminance = (-0.32466 * red) + (1.57837 * green) + (-0.73191 * blue)
        return {'c' : cData, 'r' : red, 'g' : green, 'b' : blue, 'l' : luminance}

# Define the opencv_recognition class for traffic sign recognition in images(定義opencv_recognition類別，用於影像辨識交通標誌)
class opencv_recognition():
    def __init__(self, red_upper, red_lower, green_upper, green_lower):
        self.imcap = cv2.VideoCapture(0)
        if not self.imcap.isOpened():
            print("Cannot open camera")
            exit()
        self.imcap.set(cv2.CAP_PROP_BRIGHTNESS, camera_BRIGHTNESS)
        self.thread = False
        self.hsv_red_upper = red_upper
        self.hsv_red_lower = red_lower
        self.hsv_green_upper = green_upper
        self.hsv_green_lower = green_lower
        self.green_x = -1
        self.green_y = -1
        self.green_area = -1
        self.red_x = -1
        self.red_y = -1
        self.red_area = -1
        self.green_node_x = -1
        self.red_node_x = -1
        self.key = 0
        self.program_fps = -1
        self.raw_image = np.zeros((480, 640, 3), np.uint8)
        self.color_read_thread = threading.Thread(target = self.color_recognition)
        self.camera_stream_thread = threading.Thread(target = self.camera_stream)

    def start(self):
        self.thread = True
        self.color_read_thread.start()
        self.camera_stream_thread.start()

    # Read the camera image(讀取鏡頭影像)
    def camera_stream(self):
        while self.thread:
            _, self.raw_image = self.imcap.read()
            self.key = cv2.waitKey(15)

    # Masking a certain part of the image and outputting the processed camera image(屏蔽部分影像及輸出處理過後的鏡頭畫面)
    def color_recognition(self):
        while self.thread:
            reset = time.time()
            img = self.raw_image.copy()
            img[0:image_black_area, 0:640] = [0, 0, 0]
            img[390:480, 0:640] = [0, 0, 0]
            hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            detect_image, self.green_x, self.green_y, self.green_area = self.block_detect((img, hsv_image, self.hsv_green_upper, self.hsv_green_lower)
            detect_image, self.red_x, self.red_y, self.red_area = self.block_detect((img, hsv_image, self.hsv_red_upper, self.hsv_red_lower)
            cv2.imshow('show', result_img)
            self.program_fps = time.time() - reset
        cv2.destroyAllWindows()

    # Detecting the X and Y coordinates of the traffic sign in the camera image(鏡頭影像辨識交通標誌X、Y座標)
    def block_detect(self,raw_img, hsv_img, lower, upper):
        mask = cv2.inRange(hsv_img, lower, upper)  
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        find_x = -1
        find_y = -1
        max_y = 0
        find_area = 0
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            x = int(x + w / 2)
            y = int(y + h / 2)
            if y > max_y and area > block_detect_min_area:
                find_area = area
                max_y = y
                find_x = x
                find_y = y
        cv2.circle(raw_img, (find_x, find_y), 5, (255, 255, 255), -1)
        return raw_img, find_x, find_y, find_area

    def get_program_fps(self):
        return int(1 / self.program_fps)
    
    def get_keyboard(self):
        return self.key
    
    def get_green_node_x(self):
        return self.green_node_x

    def get_green_x(self):
        return self.green_x
    
    def get_green_y(self):
        return self.green_y
    
    def get_green_area(self):
        return self.green_area

    def get_red_node_x(self):
        return self.red_node_x
        
    def get_red_x(self):
        return self.red_x
    
    def get_red_y(self):
        return self.red_y

    def get_red_area(self):
        return self.red_area

    def shutdown(self):
        self.thread = False
        self.color_read_thread.join()
        self.camera_stream_thread.join()
        self.imcap.release()

# Define the button_control class for reading button values(定義button_control類別，用於讀取按鈕數值)
class button_control():
  
    # Set the pin as an input mode and enable the internal pull-up resistor(設置腳位為輸入模式並上拉電阻)
    def __init__(self):
        pi.set_mode(Button_pin, pigpio.INPUT)
        pi.set_pull_up_down(Button_pin, pigpio.PUD_UP)
      
    # Read the button value(讀取按鈕數值)
    def raw_value(self):
        return pi.read(Button_pin)

    # Wait for the button to be released(等待按鈕釋放)
    def wait_release(self):
        state = 0
        while state == 0:
            state = pi.read(Button_pin)

    # Wait for the button to be pressed and then release the button(等待按鈕按下後並釋放按鈕)
    def wait_press_release(self):
        button_state = 1
        while button_state == 1:
            button_state = pi.read(Button_pin)
        button_state = 0
        while button_state == 0:
            button_state = pi.read(Button_pin)

    # Wait for the button to be pressed(等待按鈕按下)
    def wait_press(self):
        state = 1
        while state == 1:
            state = pi.read(Button_pin)
  


# Define the LED_control class for controlling LED on and off(定義LED_control類別，用於控制LED亮、暗)
class LED_control():

    # 定義LED腳位為輸出模式
    def __init__(self):
        pi.set_mode(Red_LED_pin, pigpio.OUTPUT)
        pi.set_mode(Green_LED_pin, pigpio.OUTPUT)
      
    # Turn off the red LED(設置關閉紅色LED)
    def red_off(self):
        pi.write(Red_LED_pin, pigpio.LOW)
      
    # Turn on the red LED(設置開啟紅色LED)
    def red_on(self):
        pi.write(Red_LED_pin, pigpio.HIGH)
      
    # Turn off the green LED(設置關閉綠色LED)
    def green_off(self):
        pi.write(Green_LED_pin, pigpio.LOW)
      
    # Turn on the green LED(設置開啟綠色LED)
    def green_on(self):
        pi.write(Green_LED_pin, pigpio.HIGH)

# Define the dc_motor class for controlling the power output and direction (forward/reverse) of the DC motor(定義dc_motor類別，用於控制直流馬達輸出馬力和正、反轉)
class dc_motor():

    # Define the pin as an output mode(定義腳位為輸出模式)
    def __init__(self):
        pi.set_mode(Motor_IN1_pin, pigpio.OUTPUT)
        pi.set_mode(Motor_IN2_pin, pigpio.OUTPUT)
        pi.set_mode(Motor_PWM_pin, pigpio.OUTPUT)

    # Set the output power for the DC motor(設定直流馬達輸出馬力)
    def power(self, power):
        if power == 0:
            pi.write(Motor_IN1_pin, pigpio.LOW)
            pi.write(Motor_IN2_pin, pigpio.LOW)
            pi.set_PWM_dutycycle(Motor_PWM_pin, 0)
        elif power > 0:
            if reverse == True:
                pi.write(Motor_IN1_pin, pigpio.LOW)
                pi.write(Motor_IN2_pin, pigpio.HIGH)
            else:
                pi.write(Motor_IN1_pin, pigpio.HIGH)
                pi.write(Motor_IN2_pin, pigpio.LOW)
            pi.set_PWM_dutycycle(Motor_PWM_pin, constrain(mapping(power, 0, 100, 0, 255), 0, 255))
        else:
            if reverse == True:
                pi.write(Motor_IN1_pin, pigpio.HIGH)
                pi.write(Motor_IN2_pin, pigpio.LOW)
            else:
                pi.write(Motor_IN1_pin, pigpio.LOW)
                pi.write(Motor_IN2_pin, pigpio.HIGH)
            value = mapping(abs(power), 0, 100, 0, 255)
            pi.set_PWM_dutycycle(Motor_PWM_pin, constrain(mapping(abs(power), 0, 100, 0, 255), 0, 255))

# Define the servo_motor class for setting the angle of the servo motor(定義servo_motor類別，用於設定伺服馬達角度)
class servo_motor():

    # Define the pin as an output mode(定義腳位為輸出模式)
    def __init__(self):
        pi.set_mode(Servo_pin, pigpio.OUTPUT)

    # Set the angle of the servo motor(設定伺服馬達角度)
    def angle(self, turn_angle):
        turn_angle = constrain(turn_angle, -servo_range, servo_range ) * -1
        self.servoangle = turn_angle + 90 + servo_offset
        duty = constrain(mapping(self.servoangle, 0, 180, 500, 2500), 500, 2500)
        pi.set_servo_pulsewidth(Servo_pin, duty)

# Define the lidarSensor class for reading distances from the lidar sensor in all directions(定義lidarSensor類別，用於讀取光達全方位距離)
class lidarSensor():
    def __init__(self, lidar_type):
        if lidar_type == 'D100':
            self.D100_initialization()
        self.Lidar_left = -1
        self.Lidar_right = -1
        self.Lidar_mid = -1

    def D100_initialization(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("/scan", LaserScan, self.D100_lidar_callback)

    # Read the values from the LiDAR sensor(讀取光達數值)
    def D100_lidar_callback(self, data):
        lens = int((data.angle_max - data.angle_min) / data.angle_increment)
        for i in range(lens):
            angle_error = int((data.angle_min + i * data.angle_increment) * RADIAN_TO_DEGREES) - 360
            if angle_error >= 0:
                angle = angle_error % 360 - 180
            else:
                angle = 359 - (-1 - angle_error) % 360 - 180
            ranges = data.ranges[i] * 100
            if not math.isnan(ranges):
                if angle > -5 and angle < 5:
                    # Read the value in front of the LiDAR sensor(讀取光達前方數值)
                    self.Lidar_mid = round(data.ranges[i] * 100)
                if angle > 85 and angle < 95:
                    # Read the value to the left of the LiDAR sensor(讀取光達左方數值)
                    self.Lidar_left = round(data.ranges[i] * 100)
                if angle > -95 and angle < -85:
                    # Read the value to the right of the LiDAR sensor(讀取光達右方數值)
                    self.Lidar_right = round(data.ranges[i] * 100)

# Define the tools class for limiting values within a specific range(定義tools類別，用於將數值限定在範圍內)
class tools():        
    def constrain(self, x, out_min, out_max):
        return out_min if x < out_min else out_max if x > out_max else x       

if __name__ == "__main__":
