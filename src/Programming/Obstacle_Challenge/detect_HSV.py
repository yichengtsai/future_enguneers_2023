#Import necessary modules(匯入所需模組)
from Self_Driving_Car_Function import*

# Capture streaming video from the webcam(擷取網路攝影機串流影像)
imcap = cv2.VideoCapture(0)

# Set the image capture width to 480 pixels(設定影像擷取的寬度為480像素)
imcap.set(3, 480)

# Set the image capture height to 360 pixels(設定影像擷取的高度為360像素)
imcap.set(4, 360)

# Set the image capture frame rate (FPS) to 40(設定影像擷取的幀率（FPS）為40)
imcap.set(cv2.CAP_PROP_FPS, 40)

# Set the image capture buffer size to 1 frame(設定影像擷取的緩衝區大小為1幀)
imcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Set the image capture brightness to 55(設定影像擷取的亮度為55)
imcap.set(cv2.CAP_PROP_BRIGHTNESS, 55)

# Set the image capture contrast to 0(設定影像擷取的對比度為0)
imcap.set(cv2.CAP_PROP_CONTRAST, 0)

# Set the image capture exposure to 0(設定影像擷取的曝光度為0)
imcap.set(cv2.CAP_PROP_EXPOSURE, 0)

# Adjust the size and shape of objects in the image(調整影像中的物體大小和形狀)
kernal = np.ones((4,4), np.uint8)

img2 = np.zeros((300,512,3), np.uint8)
img = np.uint8(np.clip((cv2.add(1*img2,30)),0,255))
img1 = np.uint8(np.clip((cv2.add(1.5*img2,100)),0,255))
img2 = np.hstack((img2,img1,img))
cv2.namedWindow('image')

# 建立用於調整顏色的軌道條
cv2.createTrackbar('H_low','image',0,255,nothing)
cv2.createTrackbar('H_high','image',255,255,nothing)
cv2.createTrackbar('S_low','image',0,255,nothing)
cv2.createTrackbar('S_high','image',255,255,nothing)
cv2.createTrackbar('V_low','image',0,255,nothing)
cv2.createTrackbar('V_high','image',255,255,nothing)

def print_mes():
    print('---------------')
    print('1, set Green')
    print('2, set Red')
    print('3, HSV value reset.')
    print('4, Write green.')
    print('5, Write red.')
    print('---------------')
    
def nothing(x):
    pass

print_mes()

while(1):
    # Get the position value of the trackbar(獲取軌跡條的位置值)
    H_high = cv2.getTrackbarPos('H_high','image')
    H_low = cv2.getTrackbarPos('H_low','image')
    S_high = cv2.getTrackbarPos('S_high','image')
    S_low = cv2.getTrackbarPos('S_low','image')
    V_high = cv2.getTrackbarPos('V_high','image')
    V_low = cv2.getTrackbarPos('V_low','image')

    # Screen Image Capture(螢幕影像擷取)
    success, img = imcap.read()

    # Convert the image to the HSV color space(將影像轉換成HSV色彩空間)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # The hsv_low array records the minimum values of HSV components(hsv_low陣列中紀錄HSV各個的最低值)
    hsv_low = np.array([H_low, S_low, V_low])

    # The hsv_high array records the maximum values of HSV components(hsv_high陣列中紀錄HSV各個的最高值)
    hsv_high = np.array([H_high, S_high, V_high])
    
    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    res = cv2.bitwise_and(img, img, mask=mask)
    
    cv2.imshow('image',res)
    
    k = cv2.waitKey(25) & 0xFF

    if k == ord('1'):
        # Read the values of record_HSVRed from the record_file folde(讀取record_file資料夾中record_HSVRed的數值)
        with open('record_file/record_HSVRed.p', mode='rb') as f:
            file = pickle.load(f)
        Red_Lower = file['Lower']
        Red_Upper = file['Upper']
        cv2.setTrackbarPos('H_high','image', Red_Upper[0])
        cv2.setTrackbarPos('H_low','image', Red_Lower[0])
        cv2.setTrackbarPos('S_high','image', Red_Upper[1])
        cv2.setTrackbarPos('S_low','image', Red_Lower[1])
        cv2.setTrackbarPos('V_high','image', Red_Upper[2])
        cv2.setTrackbarPos('V_low','image', Red_Lower[2])
        print('Red_set')
        print_mes()
    
    if k == ord('2'):
        # Read the values from the file "record_HSVGreen" in the "record_file" directory(讀取record_file資料夾中record_HSVGreen的數值)
        with open('record_file/record_HSVGreen.p', mode='rb') as f:
            file = pickle.load(f)
        Green_Lower = file['Lower']
        Green_Upper = file['Upper']
        cv2.setTrackbarPos('H_high','image', Green_Upper[0])
        cv2.setTrackbarPos('H_low','image', Green_Lower[0])
        cv2.setTrackbarPos('S_high','image', Green_Upper[1])
        cv2.setTrackbarPos('S_low','image', Green_Lower[1])
        cv2.setTrackbarPos('V_high','image', Green_Upper[2])
        cv2.setTrackbarPos('V_low','image', Green_Lower[2])
        print('Green_set')
        print_mes()


    if k == ord('3'):
        # Set the initial values for the trackbars(設定軌跡條的基礎數值)
        cv2.setTrackbarPos('H_high','image', 255)
        cv2.setTrackbarPos('H_low','image', 0)
        cv2.setTrackbarPos('S_high','image', 255)
        cv2.setTrackbarPos('S_low','image', 0)
        cv2.setTrackbarPos('V_high','image', 255)
        cv2.setTrackbarPos('V_low','image', 0)
        print('Reset')
        print_mes()

    if k == ord('4'):

        print('====Red HSV====')
        hsv_value = {}
        hsv_value['Lower'] = [H_low, S_low, V_low]
        hsv_value['Upper'] = [H_high, S_high, V_high]
        print('lower:' + str(hsv_value['Lower']))
        print('upper:' + str(hsv_value['Upper']))
        print('Write Finish')
        # Record the values of record_HSVRed(紀錄record_HSVRed的數值)
        pickle.dump(hsv_value, open('record_file/record_HSVRed.p', 'wb') )
        print_mes()
    
    if k == ord('5'):

        print('====Green HSV====')
        hsv_value = {}
        hsv_value['Lower'] = [H_low, S_low, V_low]
        hsv_value['Upper'] = [H_high, S_high, V_high]
        print('lower:' + str(hsv_value['Lower']))
        print('upper:' + str(hsv_value['Upper']))
        print('Write Finish')
        # Record the values of record_HSVGreen(紀錄record_HSVGreen的數值)
        pickle.dump(hsv_value, open('record_file/record_HSVGreen.p', 'wb') )
        print_mes()



    if k == 27:
        break
        
# Release the resources occupied by the camera and other related components(釋放相機等相關資源的佔用)
imcap.release()

# Close all windows created by OpenCV(關閉所有OpenCV創建的視窗)
cv2.destroyAllWindows()
