#Import necessary modules(匯入所需模組)
from Self_Driving_Car_Function import*
from sensor_msgs.msg import LaserScan # 定義光達數據格式
import rospy # Python的客戶端庫

# Using the LED_control class to control the LED lights(使用LED_control類別用於控制LED燈)
LED = LED_control()

# Using the button_control class to control the buttons(使用button_control類別用於控制按鈕)
button = button_control()

# Using the dc_motor class to control the DC motors(使用dc_motor類別用於控制直流馬達)
motor = dc_motor()

# Using the servo_motor class to control the servo motors(使用servo_motor類別用於控制伺服馬達)
servo = servo_motor()

# Using the TCS34725 class to read the color sensor(使用TCS34725類別用於讀取顏色感測器)
color_sensor = TCS34725()

# Using the Tools class(使用tools類別)
mapping = tools()

thread_run = True
lidar_run = False

RADIAN_TO_DEGREES = 180000/3141.59
lidar_data = 0

turn_direction = [0, -90, -180, -270]
pluse_turn = -90
Final_Direction = -270

line_middle = 0
color_direction_middle = 0
white_color = 0

green_lower = 0
green_upper = 0
red_lower = 0
red_upper = 0
record_box = ''

count = 0
color = 0
k = 0
back=0
last_time=0

def lidar_callback(data):
    global lidar_data, lidar_run
    lidar_data = data
    lidar_run = True

# Read the values from the LiDAR for the left, front, and right directions(讀取光達左方、前方和右方的數值)
def lidar_get_distance():
    lens = int((lidar_data.angle_max - lidar_data.angle_min) / lidar_data.angle_increment) - 1
    mid = -1
    left = -1
    right = -1
    for i in range(lens):
        angle_error = int((lidar_data.angle_min + i * lidar_data.angle_increment) * RADIAN_TO_DEGREES) + 180
        if angle_error >= 0:
            angle = angle_error % 360 - 180
        else:
            angle = 359 - (-1 - angle_error) % 360 - 180
        ranges = lidar_data.ranges[i] * 100
        if not math.isnan(ranges):
            if abs(angle) < 5:
                # The variable "mid" records the LiDAR value in the front direction(mid變數紀錄光達前方數值)
                mid = int(ranges)
            if abs(angle - 90) < 5:
                # The variable "left" records the LiDAR value in the left direction(left變數紀錄光達左方數值)
                left = int(ranges)
            if abs(angle + 90) < 5:
                # The variable "right" records the LiDAR value in the right direction(right變數紀錄光達右方數值)
                right = int(ranges)
        if mid > 0 and left > 0 and right > 0:
            break
    # Return the LiDAR values in the left, front, and right directions(回傳光達左方、前方和右方的數值)
    return left, mid, right
    
# Read the values of blue line, orange line, and white area(讀取藍、橘色線條和白色區域的數值)
def linevalue_read():
    global line_middle, color_direction_middle, white_area 
    with open('record_file/record_linevalue.p', mode='rb') as f:
        file = pickle.load(f)
    blue_line = file['Blue']
    orange_line = file['Orange']
    white_area = file['white']
    color_direction_middle = (blue_line + orange_line) / 2 + 2
    line_middle = (white_area + orange_color) / 2
 
    print('orange:' + str(orange_line))
    print('blue:' + str(blue_line))
    print('white:' + str(white_area))
    print('direction_middle:', color_direction_middle)
    print('line middle:', line_middle)
    print('=======================')

# Read the HSV values of the traffic sign(讀取交通標誌的HSV數值)
def block_colorvalue_read():
    global green_lower, green_upper, red_lower, red_upper
    with open('record_file/record_HSVGreen.p', mode='rb') as f:
        file = pickle.load(f)
    g_lower = file['Lower']
    g_upper = file['Upper']
    print('Green_Lower:' + str(g_lower))
    print('Green_Upper:' + str(g_upper))
    
    with open('record_file/record_HSVRed.p', mode='rb') as f:
        file = pickle.load(f)
    r_lower = file['Lower']
    r_upper = file['Upper']
    print('Red_Lower:' + str(r_lower))
    print('Red_Upper:' + str(r_upper))
    
    red_lower = np.array(r_lower, np.uint8) 
    red_upper = np.array(r_upper, np.uint8)
    green_lower = np.array(g_lower, np.uint8)
    green_upper = np.array(g_upper, np.uint8)

# Read the values from the color sensor(讀取顏色感應器數值)
def color_read():
    global color
    while thread_run:
        # The color variable records the current values from the color sensor(color變數紀錄顏感當下數值)
        color = color_sensor.readluminance()['c']
        time.sleep(0.01)

# Image recognition controls the servo motor to avoid traffic signs(影像辨識控制伺服馬達閃避交通標誌)
def dodgeblock_control(set_gyro):
    global record_box, back, last_time, count
    if opencv_detect.get_red_y() == -1 and opencv_detect.get_green_y() == -1:
        left, mid, right = lidar_get_distance()
        if left > 0 and right > 0:
            center_error = (right - left) / 1.8
        elif left > 0:
            center_error = 48 - left
        else:
            center_error = right - 48
        servo_angle = center_error * 1.1
    elif opencv_detect.get_red_y() > opencv_detect.get_green_y():
        if opencv_detect.get_red_y() > 340:
            record_box = 'red'
        servo_angle = (opencv_detect.get_red_x() - opencv_detect.get_red_node_x()) * 0.12
    else:
        if opencv_detect.get_green_y() > 340:
            record_box = 'green'
        servo_angle =  (opencv_detect.get_green_x() - opencv_detect.get_green_node_x()) * 0.11
    servo.angle(servo_angle)

