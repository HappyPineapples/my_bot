import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node

def generate_launch_description():

    package_name='my_bot'

    gazebo_params_filename = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'gazebo_params.yaml'
    )

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py'
        )]), launch_arguments={
            'use_sim_time': 'true',
            'use_ros2_control': 'true',
            'use_depth_camera': 'false'
        }.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'),'launch','gazebo.launch.py'
            )]), launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_filename}.items()
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'my_bot'],
        output='screen'
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"]
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"]
    )


    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[diff_drive_spawner],
        )
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_broad_spawner],
        )
    )

    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('my_bot'),'launch', 'joystick.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    return LaunchDescription([
        rsp,
        joystick,
        gazebo,
        spawn_entity,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
    ])