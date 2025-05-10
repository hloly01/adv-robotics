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

**Replication Instructions**

**Code**

To replicate the tracking part of this project, the necessary materials are a robot capable of walking and turning at speeds up to 1 m/s and a camera. For this project, we used a HuskyLens camera capable of object and color tracking, though any camera compatible with a microprocessor could be used. The HuskyLens handled the object/color tracking for us, which significantly simplified the code. Once the camera can sucessfully identify the person, main.py (or a similar approach) could be used to replicate our project. It is worth noting that we used an MQTT server to track our results, but if the robot fails to connect it will skip any publish commands. 
