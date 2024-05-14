import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    package_name = 'my_bot'

    slam_params_filename = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'mapper_params_online_async.yaml'
    )

    # twist_mux_params_filename = os.path.join(
    #     get_package_share_directory(package_name),
    #     'config',
    #     'twist_mux.yaml'
    # )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py'
        )]), launch_arguments={
            'params_file': slam_params_filename,
            'use_sim_time': use_sim_time,
        }.items()
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py'
        )]), launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # twist_mux = Node(
    #     package='twist_mux',
    #     executable='twist_mux',
    #     parameters=[twist_mux_params_filename],
    #     remappings=[('cmd_vel_out', 'diff_cont/cmd_vel_unstamped')]
    # )


    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        slam,
        navigation,
        # twist_mux
    ])
