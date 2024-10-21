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

turn_direction = [0, -90, -180, -270]
pluse_turn = -90
Final_Direction = -270

line_middle = 0
color_direction_middle = 0
white_area = 0

record_box = ''
RADIAN_TO_DEGREES = 180000/3141.59
lidar_data = 0
color = 0
k = 0

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

# Use the LiDAR to center the vehicle between the two side walls(透過光達使車輛置中於兩側邊牆中間)
def center_control():
    left, mid, right = lidar_get_distance()
    if left > 0 and right > 0 and left < 100 and right < 100:
        center_error = (right - left) / 1.8
    elif right < 0 or right > 120:
        center_error = 48 - left
    else:
        center_error = right - 48
    servo.angle(center_error * 2 + gyro * 1.4)
    return left, mid, right

def handler(signum, frame):
    exit(0)

# Read the values from the color sensor(讀取顏色感應器數值)
def color_read():
    global color
    while thread_run:
        # The color variable records the current values from the color sensor(color變數紀錄顏感當下數值)
        color = color_sensor.readluminance()['c']
        time.sleep(0.01)
#=====================main=====================
try:
    # Define multiple threads(定義多執行序)
    color_thread = threading.Thread(target = color_read)
 
    # Call the function to execute(呼叫函式執行)
    linevalue_read()
    color_thread.start()

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
    while button_state == 1:
        button_state = button.raw_value()
        time.sleep(0.05)
        left, mid, right, gyro = lidar_get_distance(0)
        print('left:', left, ' mid:', mid, ' right:', right)
    print('start run')
    motor.power(-70)
    #=============start(開始)=============
    get_left_dis=50
    get_right_dis=50
    get_mid_dis=195
    reverse=False
    count_1=0
    while get_left_dis < 120 and get_right_dis < 120:
        get_left_dis, get_mid_dis, get_right_dis, gyro_1 = lidar_get_distance(turn_direction[count_1])
        servo.angle(0)
    if get_left_dis < get_right_dis:
        turn_direction = [0, 90, -180, -90]
        reverse=True
    reset = time.time()
    while time.time() - reset < 2:
        get_left_dis, get_mid_dis, get_right_dis = center_control(turn_direction[(count_1+1)%4])
    count_1 = 1
    if reverse == True:
        for a in range(3):
            while count_1 < 12:
                get_right_dis=50
                get_mid_dis=150
                while get_right_dis < 100 or get_mid_dis > 90:
                    get_left_dis, get_mid_dis, get_right_dis = center_control(turn_direction[count_1%4])  
                reset = time.time()
                while time.time() - reset < 1.5:
                    get_left_dis, get_mid_dis, get_right_dis = center_control(turn_direction[(count_1+1)%4])
                count_1+=1
    else:
        for a in range(3):
            while count_1 < 12:
                get_left_dis=50
                get_mid_dis=150
                while get_left_dis < 100 or get_mid_dis > 90:
                    get_left_dis, get_mid_dis, get_right_dis = center_control(turn_direction[count_1%4])
                reset = time.time()
                while time.time() - reset < 1.5:
                    get_left_dis, get_mid_dis, get_right_dis = center_control(turn_direction[(count_1+1)%4])
                count_1+=1
    #=============End(結束)=============
finally:
    print('\nshutdown')
    motor.power(0)
    servo.angle(0)
    thread_run = False
