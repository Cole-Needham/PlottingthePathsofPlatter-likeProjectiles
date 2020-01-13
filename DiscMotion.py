#
#Cole and Nick's Term 2 Project- Modelling Disc Motion
#Uses the Euler Method along with initial conditions and
#forces to plot the position of a disk in 3d space over time.
#

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

#timestep
dt=0.2
#initial position of disc (in meters)
x=0
pastx=[0]
y=1
pasty=[1]
z=0
pastz=[0]
#initial velocity of disk
vx=5
vy=1
vz=2
#initial acceleration of disc
ax=0.4
az=0.2

#Forces stuff
"""def xforces ():

def yforces ():

def zforces ():"""

#Euler steps takes acceleration in each cardinal direction and evaluates velocity using it
def xVelocity (vx,ax,dt):
	vx=vx+ax*dt
	return (vx)
def yVelocity (vy,ay,dt):
	vy=vy+ay*dt
	return (vy)
def zVelocity (vz,az,dt):
	vz=vz+az*dt
	return (vz)
#Euler steps takes velocity in each cardinal direction and computes position using it
def xPosition (x,vx,dt):
	x=x+vx*dt
	return (x)
def yPosition (y,vy,dt):
	y=y+vy*dt
	return (y)
def zPosition (z,vz,dt):
	z=z+vz*dt
	return (z)
#Iterates the position many times
def Motion (x,y,z,vx,vy,vz,ax,ay,az,dt):
	while y>0:
		x=xPosition(x,vx,dt)
		y=yPosition(y,vy,dt)
		z=zPosition(z,vz,dt)
		pastx.append(x)
		pasty.append(y)
		pastz.append(z)
		vx=xVelocity(vx,ax,dt)
		vy=yVelocity(vy,ay,dt)
		vz=zVelocity(vz,az,dt)
	return (pastx,pasty,pastz)

#Runs "Motion" and takes output of xyz positions as three separate arrays
final=Motion(x,y,z,vx,vy,vz,ax,ay,az,dt)
xhistory=final[0]
print(xhistory)
yhistory=final[1]
print(yhistory)
zhistory=final[2]
print(zhistory)


#Sets 3d plane
fig= plt.figure()
axis=plt.axes(projection="3d")
#plots points on 3d plane using the three arrays from above
#Remember to add colour changing points to make the graph nicer
axis.scatter3D(xhistory,yhistory,zhistory,);
plt.show()
