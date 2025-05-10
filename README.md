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

**Payload Following Robot:**

Notes: 
Files can be found here:
https://drive.google.com/drive/folders/1Vo1qeorxsYMVxnXhXnE2a8wL8P62O5aA?usp=drive_link
For a full report of the project’s outcomes, see https://docs.google.com/document/d/1pVnGqZaFaHImLLfK2TlMqjvi3Yw3gaD4BtxjbRaPBE4/edit?usp=sharing

 This robot requires a different chassis that can be printed in PLA on an MK4 Prusa or any printer with a bed of at least 8.5 in. by 5.5 in. This chassis is wider to accommodate wider wheels for more traction and eliminates the default caster wheels. This chassis also operates the robot as a front-wheel differential drive robot, whereas the default is a back-wheel differential drive.
Print this castor wheel attachment that works for this castor wheel. This attachment is mounted to the back of the robot.
Wheels require an insert that is laser cut from 3mm acrylic. Wheels are printed in TPU, Ninjatek Edge and can be printed on a Prusa Mini. A pause in the print is necessary to insert the laser-cut rim. Dimensions may need to be adjusted so that the laser-cut insert to press-fit to the motor shaft. 
The case and cup holder can be printed in any TPU filament with no supports. The cup holder is is secured to the case with 4 M4 screws and nuts and the case secures on top of the chassis through the grooves in the railings of the chassis.
Mount the camera with this mount and secure it to the front of the robot in the opening of the case.

**Legged Quadruped Robot:**

Notes: Default XRP motors are not strong enough to support the weight of the robot on the 4 legs. As such, left and right legs move in sync in order to move forward and cannot reliably turn left and right, but inconsistent slipping of the feet leads to uncontrolled turns. Adding grips to the feet of the legs additionally stalls out the motor, preventing the robot from moving. This could be amended by upgrading the motors to a higher torque-rated motor and supplying a higher current. Files can be found here:
https://drive.google.com/drive/folders/1yJFZGq2zCDMP5KQiR4NU5IheTLnmeNLO?usp=drive_link

Print chassis in PLA on an MK4 printer or any printer of this bed or larger.
Print 2 pinion gears and 4 bull gears.
Laser cut 4 bent linkages and 4 short linkages from 3mm acrylic.
Linkages and gears are connected to the chassis via 20 M3 screws and locknuts. 8 10mm M3 screws connect the short link to the bent link together and the bent link to the bull gear with locknuts. 4 16mm M3 screws connect the short link to the chassis railings with locknuts and washers. 4 12mm M3 screws connect the bullgears to the chassis with locknuts.
Add heat-set inserts into the bottom of the chassis at the included holes. Laser cut 4 leg guards. These pieces prevent the legs from buckling while walking. These are attached with 8 12mm M3 screws connected to the chassis.

**Legged Strandbeest Robot**

Part models and assembly instructions are located at https://cad.onshape.com/documents/352898896a80e19afb49d088/w/5fa87e00c7bdca29537ea5c9/e/2008de49ce623d45438a7488?renderMode=0&uiState=681ea85e48ce507f07b78573. All parts are manufacturable using either a laser cutter or a 3D printer. 
For XRP version 1 chassis, a 1-cm hole must be drilled in the chassis between the motor shaft and the outside of the robot. For XRP version 2 chassis, these holes already exist, so the strandbeest linkage can be attached to the chassis without modification.
Assemble the linkage system according to its original Onshape assembly starting from the motor side. The nine parts of each crankshaft should be glued to ensure that they don’t separate. 
Once complete, the strandbeest walking robot can be controlled by exactly the same differential drive code as a normal XRP. The four legs on each side of the robot can be controlled as though they were one of the robot’s wheels. 

**Terrain Navigation Robot**

Part models and assembly instructions are located at https://cad.onshape.com/documents/dbd1454ff3330c0206134982/w/dce826dccf6e6e0ceb912fed/e/1a807cf66c90472402f4d357?renderMode=0&uiState=681ea9952047863eae74fcb4  Chassis parts are 3D printable
Print the new XRP chassis, wheel hubs, and connecting arm to the front wheels. Print the silicone wheel molds.
Use silicone 10 and 30 to create the front and back wheel respectively. Each is made from a two part solution that gets stirred together and put in a pressurized chamber to remove bubbles. Wait for the silicone to cure.
Once assembled, the terrain robot can run on regular XRP motion commands. Try and watch as it navigates over obstacles!

