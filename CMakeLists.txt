cmake_minimum_required(VERSION 2.8.3)
project(force_sensor_variense_fse1001)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES v2v_collision_check
#  CATKIN_DEPENDS message_generation rospy
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

