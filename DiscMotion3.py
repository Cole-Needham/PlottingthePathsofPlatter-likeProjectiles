from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import random

#Disc parameters
d=0.217 #diameter (m)
A=np.pi*d*d/4 #planform area (m^2)
m=0.165 #mass (kg)

#environmental parameters
p=1.225 #air density (kg/m^3)
dt=0.001 #change in time (s)
t=0 #time (s)
g=9.809 #acceleration due to gravity

# positions
x=0 # distance in the forward direction
xarray=[]
xreal=[0.00,0.64,1.32,1.95,2.58,3.16,3.88,4.45,4.98,5.50,5.99,6.46,6.91,7.34,7.76,8.16,8.54,8.92,9.26,9.60,10.01,10.31,10.63,10.93,11.18,11.43,11.67,11.86,12.01,12.17,12.29]
y=0 # distance side to side
yarray=[]
yreal=[0.000,-0.019,-0.016,-0.027,-0.037,-0.037,-0.047,-0.053,-0.058,-0.068,-0.076,-0.088,-0.100,-0.114,-0.130,-0.144,-0.159,-0.177,-0.195,-0.216,-0.236,-0.255,-0.278,-0.297,-0.321,-0.343,-0.369,-0.399,-0.428,-0.460,-0.491]
z=1.5 # distance up and down
zarray=[]
zreal=[1.500778596,1.694447219,1.8704778,2.040669744,2.184038196,2.315542399,2.474147003,2.583413632,2.696371647,2.804309518,2.899432327,2.990600493,3.052135866,3.093951236,3.124581516,3.134631272,3.143358616,3.119087396,3.062651067,2.983128296,2.873823206,2.747329604,2.555346906,2.368935257,2.133707902,1.878662512,1.602961763,1.306896349,0.978493692,0.613360345,0.228025234]
#angles (all in radians)
anglevtheta=0 #angle of velocity around x/y plane (earth frame)
anglevphi=0 #elevation angle of velocity (deviation up from horizontal) (earth frame)

discaxistheta=3.751921 #measured with respect to anglev (x/y plane)(precession angles)(wind frame)(this is initial theta angle 3/2pi is sloped directly right, )
discaxisphi=0.163633 #measured with respect to anglev (vertical deviation)(precession angles)(wind frame)

angleroll=0 #measures the roll side to side of the disc with respect to the direction of velocity of the disc (aviation angles)(wind frame)
anglepitch=0 #measures the pitch of the disk fore and back with respect to the direction of the velocity of the disc. ***AKA AOA*** (aviation angles)(wind frame)

#other angular stuff
vangular= #angular velocity of disc in rad/sec (body frame)
precession=0 #rate of precession per second. likely in degrees. (wind frame)

#Coefficients
Cl0=1.100557
Cla=0.801844 #coefficient for use in lift (dependent on aoa)
Cl=0
def getCl (Cl0,Cla,anglepitch,anglevphi):
	Cl=(Cl0+(Cla*(anglepitch+anglevphi-(np.pi/2)))) #constant lift coeff***
	#print(-anglevphi+(np.pi/2))
	return(Cl)
Cd0=0.313422
Cda=0.828133 #coefficient for use in drag (dependent on aoa)
Cd=0
def getCd (Cd0,Cda,anglepitch,anglevphi): #***
	Cd=(Cd0+(Cda*((anglepitch+anglevphi-(np.pi/2))**2))) #constant drag coeff***
	return(Cd)
Cr=0.0679008 #constant roll coeff
#***Cra=0 #coefficient for use in roll (dependent on anglephi probably)

# velocities
vx=9.57
vy=0
vz=2.61
vmag=0 #magnitude of velocity

#accelerations
ax=0
ay=0
az=0

Grav=0
Lift=0
Liftup=0
Liftside=0
Drag=0

#Accelerations
def getxAcceleration (Drag,anglevphi,anglevtheta,Liftup,Liftside,m):
	ax=((Drag*(-np.sin(anglevphi)*np.cos(anglevtheta))+(Liftup*(-np.cos(anglevphi)*np.cos(anglevtheta))))+(Liftside*(np.sin(anglevtheta))))/m
	#print(Drag*(-np.sin(anglevphi)*np.cos(anglevtheta)))
	#print(Drag)
	return(ax)
def getyAcceleration (Drag,anglevtheta,anglevphi,Liftup,Liftside,m):
	ay=((Drag*(-np.sin(anglevphi)*np.sin(anglevtheta)))+(Liftup*(-np.cos(anglevphi)*np.sin(anglevtheta)))+(Liftside*(np.cos(anglevtheta))))/m
	return(ay)
def getzAcceleration (Drag,anglevphi,Liftup,Grav,m):
	az=((Drag*(-np.cos(anglevphi)))+(Liftup*(np.sin(anglevphi)))-(Grav))/m
	#print(Drag*(-np.cos(anglevphi)))
	#print(Liftup)
	#print("phiv",anglevphi)
	#print("Liftup",Liftup*(np.sin(anglevphi)))
	return(az)

#Velocities
def getxVelocity (ax,vx):
	vx=vx+ax*dt
	return(vx)