# Avoid traffic signs until the color sensor detects a line(閃避交通標誌到顏色感測器偵測到線)
def dodgeblock_to_line():
    global count, back
    while color > line_middle:
        dodgeblock_control()
        time.sleep(0.001)

# Avoid traffic signs until the specified time elapses(閃避交通標誌到設定的時間)
def dodgeblock_to_time(set_time):
    set_reset = time.time()
    while time.time() - set_reset < set_time:
        dodgeblock_control()
        time.sleep(0.001)

# Using the color sensor to determine the car's driving direction(使用顏色感測器判斷汽車行走方向)
def direction_detect():
    global turn_direction, pluse_turn, reverse_angle
    print('direction detect')
    while color > line_middle:
        dodgeblock_control(0)
    low_color = 100
    while color < line_middle:
        dodgeblock_control(0)
        if color < low_color:
            low_color = color
    if low_color < color_direction_middle:
        print('blue line')
        reverse_angle = -270
    else:
        print('orange line')
        turn_direction = [0, 90, 180, 270]
        pluse_turn = 90
        reverse_angle = 270

def handler(signum, frame):
    exit(0)
#=====================main=====================
try:
    # Define threads(定義多執行序)
    color_read_thread = threading.Thread(target = color_read)
    # Call a function(呼叫函式)
    linevalue_read()
    block_colorvalue_read()
    color_read_thread.start()
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, lidar_callback)
    signal.signal(signal.SIGINT, handler)
    print('ros callback ...')
    while not lidar_run:
        pass
    print('ros running...\n')
    servo.angle(0)
    print('waitting start ...')
    button_state = 1
    while button_state == 1 and not opencv_detect.get_keyboard() == ord('g'):
        button_state = button.raw_value()
        time.sleep(0.05)
    print('start run')
    motor.power(-67)
    direction_detect()
    dodgeblock_to_time(1.2, pluse_turn)
    for angle in turn_direction:
        motor.power(-67)
        count = count + 1
        if count == 1:
            continue
        dodgeblock_to_line_detect(angle)
        motor.power(-62)
        if count==4:
            dodgeblock_to_time(1.2, angle + pluse_turn)
        else:
            dodgeblock_to_time_detect(1.2, angle + pluse_turn)
    turn_direction.pop()
    for angle in turn_direction:
        motor.power(-67)
        count = count + 1
        dodgeblock_to_line(angle)
        motor.power(-62)
        dodgeblock_to_time(1.2, angle + pluse_turn)
        
    if record_box == 'red' and reverse_angle==270:
        dodgeblock_to_line(reverse_angle)
        print('mid', mid)
        gyro_1=0
        motor.power(-75)
        while gyro_1 > 160 or gyro_1 < 150:
            left, mid, right = lidar_get_distance()
            servo.angle(-95)
        motor.power(-65)
        dodgeblock_to_time(0.8, 90)
        turn_direction_1 = [90, 0, -90]
        pluse_turn = -90
        for angle in turn_direction_1:
            count = count + 1
            print('count:', count)
            dodgeblock_to_line(angle)
            dodgeblock_to_time(1, angle + pluse_turn)
    elif record_box == 'red' and reverse_angle==-270:
        dodgeblock_to_line(reverse_angle)
        print('mid', mid)
        gyro_1=0
        motor.power(-75)
        while gyro_1 > 160 or gyro_1 < 150:
            left, mid, right, gyro_1 = lidar_get_distance()
            servo.angle(-95)
            print(gyro_1)
        motor.power(-65)
        dodgeblock_to_time(0.8, -90)
        turn_direction_1 = [-90, 0, 90]
        pluse_turn = 90
        for angle in turn_direction_1:
            count = count + 1
            print('count:', count)
            dodgeblock_to_line(angle)
            dodgeblock_to_time(1, angle + pluse_turn)
    else:
        if reverse_angle==-270:
            pluse_turn=-90
            turn_direction_1 = [90, 0, -90, -180, 90]
            for angle in turn_direction_1:
                count = count + 1
                print('count:', count)
                dodgeblock_to_line(angle)
                dodgeblock_to_time(1, angle + pluse_turn)
        else:
            pluse_turn=90
            turn_direction=[-90, 0, 90, 180, -90]
            for angle in turn_direction:
                count = count + 1
                print('count:', count)
                dodgeblock_to_line(angle)
                dodgeblock_to_time(1, angle + pluse_turn)
    #=============End(結束)=============
finally:
    print('record_box:', record_box)
    print('\nshutdown')
    motor.power(0)
    servo.angle(0)
    thread_run = False
    color_read_thread.join()
    opencv_detect.shutdown()# Stop the OpenCV image recognition function and streaming(opencv影像辨識功能停止串流)
