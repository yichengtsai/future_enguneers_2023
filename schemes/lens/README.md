# <div align="center"><img src=../../other/img/logo.jpg></img>2023WRO Future Engineers Fire In Half </div>
## <div align="center">Lens of Introduction(鏡頭介紹)</div> 

### Lens Modle Selection(鏡頭模組選擇)

- 鏡頭屬於自走車重要的零件之一，我們決定拿3.6mm Lens Raspberry Pi 5MP IR Camera(以下稱為一代)、Raspberry Pi Camera Moudule V2(以下稱為二代)與 Raspberry Pi camera V3(以下稱為三代)來做比較，一代只有500萬像素與30fps，二代有800萬像素與最高可達90fps，而三代鏡頭與我們的樹莓派系統不相融所以無法使用，所以我們決定使用性能更好的二代。

- The lens is one of the important components of the self-driving car. We decided to compare the 3.6mm Lens Raspberry Pi 5MP IR Camera (referred to as the first generation), Raspberry Pi Camera Module V2 (referred to as the second generation), and Raspberry Pi camera V3 (referred to as the third generation). The first generation has 5 megapixels and 30fps, the second generation has 8 megapixels and can reach up to 90fps, while the third-generation lens is not compatible with our Raspberry Pi system, so we decided to use the higher-performance second generation.



<table>
  <tr>
    <th>名稱</th>
    <th>實體照</th>
    <th>幀數</th>
    <th>分辨率</th>
    <th>感測器</th>
  </tr>
  <tr>
    <td>3.6mm Lens Raspberry Pi 5MP IR Camera</td>
    <td><img src=./img/IMG_2642.png width=300/></td>
    <td>30fps</td>
    <td>500萬像素</td>
    <td>OV5647</td>
  </tr>
  <tr>
    <td>Raspberry Pi Camera Moudule V2</td>
    <td><img src=./img/IMG_2643.png width=300/></td>
    <td>90fps</td>
    <td>800萬像素</td>
    <td>Sony IMX708</td>
  </tr>
   <tr>
    <td>Raspberry Pi camera V3</td>
    <td><img src=./img/IMG_2644.png width=300/></td>
    <td>90fps</td>
    <td>1190萬像素</td>
    <td>Sony IMX708</td>
  </tr>
</table>


### Wide-angle Lens(廣角鏡頭)
- 在選定了二代鏡頭後，我們在網上發現可以手動更換成IMX219廣角攝影鏡頭。這使我們再次進行了比較。原本的二代鏡頭只有77度的視野，但更換成廣角鏡頭後，視野可達160度。經過測試，廣角鏡頭讓我們的機型能夠提前看到下一個積木，大大地提升了鏡頭辨識偵測的效率。因此，我們決定採用IMX219廣角攝影鏡頭。

- After choosing the second-generation lens, we discovered online that it could be manually replaced with an IMX219 wide-angle lens. This led us to conduct another comparison. The original second-generation lens had a field of view of only 77 degrees, but after replacing it with the wide-angle lens, the field of view increased to 160 degrees. Through testing, we found that the wide-angle lens allowed our vehicle to detect the next block much earlier, significantly improving the efficiency of the camera's recognition and detection. Therefore, we decided to adopt the IMX219 wide-angle lens.

<div align="center">
<table>
  <tr>
    <th>Raspberry Pi Camera Moudule V2</th><th>IMX219廣角攝影鏡頭</th>
  </tr><tr>
    <td><img src="./img/IMG_2643.png" alt="car view" width="400"></td>
    <td><img src="./img/IMX219_160.png" alt="IMX219廣角160度攝影鏡頭" width="300"></td>
  <tr>
  </tr>
</table>
</div>

### Lens Parameter Adjustment (鏡頭參數調整)
 在樹莓派的設定中，我們可以選擇不同的鏡頭讀取畫質，共有三種選擇：
 1. 1080X640p,30fps
 2. 640X480p,60fps
 3. 320X240p,90fps

- 經過測試發現，畫質最高的選項因所需的效能較高，幀數較低，導致來不及辨識，常常撞到積木；而幀數最高的選項，雖然速度較快，但由於畫質降低，仍然會辨識不到積木，仍然會撞到。因此，我們決定選擇中間值640X480p,60fps，這樣的設置能夠既保證辨識到積木，又能及時做出反應。

In the Raspberry Pi settings, we have the option to choose from three different camera resolutions:
1. 1080X640p, 30fps
2. 640X480p, 60fps
3. 320X240p, 90fps

- After conducting tests, we found that the highest resolution option requires higher performance but has lower frame rates, resulting in insufficient time for object recognition and often leading to collisions with blocks. On the other hand, the option with the highest frame rate has lower image quality, which still causes difficulty in recognizing blocks and results in collisions. Therefore, we have decided to choose the middle option, 640X480p at 60fps, as this setting ensures both accurate object recognition and timely response.

<div align="center">
<table>
  <tr>
    <th>二代鏡頭畫面(無廣角)</th><th>二代鏡頭畫面(廣角)</th>
  </tr><tr>
    <td><img src="./img/V2_not.png" alt="二代畫面(無廣角)" width="300"></td>
    <td><img src="./img/V2_160.png" alt="二代畫面(廣角)" width="300"></td>
  <tr>
  </tr>
</table>
</div>

# <div align="center">![HOME](../../other/img/Home.jpg)[Return Home](../../)</div>  
