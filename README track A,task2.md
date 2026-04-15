# team_deimos_recruitment_task:)
objective: so our objctive here was to make a 50kg rover drive from its spawn point which is the origin of the map frame, to a differnet point in the map
what did i do?:
so first i need a rover that that i could use , biulding a custom one will take a enormous amount of time and i didnt have that , so i used the turtlebot3 waffle bot.
then i needed a world in which the bot will autonomously navigate ,as a beginner a choose turtlebot3 world,so i exported the turtlebot3 model waffle and launced the gazebo world,and then used the teleop_keyboard node fron the turtlebot3_teleop package , then i drove the bot for an hour for no apparent reason.
then i had to run the cartographer node in rviz which is a SLAM algorithm used for making the map of the world using the lidar on the waffle , so i so run the rviz , set the fixed frame of odom and drove around the map to map it , after mapping i saved the pmg and yaml file in map folder.
nav2 requires you a 2D map of the world for non maplessness navigation , now you can either use slam to form a map or get it from somewhere else , you can even paint one.
so then i made a action_client.py file so that we can set the goal, the final destination for the bot to autonomously navigate the bot to , so for now i set the goal to  x=2.0, y=0.0, w=1.0 as this region has enough space for bot to fit 
then finally i ran the gazebo , the navigation in the rviz and set the 2Dpost estimate as when you boot up the naz2 brain , the rovr doesnt know where (0,0) is ,u you need the 2D pose estimate to tell the rviz that the bot is located here
after doing this a advanced alogrithm called AMCl adaptive monte carlo localizaton wakes up.this algorithm makes a lots a green arrows around the area where we selected the 2d pose estimate and then campares the predicted lidar scan at that spot and the real lidar scan , ensuring that the robot's base_ink remains accurately localized within the map coordinate frame.
in the new ternimal i then ran the action_client file which told the rviz its goal_pose and and the robot then autonomously moves to the set coordinate.
so i to change the parameters as required ny the task i downled the official waffle file and named it nav2_param.yaml in the congif folde. i then set the the required values and changed the robto radius to footprint of 1*8 meters , since the footprint is too large for the turtleworld map , whe  you try to use the navigation now , it will be stuck on nagivating the path as it is too big to fit in thier , so we will require a different world to run the navigation
#####
inflation radius --Any pixel on the map that is further away than this radius from an obstacle is assigned  a zero cost. It is condidered safe any pixel within this radius is given a cost
if a pixel is too close that the robots foorprint would hit the wall , it is given an infinite cost 
cost scaling factor--it helps in calcuation the cost of the pixel inside the inflation radius and outisde the footprint ny the formula  cost=e^-(k*d) where d is the distance from the obstable and k is the cost_scaling_factor.
so for exmple if the cost scaling factor is high , the cost for the pixel inside the inflation radius would be quite low and the cost will drop off very quickly form the footpriint to the inflation radius ,the robot will drive very close to the walls  but it is risky for high-speed robots
if the cost scaling factor is low then the cost will drop very slowly and the robot will try to drive in the middle of the room where the cost is minimum 






