# <div align="center"><img src=../../other/img/logo.jpg></img>2023WRO Future Engineers Fire In Half </div>
## <div align="center">Power Management(電源管理)</div> 

- ### 供電結構圖 
![image](./img/power_supply_system.png) 

### 中文
- 在車輛移動的過程中，持續供應電力是必要的，特別是驅動直流馬達所需的12V電源。為了滿足這個需求，我們有兩種電池選擇：鋰離子電池（18650）和鋰聚合電池（3S），因為考慮到車輛的空間問題，而18650電池較占空間並且重量較重，所以我們選擇鋰聚合電池。  
- 為了讓樹梅派正常運作，我們需要將12V電池供應的電壓調整為5V。起初，我們使用了LM2596 DC-DC可調降壓模組，但後來發現它無法提供樹梅派所需的3A電流。因此，我們選擇了一個能夠供應3A電流的恆壓恆流降壓電源模組。為了監控電池的電壓狀態，我們在電池部分加裝一個低電壓警報器確定目前電池電壓在預定的範圍內。
- 為了更好地控制後驅馬達的轉速、方向和運動模式等參數，我們決定加裝一個馬達控制器。起初，我們打算使用L298N馬達驅動模組作為馬達控制器；然而，後來在網上發現了L293D馬達驅動IC，它們具有相同的功能，但體積卻小了好幾倍。考慮到節省空間的因素，我們最終決定使用L293D馬達驅動IC作為我們的馬達控制器。

### English
- During the vehicle's movement, a continuous power supply is essential, especially for providing the 12V power required to drive the DC motors. To meet this requirement, we have two battery options: lithium-ion batteries (18650) and lithium polymer batteries (3S). Considering the space constraints of the vehicle, and the fact that 18650 batteries take up more space and are heavier, we chose the lithium polymer batteries.  
- In order to power the Raspberry Pi properly, we need to adjust the voltage supplied by the 12V battery to 5V. Initially, we used the LM2596 DC-DC adjustable step-down module, but later found that it couldn't provide the required 3A current for the Raspberry Pi. Therefore, we opted for a constant voltage and constant current buck power supply module that can supply 3A of current. To monitor the battery voltage status, we added a low voltage alarm to the battery section to ensure that the battery voltage remains within the predetermined range.  
- In order to better control the rear motor's speed, direction, and motion mode, we decided to install a motor controller. Initially, we planned to use the L298N motor driver module as the motor controller. However, later on, we found the L293D motor driver IC online, which offers the same functionalities but is significantly smaller in size. Considering space-saving considerations, we ultimately decided to use the L293D motor driver IC as our motor controller.

- ### Battery(電池)

<div align="center">
<table>
<tr>
<th>18650電池</th>
<th>鋰聚合物電池 3S</th>
</tr>
<td><img src="./img/18650.png" width="200" hight="500" alt=""></td>
<td><img src="./img/3S.png" width="200" hight="500" alt=""></td>
<tr>
</tr>
</table>
</div>

- ### Step-down_module(降壓模組)

<div align="center">
<table>
<tr>
<th>LM2596 DC-DC可調降壓模組</th>
<th>恆壓恆流降壓電源模組</th>
</tr>
<td><img src="./img/3AStep-down.png" width="200" alt=""></td>
<td><img src="./img/5AStep-down.png" width="200" alt=""></td>
<tr>
</tr>
</table>
</div>


- ### Motor_driver_module(馬達驅動模組)

<div align="center">
<table>
<tr>
<th>L298N馬達驅動模組</th>
<th>L293D馬達驅動IC</th>
</tr>
<td><img src="./img/L298N.png" width="200" alt=""></td>
<td><img src="./img/L293D.png" width="200" alt=""></td>
<tr>
</tr>
</table>
</div>

# <div align="center">![HOME](../../other/img/Home.jpg)[Return Home](../../)</div>  
