------------------------------------------------------------------------------------

This is the shared git repo of Cole Needham and Nicholas Phillips

It contains the important code used in "Plotting the Paths of Platter-like Projectiles", 
a Term 2 Project for the Science One program at the
University of British Columbia

The equations used for the model are based of those of Potts & Crowther (2000/2001) and Hubbard & Hummel (2002) 

All code utilizes Python 3. Documentation is poor, but the programs are not complex, and most variable names should be roughly descriptive of their purpose.

There are a few programs in this repo, but there is a large amount of overlap in code between the versions (as expected)
README should contain the purpose of each version

Feel free to contact me with any questions at:

cole.needham01@gmail.com

------------------------------------------------------------------------------------

The programs' uses are as follows:

'DiscMotion.py'
-> Early branch
--> not really worth looking at (doesn't contain any equations, just an euler loop and 3d plotting)

'DiscMotion2.py'
-> First useful piece of code
--> Takes input of environmental conditions, disc parameters, and initial conditions
---> Simulates the flight of a disc until it hits the ground (z=0)

'DiscMotion3.py'
->Very similar to DiscMotion2
--> takes real positional data (array form)
---> generates 3d plots of simulation against real data

'DiscMotion4.py'
-> The big boy
--> Very messy, contains a lot of artifacts from debugging (sorry)
---> Takes real positional data in array form, initial velocities, and number of real data points
----> Runs simulated disc with random coefficients against real data, calculating residuals and storing values along the way
-----> Returns final lowest residual and coefficients that resulted in it (generated the data used in the paper)

'README.txt'
-> see 'README.txt'
