------------------------------------------------------------------------------------

This is the shared git repo of Cole Needham and Nicholas Phillips

It contains (most) of the code used in "Plotting the Paths of Platter-like Projectiles", 
a Term 2 Project for the Science One program at the
University of British Columbia

The equations used for the model are based of those of Potts & Crowther (2000/2001) and Hubbard & Hummel (2002) 

All code utilizes Python 3

There are a few programs in this repo, but only like 2 of them are important in any way (sorry to disappoint)

Feel free to contact me with any questions at:

cole.needham01@gmail.com

------------------------------------------------------------------------------------

The programs' uses are as follows:

'2DdiscmotionV2.py'
-> An early testing branch for the Euler loop as well as lift and drag forces
--> NOT WORTH LOOKING AT, it's only there because it's not hurting anyone

'DataPlotting.py'
-> Another early branch for testing 3 dimensional plotting
--> also not worth looking at, but it's not hurting anyone by being there, is it?

'DiscMotion.py'
-> Early branch
--> not worth looking at (doesn't contain any equations, just an euler loop and 3d plotting)

'DiscMotion2.py'
-> First useful piece of code
--> Takes input of environmental conditions, disc parameters, and initial conditions
---> Simulates the flight of a disc until it hits the ground (z=0)

'DiscMotion3.py'
->Very similar to DiscMotion2
--> also takes real positional data (array form)
---> plots simulation against real data

'DiscMotion4.py'
-> The big boy
--> Very messy, contains a lot of artifacts from debugging (sorry)
---> Takes real positional data in array form, initial velocities, and number of real data points
----> Runs simulated disc with random coefficients against real data, calculating residuals and storing values along the way
-----> Returns final lowest residual and coefficients that resulted in it

'README.txt'
-> see 'README.txt'
