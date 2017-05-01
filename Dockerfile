FROM resin/rpi-raspbian:jessie

RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN apt-get update && apt-get -y install python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake wget unzip

COPY . /ros
WORKDIR /ros/catkin_ws

# Install ROS following instructions here:
# http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi
RUN rosinstall_generator ros_comm --rosdistro kinetic --deps --wet-only --tar > kinetic-ros_comm-wet.rosinstall
RUN wstool init src kinetic-ros_comm-wet.rosinstall
WORKDIR /ros/catkin_ws/external_src
RUN wget http://sourceforge.net/projects/assimp/files/assimp-3.1/assimp-3.1.1_no_test_models.zip/download -O assimp-3.1.1_no_test_models.zip && unzip assimp-3.1.1_no_test_models.zip
WORKDIR /ros/catkin_ws/external_src/assimp-3.1.1
RUN cmake . && make && make install
WORKDIR /ros/catkin_ws
RUN rosdep init && rosdep update
RUN rosdep install -y --from-paths src --ignore-src --rosdistro kinetic -r --os=debian:jessie
RUN ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/kinetic
RUN echo source /opt/ros/kinetic/setup.bash >> ~/.bashrc

CMD sleep infinity
