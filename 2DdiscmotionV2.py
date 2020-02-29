import numpy as np
import matplotlib.pyplot as plt

#This is all horribly commented because it is a proof-of-concept program, rather than something fully functional

dt= 0.1
t=0
p= 1.225
A=np.pi*0.15*0.15
m=0.2
g=9.809

cl0= 0.188
cla= 2.37
cl=0

cd0= 0.15
cda= 1.24
cd=0

Vx= 20
Vy= 0

ax=0
ay=0

aoa=5/180*np.pi
anglev=0

arrayx=[0]
arrayy=[1.5]
x=0
y=1.5

def getAngleofAttack(aoa,Vx,Vy):

	
def getAnglev(Vx,Vy):
	anglev=np.arctan(Vy/Vx)
	return(anglev)

def getCl(cl0,cla,cl):
	cl=cl0+cla*aoa
	return(cl)

def getCd(cd0,cda,cd):
	cd=cd0+cda*aoa
	return(cd)

def getForces(Vx,cl,cd,A,p,anglev,m):
	Fg=m*g
	Fl=(cl*A*p*(Vx*Vx+Vy*Vy))/2
	Fd=(cd*A*p*(Vx*Vx+Vy*Vy))/2
	Fx=-Fd*np.cos(anglev)-Fl*np.sin(anglev)
	Fy=Fl*np.cos(anglev)-Fd*np.sin(anglev)-Fg
	ax=Fx/m
	ay=Fy/m
	return(ax,ay)

def getVelocities(ax,ay,Vx,Vy):
	Vx=Vx+ax*dt
	Vy=Vy+ay*dt
	return(Vx,Vy)

def getPosition(Vx,Vy,x,y):
	x=x+Vx*dt
	y=y+Vy*dt
	return(x,y)


while y>0:
	anglev=getAnglev(Vx,Vy)
	cl=getCl(cl0,cla,cl)
	cd=getCd(cd0,cda,cd)

	ax=getForces(Vx,cl,cd,A,p,anglev,m)[0]
	ay=getForces(Vx,cl,cd,A,p,anglev,m)[1]

	Vx=getVelocities(ax,ay,Vx,Vy)[0]
	Vy=getVelocities(ax,ay,Vx,Vy)[1]

	x=getPosition(Vx,Vy,x,y)[0]
	arrayx.append(x)
	y=getPosition(Vx,Vy,x,y)[1]
	arrayy.append(y)
	t=t+dt
print (arrayy)
print (x)
print(t)

fig=plt.figure()
axis=plt.axes()
axis.scatter(arrayx,arrayy);
plt.show()

#print(getAnglev(Vx,Vy))

