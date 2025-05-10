# adv-robotics

Repository for H.O.N.K final project

Contributors
- Hannah Loly
- Joanna Turner
- Juliette Kilgore
- Nezy Jose
- Aengus Kennedy

huskylensPythonLibrary.py is the library needed for the camera

track_person.py tracks a person or object using proportional control 

**Final Report**

**Problem**

The motivation for this project was to create a robot that could follow a person while carrying their muffin on different terrains. This idea was created because it is often the case that people have too many things to carry at one point in time. Having a robot that could ease the load and carry small food items like muffins is beneficial to an average person, especially students and the elderly. Similar to service animals, this robot also has the potential to act as a second eye to follow and assist a user in day-to-day tasks. 

**Approach**

To solve the problem presented above, and to explore it further it was necessary to divide the project into two sub-projects with different goals. One goal was to program one robot to follow a person by implementing PID control and color recognition with the integration of the MQTT server to display the camera tracking results so that the person walking and all other teammates can see the robot’s performance. The next sub-section of the project involved designing multiple designs of the XRP robot to tackle different terrains that a person would come across on foot, such as different textured floors and curbs. These terrains were considered with a generic unupgraded XRP robot with improved traction, a quadruped walking robot, a squishy-wheeled terrain navigation robot, and a octoped robot that walked using the strandbeest linkage.


**Joanna**: To go forward with the basic goal of carrying the muffin, I would have designed the cupholder in Onshape, but the base of this holder was completed by Nezy. Nezy and I worked together to come up with a suitable design for the cupholder for the generic robot.

I also worked on the MQTT aspect for the generic robot. This MQTT code was added to the basic robot tracking code so that the results from the color recognition on the camera could be viewed in real time while also outputting the last 10 results from the color tracking. The purpose of implementing this is so that other teammates and the person being followed by the robot could see if the robot is taking the correct action based on the camera readings. While Hannah wrote the base code for the robot's following behavior I would have assisted in modifications to this code and the fine-tuning necessary to improve this following behaviour of the robot. I have attached a screenshot of the MQTT server which shows the results from the camera readings.



Hannah and I tried a number of different methods for following the person including object recognition, april tag recognition and when none of those worked, I suggested color recognition and that seemed to be the most promising of the three. When implementing the robot tracking we noticed that when the color was at the right corner of the screen it seemed to turn left. I figured out that the camera was warping in that the readings of the x values increased from left to right up until a point on the right side of the screen where they seem to significantly drop to values in the range of 1 to 50. I initially wrote a modified code to try and fix it but when that didn’t work Hannah and I worked together to figure out how to solve this. When this issue was solved we tested this new code and the robot behaved in the behaviour we expected where when the person turned right the robot would follow suit even if the color was on the corner of the right side of the screen. Hannah built on this code to include a state transition and finally the robot did what we initially wanted. 

**Juliette**: The goal for the terrain navigation robot was to create a wheeled mechanism that could climb over obstacles and complex terrain. I thought it would be interesting to explore different wheel materials to see what would work better. I thought that a squishy wheel would be able to mold to its environment and help the robot gain grip when climbing steep surfaces. I began with a TPU print but soon found that it wasn’t very flexible and I needed a significant amount of force to deform the wheel. I tried moving to silicon with pellet printing and found that it was much more successful, but wanted to see if something even more flexible would work better, so I moved to working with silicone molds. I worked with Yija to cast two different hardnesses of the silicone and found that these molds had more consistent flexibility throughout the wheel (the printed ones weren’t consistent because of perimeters and infill) and gave the wheels the traction they needed. I also modified the chassis to be in a triangle shape so that the chassis wouldn’t get stuck when climbing. This proved to be the optimal approach and it was able to navigate a terrain of 2x4s. 

**Hannah**: I started by working on object tracking and developing proof of concept for our project. The robot performed very well on a tabletop and followed without many problems. I tuned the base velocity to improve its following capabilities at a walking pace. Once a base code was established, I started testing with Joanna, and we developed the final code together. Testing with a person to follow proved quite difficult. It was awkward to get a view of the camera without laying on the ground, so Joanna had the idea to post our results to the MQTT server and she wrote the code to do this. We struggled with using the camera object tracking for quite some time. Despite having a clear view of the object, the camera was typically unable to identify our indicator. Without an object to track, we felt we needed to change our approach. We attempted tracking an April Tag, but the camera would not identify a printed tag to train. We landed on color tracking as our final approach, which yielded more consistent identification. One downside of color tracking was that the sides of the camera screen (far right and far left) resulted in the same position readout and would cause the robot to turn left. To counteract this, Joanna initially wrote a modified code that handled “wraparound detection” which we fine-tuned to ensure correct turning. As a group, we had some concerns about the walking robots’ ability to turn and keep up with a person. I implemented two stages for the robot, a 5 second walking demonstration, followed by person tracking until the user button is depressed. The tracking section of the code uses camera position to determine what action the robot should take (wait, move forward, turn, etc). 

