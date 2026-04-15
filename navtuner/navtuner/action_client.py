#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped

class Nav2GoalSender(Node):
    def __init__(self):
        super().__init__('nav2_goal_sender')
        # Create the action client that talks to the Nav2 server
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y, w):
        goal_msg = NavigateToPose.Goal()
        
        # Construct the target pose (where we want the rover to go)
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.orientation.w = float(w) 
        
        goal_msg.pose = pose

        self.get_logger().info('Waiting for Nav2 action server...')
        self._action_client.wait_for_server()

        self.get_logger().info(f'Sending goal: X={x}, Y={y}')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Nav2 rejected the goal. Is it inside a wall?')
            return

        self.get_logger().info('Nav2 accepted the goal. Navigating...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Navigation completed! Rover has arrived.')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = Nav2GoalSender()
    
    # Coordinates for the rover to drive to. 
    # NOTE: (2.0, 0.0) is usually a safe bet in the default Waffle house map!
    action_client.send_goal(x=2.0, y=0.0, w=1.0)
    
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()