def getyVelocity (ay,vy):
	vy=vy+ay*dt
	return(vy)
def getzVelocity (az,vz):
	vz=vz+az*dt
	return(vz)
def getVelocityMagnitude (vx,vy,vz):
	vmag=np.sqrt((vx*vx)+(vy*vy)+(vz*vz)) #velocity magnitude = sqrt(vx^2+vy^2+vz^2)
	return (vmag)

#Positions
def getxPosition (vx,x):
	x=x+vx*dt
	return(x)
def getyPosition (vy,y):
	y=y+vy*dt
	return(y)
def getzPosition (vz,z):
	z=z+vz*dt
	return(z)

#Coefficients
def getCoeffLift (Cl,Cl0,Cla,anglepitch):
	Cl=Cl0+Cla*anglepitch
	#print(Cl)
	return(Cl)
def getCoeffDrag (Cd,Cd0,Cda,anglepitch):
	Cd=Cd0+Cda*anglepitch*anglepitch
	return(Cd)

#Forces
def getGravity (g,m):
	Grav=m*g
	return(Grav)
def getLift (Cl,A,p,vmag):
	Lift=(Cl*A*p*vmag*vmag)/2
	#print('Lift',Lift)
	#print(Cl)
	return (Lift)
def getLiftup(Lift,angleroll,Liftup):
	Liftup=Lift*(np.cos(angleroll))
	return (Liftup)
def getLiftside(Lift,angleroll,Liftside):
	Liftside=Lift*(np.sin(angleroll))
	#print('angleroll',angleroll)
	return(Liftside)
def getDrag (Cd,A,p,vmag):
	Drag=(Cd*A*p*vmag*vmag)/2
	return (Drag)

#AngularChanges
def getPrecession (p,vmag,A,Cra,m,d,vangular):
	precession=(p*vmag*vmag*A*Cra)/(m*d/2*vangular)
	return (precession)
def getPolarTheta (discaxistheta,precession):
	discaxistheta=discaxistheta+precession*dt
	return(discaxistheta)
def getAnglePitch (discaxistheta,discaxisphi,anglepitch):
	anglepitch=(np.arcsin(-np.cos(discaxistheta)*np.tan(discaxisphi)))
	return(anglepitch)
def getAngleRoll (discaxistheta,discaxisphi,angleroll):
	angleroll=(np.arcsin(np.sin(discaxistheta)*np.tan(discaxisphi)))
	return(angleroll)
def getAngleVelocityTheta (vx,vy):
	anglevtheta=(np.arctan(vy/vx))
	return(anglevtheta)
def getAngleVelocityPhi (vz,vmag):
	anglevphi=(np.arccos(vz/vmag))
	return(anglevphi)

while t<2.0: #main loop
		

	##########################################
	vmag=(getVelocityMagnitude (vx,vy,vz)) #update magnitude of velocity
	#print(vmag)
	anglevtheta=(getAngleVelocityTheta (vx,vy))
	#print(anglevtheta)
	anglevphi=(getAngleVelocityPhi (vz,vmag))
	#print(anglevphi)
	precession=(getPrecession(p,vmag,A,Cr,m,d,vangular)) #update precession rate
	discaxistheta=(getPolarTheta (discaxistheta,precession)) #update angle of precession of disc
	anglepitch=(getAnglePitch (discaxistheta,discaxisphi,anglepitch))
	#print(anglepitch)
	angleroll=(getAngleRoll (discaxistheta,discaxisphi,angleroll))
	Cd=getCd(Cd0,Cda,anglepitch,anglevphi) #****
	#print(Cd)
	Cl=getCl(Cl0,Cla,anglepitch,anglevphi) #****
	#print(Cl)
	Drag=getDrag (Cd,A,p,vmag)
	#print(Drag)
	Grav=getGravity (g,m)
	#print(Grav)
	Lift=getLift (Cl,A,p,vmag)
	#print(Lift)
	Liftup=getLiftup(Lift,angleroll,Liftup)
	#print(Liftup)
	Liftside=getLiftside(Lift,angleroll,Liftside)
	#print("side",Liftside)
	ax=getxAcceleration (Drag,anglevphi,anglevtheta,Liftup,Liftside,m)
	#print(ax)
	ay=getyAcceleration (Drag,anglevtheta,anglevphi,Liftup,Liftside,m)
	az=getzAcceleration (Drag,anglevphi,Liftup,Grav,m)	

	vx=getxVelocity (ax,vx)
	vy=getyVelocity (ay,vy)
	vz=getzVelocity (az,vz)
	
	x=getxPosition (vx,x)
	xarray.append(x)
	y=getyPosition (vy,y)
	yarray.append(y)
	z=getzPosition (vz,z)
	zarray.append(z)
	t=t+dt
	
	#print(t)
	#Sets 3d plane
#print(xarray)
fig= plt.figure()
axis=plt.axes(projection="3d")
	#plots points on 3d plane using the three arrays from above
	#Remember to add colour changing points to make the graph nicer
axis.scatter3D(xarray,yarray,zarray,'bo');
axis.scatter3D(xreal,yreal,zreal,'r+')
plt.show()