**Aengus**: For one of the walking/legged modifications to the XRP robot, I wanted to use the strandbeest linkage to create attachments of four legs each that could replace each wheel of the XRP, and I wanted to use the existing XRP side mounting rails to make legs that could be added onto the XRP with minimal modification to the existing chassis. To achieve this, I removed my XRP’s wheels and drilled two holes in the chassis so that a 3D printed part could extend the motors’ shaft to the exterior of the frame. This shaft joins a laser cut frame containing the entire moving linkage, all secured to the chassis using the XRP’s side mount rails. 
The result is a walking robot that can be controlled in the same way as a differential drive robot, with four legs on each side of the robot that can steer depending on which side’s legs are cycling faster. The linkage is designed for a smooth walking pattern, so the chassis of the XRP remains almost completely flat as the mechanism walks, which supports the goal of carrying a payload. With a camera attached, the strandbeest XRP can track the pink target using the same code that the wheeled XRP uses (see strandbeest_following.mp4 below).

**Nezy**: I developed the generally improved XRP robot to start with and easily integrate the default XRP design and functionality. I made wheels out of TPU and a laser-cut insert to press fit into the motor shaft. I designed the wheels to be grippier with TPU and have a ribbed texture in order to help the robot with traction over non-smooth terrain. I also made these wheels wider to give it more surface area to help with traction. In order to accommodate the wider wheels I had to widen the whole chassis to make room, and this involved redesigning and reprinting the whole chassis. We also wanted to replace the ball castors since the design of them caused debris to collect in the cavity and prevent spinning. We ordered a new caster wheel, and I designed an attachment piece that connects the new caster to the chassis. 


To try and tackle more terrains, such as bumps, I also developed the quadruped walking robot. I decided to redesign the whole chassis to integrate a 4-bar linkage walking design. I incorporated a gear train in order to drive two legs on one side of the robot with just one motor. This also helped in ensuring a 180-degree offset between legs and helps with its motion. After assembly, I ran into a few issues with motors stalling and linkages giving out. Since the original design of the linkages is based on 3D printed soft joints, it is less compliant compared to my laser-cut pin joints. To address this, I ended up adding rubber bands and leg guards at the bottom of the chassis to help restrain the motion to the defined continuous motion. The main issue with this design mostly had to do with the motor stalling. 

I also developed TPU shoes in order to help the robot with traction, but when I implemented this, the feet would get stuck to the floor, and the motor was not strong enough to move the legs and would stall out. Without the feet the legs would slip, and though the robot would still move forward, it was very uncontrolled. Finding a balance between traction and motor stalling would require some more time. Additionally, due to the motor stalling, the robot needs 2 feet level on the ground in order to move, which leads to the robot only moving in a gallop, whereas my intent was for it to move in a trot, where the left and right legs are offset. This ended up working fine since the gallop trot is typically faster.


**Results**

Initial Project Proposal: https://docs.google.com/document/d/1EBQ_19-cI4nVA9oXWnj0M3b3HF9xziEswdf9Fsvx6aE/edit?usp=drive_link
Coding Base Goal: Following a person using the camera.  https://vimeo.com/1083012195?share=copy#t=0 
Integration Stretch Goal: Following in outside conditions with coffee cup, rain and bumpy terrain. https://vimeo.com/1083012225?share=copy#t=0 
Terrain robot in action:
Obstacles:https://drive.google.com/file/d/16G9k_CZcR__kkqiWQWWemayhPQpzKglc/view?usp=sharing 
Height:https://drive.google.com/file/d/16J9QbW-kvHHMqweEa2FWGfuadg-LfbSL/view?usp=sharing 
 Quadruped walking: https://drive.google.com/file/d/16133N4jzVZEb_t7oZy47utP0TBd9irHQ/view?usp=drive_link
Strandbeest walking: https://drive.google.com/file/d/1eoKmq0rgagFSSXSfYNL1REPwemu0Kf8j/view?usp=drive_link
Strandbeest following:
https://drive.google.com/file/d/1V6RHlMUmlsBHP4uFBQysgwOAJJGCKJP3/view?usp=drive_link
**Impact**

This project has potential impact for everyday people and for the disabled. The ability to have a robot carry a payload behind someone can be further explored and expanded upon for a wide range of applications. The following aspect of this project over a variety of terrain also has a wide range of potential for monitoring and tracking. This could be useful in contexts where service animals may be used, for example for guide dogs, mobility assistance, seizure detection, and medication reminders. The robot in itself is very affordable, and we can see this being marketed commercially due to its affordability and scalability. Additionally, the adaptability and modular design of the XRP robor enables it to be helpful in a wide range of unique scenarios and tasks by adding additional sensors possibly for allergy detection, or by adding different camera functionality to assist the vision impaired.
