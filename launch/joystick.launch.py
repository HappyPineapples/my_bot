import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    joy_params = os.path.join(get_package_share_directory('my_bot'),'config','joystick.yaml')

    twist_mux_params_filename = os.path.join(
        get_package_share_directory('my_bot'),
        'config',
        'twist_mux.yaml'
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[joy_params]
    )

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_node',
        parameters=[joy_params],
        remappings=[('/cmd_vel','/cmd_vel_joy')]
    )

    twist_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        parameters=[twist_mux_params_filename],
        remappings=[('cmd_vel_out', 'diff_cont/cmd_vel_unstamped')]
    )


    # Launch!
    return LaunchDescription([
        joy_node,
        teleop_node,
        twist_mux
    ])
