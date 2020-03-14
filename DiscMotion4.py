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

discaxistheta=np.pi #measured with respect to anglev (x/y plane)(precession angles)(wind frame)(this is initial theta angle 3/2pi is sloped directly right, )
discaxisphi=5/180*np.pi #measured with respect to anglev (vertical deviation)(precession angles)(wind frame)

angleroll=0 #measures the roll side to side of the disc with respect to the direction of velocity of the disc (aviation angles)(wind frame)
anglepitch=0 #measures the pitch of the disk fore and back with respect to the direction of the velocity of the disc. ***AKA AOA*** (aviation angles)(wind frame)

#other angular stuff
vangular=8 #angular velocity of disc in Hz (body frame)
precession=0 #rate of precession per second. likely in degrees. (wind frame)

#Coefficients
Cl0=0.3
Cla=1.8 #coefficient for use in lift (dependent on aoa)
Cl=0
def getCl (Cl0,Cla,anglepitch,anglevphi):
	Cl=(Cl0+(Cla*(anglepitch+anglevphi-(np.pi/2)))) #constant lift coeff***
	#print(-anglevphi+(np.pi/2))
	return(Cl)
Cd0=0.1
Cda=1.24 #coefficient for use in drag (dependent on aoa)
Cd=0
def getCd (Cd0,Cda,anglepitch,anglevphi): #***
	Cd=(Cd0+(Cda*((anglepitch+anglevphi-(np.pi/2))**2))) #constant drag coeff***
	return(Cd)
Cr=0.01 #constant roll coeff
#***Cra=0 #coefficient for use in roll (dependent on anglephi probably)

# velocities
vx=10
vy=0
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
###########################################################################
counter=0
iterationnumber=5000
residual=10000
while(counter<iterationnumber):
	
	sumresidual=0
	internalcounter=0
	counter=counter+1

	t=0
	dt=0.001

	vx=14.224 #needs changing
	vy=-1.970
	vz=3.727
	n=35
	x=0 # distance in the forward direction
	xarray=[]
	comparex=[0]
	realx=[0.0000,0.9534,1.8456,2.7224,3.5738,4.4048,5.1950,5.9649,6.7194,7.4382,8.2998,9.1308,9.7681,10.3799,10.9712,11.5575,12.1489,12.6740,13.2348,13.7497,14.2646,14.7694,15.2639,15.7278,16.3039,16.8902,17.3388,17.7620,18.1851,18.6083,19.0110,19.4393,19.8369,20.2703,20.7546] #midrange disc

	y=0 # distance side to side
	yarray=[]
	comparey=[0]
	realy=[0.00,-0.13,-0.27,-0.38,-0.50,-0.62,-0.73,-0.85,-0.96,-1.06,-1.19,-1.29,-1.37,-1.46,-1.52,-1.58,-1.64,-1.68,-1.71,-1.73,-1.74,-1.73,-1.68,-1.62,-1.57,-1.48,-1.35,-1.23,-1.07,-0.93,-0.70,-0.51,-0.31,-0.05,0.19]

	z=1.5 # distance up and down
	zarray=[]
	comparez=[0]
	realz=[1.50,1.75,1.94,2.09,2.22,2.33,2.44,2.50,2.56,2.60,2.62,2.65,2.65,2.64,2.60,2.56,2.52,2.46,2.40,2.32,2.24,2.17,2.08,1.98,1.84,1.70,1.56,1.42,1.24,1.05,0.84,0.59,0.31,0.00,-0.42]

	Cl0=random.random()*1.2
	Cla=random.random()*8
	#print(Cla)
	Cd0=random.random()
	Cda=random.random()*4
	Cr=random.random()*0.2
	discaxistheta=random.random()*2*np.pi
	discaxisphi=random.random()*np.pi/9

	while t<(0.066*n+0.1): #main loop needs changing loop for loop
		

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
		######################################
		internalcounter=internalcounter+1
		#print(internalcounter)
		if internalcounter%66==0: #might need changing, probably not
			comparex.append(x)
			comparey.append(y)
			comparez.append(z)
		#########################################
	#print(t)
	#Sets 3d plane
	#print(xarray)
	#fig= plt.figure()
	#axis=plt.axes(projection="3d")
	#plots points on 3d plane using the three arrays from above
	#Remember to add colour changing points to make the graph nicer
	#axis.scatter3D(xarray,yarray,zarray,);
	#plt.show()
	##########################################################
	comparisoncounter=0
	#print(len(realx))
	#print(len(realy))
	#print(len(realz))
	#print(len(comparex))
	#print(len(comparey))
	#print(len(comparez))
	print(counter)
	print(sumresidual)
	while comparisoncounter<n:
		sumresidual=sumresidual+((realx[comparisoncounter]-comparex[comparisoncounter])**2)+((realy[comparisoncounter]-comparey[comparisoncounter])**2)+((realz[comparisoncounter]-comparez[comparisoncounter])**2)
		comparisoncounter=comparisoncounter+1
	print(sumresidual)
	
	if (sumresidual<residual):
		residual=sumresidual
		storeCl0=Cl0
		storeCla=Cla
		storeCd0=Cd0
		storeCda=Cda
		storeCr=Cr
		storetheta=discaxistheta
		storephi=discaxisphi
	print(residual)
print("Cl0",storeCl0)
print("Cla",storeCla)
print("Cd0",storeCd0)
print("Cda",storeCda)
print("Cr",storeCr)
print("thera",storetheta)
print("phi",storephi)
print("Residual",residual)


