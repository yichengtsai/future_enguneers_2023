# <div align="center">ROS of Introduction(ROS系統介紹)</div> 
## 中文介紹

- ROS（機器人操作系統）是一個開源的機器人軟件平台，旨在為機器人開發提供一套靈活、模組化和可重用的工具和庫。ROS最初由Willow Garage公司於2007年發起開發，並在後來得到了廣泛的社區支持和貢獻。它是一個分佈式系統，允許機器人的不同組件在計算機網絡上相互通信，以實現高度協調的控制和感知。  
- ROS提供了各種功能和工具，包括硬件抽象層、設備驅動程序、通信中間件、包管理系統、3D可視化和仿真工具等。它支持多種編程語言，如C++和Python，使開發人員能夠根據自己的喜好和需求編寫機器人應用程序。
- ROS的設計理念是開放性和共享性，許多研究機構、工業界和個人都在其基礎上進行開發和應用。ROS的龐大社區提供了大量的教程、文檔和支援資源，幫助用戶學習和使用ROS，推動機器人技術的發展和創新。

## English introduction

- ROS (Robot Operating System) is an open-source robotic software platform designed to provide a flexible, modular, and reusable set of tools and libraries for robot development. ROS was originally initiated by Willow Garage in 2007 and has since gained extensive community support and contributions. It is a distributed system that allows different components of a robot to communicate with each other over a computer network, enabling highly coordinated control and perception.
- ROS offers various functionalities and tools, including hardware abstraction, device drivers, communication middleware, package management system, 3D visualization, and simulation tools, among others. It supports multiple programming languages such as C++ and Python, enabling developers to write robot applications based on their preferences and needs.
- The design philosophy of ROS is openness and sharing, and many research institutions, industries, and individuals are developing and applying it. The large ROS community provides numerous tutorials, documentation, and support resources to help users learn and utilize ROS, driving the advancement and innovation of robotics technology.

## Installation steps(安裝步驟)
### 中文
1.設置 ROS Noetic 存儲庫  
運行此 echo 命令將官方 ROS Noetic 存儲庫添加到源列表中：
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu buster main" > /etc/apt/sources.list.d/ros-noetic.list'
```
2.添加官方ROS密鑰  
為了確保我們將安裝經過身份驗證的 ROS 包以在您的 Raspberry Pi 4 上編譯 Noetic 並避免黑客攔截您的網絡流量，請運行
``````
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
``````
3.安裝構建依賴項以在 Raspberry Pi 4 上編譯 ROS Noetic 包  
運行以下 2 個命令：  
``````
sudo apt update  
sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake  
``````
4.下載 ROS Noetic 依賴源/存儲庫  
``````
sudo rosdep init && rosdep update  
mkdir ~/ros_catkin_ws && cd ~/ros_catkin_ws  
rosinstall_generator ros_comm --rosdistro noetic --deps --wet-only --tar > noetic-ros_comm-wet.rosinstall  
wstool init src noetic-ros_comm-wet.rosinstall  
rosdep install -y --from-paths src --ignore-src --rosdistro noetic -r --os=debian:buster  
``````
5.在 Raspberry Pi 4 上編譯 Noetic 包  
運行以下命令，這將需要一段時間：  
```
sudo src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/noetic -j1 -DPYTHON_EXECUTABLE=/usr/bin/python3
```
參考網址: https://varhowto.com/install-ros-noetic-raspberry-pi-4/#5_Steps_to_Install_ROS_Noetic_on_Raspberry_Pi_4

### English
1.Setting up ROS Noetic repository
Run the following echo command to add the official ROS Noetic repository to the source list.
``````
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu buster main" > /etc/apt/sources.list.d/ros-noetic.list'
``````
2.Adding the official ROS key
To ensure that we install authenticated ROS packages and secure your network traffic from potential interception, please run the following command to add the official ROS key for compiling Noetic on your Raspberry Pi 4.
``````
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
``````
3.Install build dependencies to compile ROS Noetic packages on Raspberry Pi 4
Run the following two commands:  
``````
sudo apt update  
sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake  
``````
4.Download ROS Noetic dependencies source/repository.
``````
sudo rosdep init && rosdep update  
mkdir ~/ros_catkin_ws && cd ~/ros_catkin_ws  
rosinstall_generator ros_comm --rosdistro noetic --deps --wet-only --tar > noetic-ros_comm-wet.rosinstall  
wstool init src noetic-ros_comm-wet.rosinstall  
rosdep install -y --from-paths src --ignore-src --rosdistro noetic -r --os=debian:buster  
``````
5.Compile Noetic packages on Raspberry Pi 4
Run the following command, as it will take some time:
``````
sudo src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/noetic -j1 -DPYTHON_EXECUTABLE=/usr/bin/python3
``````
Reference URL: https://varhowto.com/install-ros-noetic-raspberry-pi-4/#5_Steps_to_Install_ROS_Noetic_on_Raspberry_Pi_4


# <div align="center">[Return Home](../../)</div>  
