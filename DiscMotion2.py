from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

#Disc parameters
d=0.1 #diameter (m)
A=np.pi*d*d/4 #planform area (m^2)
m=0.2 #mass (kg)

#environmental parameters
p=1.225 #air density (kg/m^3)
dt=0.01 #change in time (s)
t=0 #time (s)
g=9.809 #acceleration due to gravity

# positions
x=0 # distance in the forward direction
xarray=[]
y=0 # distance side to side
yarray=[]
z=1.5 # distance up and down
zarray=[]

#angles (all in radians)
anglevtheta=0 #angle of velocity around x/y plane (earth frame)
anglevphi=0 #elevation angle of velocity (deviation up from horizontal) (earth frame)

discaxistheta=0 #measured with respect to anglev (x/y plane)(precession angles)(wind frame)
discaxisphi=5/180*np.pi #measured with respect to anglev (vertical deviation)(precession angles)(wind frame)

angleroll=0 #measures the roll side to side of the disc with respect to the direction of velocity of the disc (aviation angles)(wind frame)
anglepitch=0 #measures the pitch of the disk fore and back with respect to the direction of the velocity of the disc. ***AKA AOA*** (aviation angles)(wind frame)

#other angular stuff
vangular= #angular velocity of disc in rad/sec (body frame)
precession=0 #rate of precession per second. likely in degrees. (wind frame)

#Coefficients
Cl0=0.2
Cla=1.89 #coefficient for use in lift (dependent on aoa)
Cl=0
def getCl (Cl0,Cla,anglepitch):
	Cl=(Cl0+(Cla*anglepitch)) #constant lift coeff
	return(Cl)
Cd0=0.83
Cda=0.83 #coefficient for use in drag (dependent on aoa)
Cd=0
def getCd (Cd0,Cda,anglepitch):
	Cd=(Cd0+(Cda*anglepitch*anglepitch)) #constant drag coeff
	return(Cd)
Cr=0.012 #constant roll coeff
#***Cra=0 #coefficient for use in roll (dependent on anglephi probably**)

# velocities
vx=10
vy=5
vz=0
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
	ax=((Drag*(-np.cos(anglevphi)*np.cos(anglevtheta))+(Liftup*(np.cos(anglevphi)*np.cos(anglevtheta))))+(Liftside*(np.sin(anglevtheta))))/m
	return(ax)
def getyAcceleration (Drag,anglevtheta,anglevphi,Liftup,Liftside,m):
	ay=((Drag*(-np.cos(anglevphi)*np.sin(anglevtheta)))+(Liftup*(-np.cos(anglevphi)*np.sin(anglevtheta)))+(Liftside*(np.cos(anglevtheta))))/m
	return(ay)
def getzAcceleration (Drag,anglevphi,Liftup,Grav,m):
	az=((Drag*(-np.cos(anglevphi)))+(Liftup*(np.sin(anglevphi)))-(Grav))/m
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
	return (Lift)
def getLiftup(Lift,angleroll,Liftup):
	Liftup=Lift*(np.cos(angleroll))
	return (Liftup)
def getLiftside(Lift,angleroll,Liftside):
	Liftside=Lift*(np.sin(angleroll))
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
	anglepitch=(np.pi/2)-(np.arctan(np.cos(discaxistheta)*np.tan(discaxisphi)))
	return(anglepitch)
def getAngleRoll (discaxistheta,discaxisphi,angleroll):
	angleroll=(np.pi/2)-(np.arctan(np.sin(discaxistheta)*np.tan(discaxisphi)))
	return(angleroll)
def getAngleVelocityTheta (vx,vy):
	anglevtheta=(np.arctan(vy/vx))
	return(anglevtheta)
def getAngleVelocityPhi (vz,vmag):
	anglevphi=(np.arccos(vz/vmag))
	return(anglevphi)

while z>0: #main loop
	vmag=(getVelocityMagnitude (vx,vy,vz)) #update magnitude of velocity
	anglevtheta=(getAngleVelocityTheta (vx,vy))
	anglevphi=(getAngleVelocityPhi (vz,vmag))
	precession=(getPrecession(p,vmag,A,Cr,m,d,vangular)) #update precession rate
	discaxistheta=(getPolarTheta (discaxistheta,precession)) #update angle of precession of disc
	anglepitch=(getAnglePitch (discaxistheta,discaxisphi,anglepitch))
	angleroll=(getAngleRoll (discaxistheta,discaxisphi,angleroll))
	Cd=getCd(Cd0,Cda,anglepitch)
	Cl=getCl(Cl0,Cla,anglepitch)

	Drag=getDrag (Cd,A,p,vmag)
	Grav=getGravity (g,m)
	Lift=getLift (Cl,A,p,vmag)
	Liftup=getLiftup(Lift,angleroll,Liftup)
	Liftside=getLiftside(Lift,angleroll,Liftside)

	ax=getxAcceleration (Drag,anglevphi,anglevtheta,Liftup,Liftside,m)
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

#Sets 3d plane
fig= plt.figure()
axis=plt.axes(projection="3d")
#plots points on 3d plane using the three arrays from above
#Remember to add colour changing points to make the graph nicer
axis.scatter3D(xarray,yarray,zarray,);
plt.show()

