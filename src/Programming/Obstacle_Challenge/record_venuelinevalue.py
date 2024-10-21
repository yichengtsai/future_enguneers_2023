#Import necessary modules(匯入所需模組)
from Self_Driving_Car_Function import*
import time # 時間模組
import pickle # 序列化和反序列化模組

# button變數創建button_control類別用於按鈕控制的實例
button = button_control()

# color_sensor_value變數創建TCS34725類別用於顏色感測器物件的實例
color_sensor_value = TCS34725()

white_area = -1
orange_line = -1
blue_line = -1

# Function to record the file(紀錄檔案的函式))
def file_write():
    print('\n=======file write down=======')
    print('Orange:' + str(orange_line))
    print('Blue:' + str(blue_line))
    print('white:' + str(white_area))
    value = {}
    # 將blue_line、orange_line和white_area變數放入value陣列中
    value['Blue'] = blue_line
    value['Orange'] = orange_line
    value['white'] = white_area
    print('Write Finish')
    pickle.dump(value, open('record_file/record_linevalue.p', 'wb') )

# Function to record the values of the white area(紀錄白色區域數值的函式)
def white_area_read():
    global white_area # Declare the variable white_area as a global variable(將white_area變數聲明為全域變數)
    print('=======white area=======')
    print('wait button')
    button.wait_press_release()
    print('start white area\n')
    state = 1
    low_value = 100
    while state == 1:
        state = button.raw_value()
        color_value = color_sensor_value.readluminance()['c']
        if color_value < low_value:
            low_value = color_value
            print('  white:' + str(low_value))
        time.sleep(0.01)
    button.wait_release()
    # The variable "white_area" records the values of the white area(white_area變數紀錄白色區域數值)
    white_area = low_value

# Function to record the values of the orange lines(紀錄橘色線條數值的函式)
def orange_line_read():
    print('\n=======orange line=======')
    print('wait button')
    button.wait_press_release()
    print('start orange line\n')
    state = 1
    low_value = 100
    while state == 1:
        state = button.raw_value()
        
        color_value = color_sensor_value.readluminance()['c']
        if color_value < low_value:
            low_value = color_value
            print('  Orange:' + str(low_value))
        time.sleep(0.01)
    button.wait_release()
    # The variable "orange_line" records the values of the orange lines(orange_line變數紀錄橘色線條數值)
    orange_line = low_value 

# Function to record the values of the blue lines(紀錄藍色線條數值的函式)
def blue_line_read():
    print('\n=======blue line=======')
    print('wait button')
    button.wait_press_release()
    print('start blue line\n')
    state = 1
    low_value = 100
    while state == 1:
        state = button.raw_value()
        
        color_value = color_sensor_value.readluminance()['c']
        if color_value < low_value:
            low_value = color_value
            print('  Blue:' + str(low_value))
        time.sleep(0.01)
    button.wait_release()
    # The variable "blue_line" records the values of the blue lines(blue_line變數紀錄藍色線條數值)
    blue_line = low_value

# Call the function(呼叫函式)
white_area_read()
orange_line_read()
blue_line_read()
file_write()
