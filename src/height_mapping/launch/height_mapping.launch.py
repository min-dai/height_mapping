#!/usr/bin/env python3

from launch_ros.actions import Node
from launch import LaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # Include the fast_lio_vel mapping launch file
    fast_lio_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('fast_lio_vel'),
                'launch',
                'mapping.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': 'true'
        }.items()
    )

    # Height mapping node with parameters from YAML file
    config_file = PathJoinSubstitution([
        FindPackageShare('height_mapping'),
        'config',
        'hieght_mapping.yaml'
    ])

    height_mapping_node = Node(
        package='height_mapping',
        executable='height_mapping_node',
        name='height_map_node',  # Must match the node name in YAML file
        parameters=[
            config_file,
            {'use_sim_time': True}  # Override use_sim_time if needed
        ],
        output='screen',
        respawn=True,
        respawn_delay=2.0
    )

    # Log info about what's being launched
    log_info = LogInfo(
        msg="Launching FAST-LIO and Height Mapping pipeline..."
    )

    return LaunchDescription([
        log_info,
        fast_lio_launch,
        height_mapping_node
    ])