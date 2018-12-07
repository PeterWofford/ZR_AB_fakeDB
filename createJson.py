import pandas as pd
import numpy as np
import json as json

class jsonObject:
	


	"""
	dF = 7
	
	dF[0][t] = total score
	dF[1][t] = fuel remaining / 60.0
	dF[5-7][t] = user forces :: [5] = x-direction force, [6] = y-direction force, [7] = z-direction force
	



	#dS = 15

	dS[0-2][t] = item 0 location :: [0] = x*10000, [1] = y*10000, [2] = z * 10000
	dS[3-5][t] = item 1 location :: [3] = x*10000, [4] = y*10000, [5] = z * 10000
	dS[6-8][t] = item 2 location :: [6] = x*10000, [7] = y*10000, [8] = z * 10000
	dS[9-11][t] = item 3 location :: [9] = x*10000, [10] = y*10000, [11] = z * 10000
	dS[12][t] = the real time at which the event happened in the game (0 <= real time < 188)
	dS[13][t] = 0 if item should remain stationary after dropped (usually when dropped in zone); 1 if item can drift upon being dropped
	dS[14][t] = -32766 (special packed identifier)
	
	#dU = 15

	******example json goes up to 14, doc says only up to 10???????
	
	dU[0][t] = ID of new object held
	dU[1][t] = ID of last object held
	dU[2][t] = SPS dropped (in this time step)
	dU[3][t] = error radius * 10000
	dU[4-6][t] = estimated zone location (calculated from SPS locations) :: [4] = x*10000, [5] = y*10000, [6] = z*10000
	dU[7][t] = number of SPS held
	dU[8][t] = points per sec * 100
	dU[9][t] = message
	dU[10][t] = hasReceiver :: 0 if no adapters held, 7 if item 7 held, 8 if item 8 held, 15 if both held*/


	#dUser 7

	#st = 13

	"""
	


	def __init__(self,codgen_ver,simulationId,standalone_ver):
		self.codgen_ver =codgen_ver
		self.simulationId = simulationId
		self.standalone_ver = standalone_ver
		self.results = []
		self.satData =[{ "dF":[[],[],[],[],[],[],[],[]],"dS":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"dU":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"dUser":[[],[],[],[],[],[],[],[]],"st":[[],[],[],[],[],[],[],[],[],[],[],[],[]],'txt':[]},{ "dF":[[],[],[],[],[],[],[],[]],"dS":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"dU":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"dUser":[[],[],[],[],[],[],[],[]],"st":[[],[],[],[],[],[],[],[],[],[],[],[],[]],'txt':[]},{ "dF":[[],[],[],[],[],[],[],[]],"dS":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"dU":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"dUser":[[],[],[],[],[],[],[],[]],"st":[[],[],[],[],[],[],[],[],[],[],[],[],[]],'txt':[]}]
		self.tDbg =[]
		self.tSt =[]
		self.tTxt =[]


	def addResults(self, zero, one):
		self.results = [zero,one]



	"""
	insert a row of 
	item- which item (Astrobee or rings) Astrobee = 0, ring = 1
	0 (x pos)
	1 (y pos)
	2 (z pos)
	3 (vx force)
	4 (vy force)
	5 (vz force)
	6 (x orientation)
	7 (y orientation)
	8 (z orientation)
	9 (w orientation)
	10 (x angular velocity)
	11 (y angular velocity)
	12 (z angular velocity)
	repeat time is how many times should this data be entered to keep the timing even
		ex. rings only report 1 time for astrobees 6 so for a ring you would insert 6
	variable - which spot would you like to add it to, default is 'st' satelite movement data
	multiplier - should the values be un changed or scaled by a certain nummber?
	"""
	def insertData(self,item,x,y,z,vx,vy,vz,q1,q2,q3,q4,avx,avy,avz,repeatTimes = 1,variable='st',multiplier = 1):
		for i in range(repeatTimes):
			self.satData[item][variable][0].append(x*multiplier)
			self.satData[item][variable][1].append(y*multiplier)
			self.satData[item][variable][2].append(z*multiplier)
			self.satData[item][variable][3].append(vx*multiplier)
			self.satData[item][variable][4].append(vy*multiplier)
			self.satData[item][variable][5].append(vz*multiplier)
			self.satData[item][variable][6].append(q1*multiplier)
			self.satData[item][variable][7].append(q2*multiplier)
			self.satData[item][variable][8].append(q3*multiplier)
			self.satData[item][variable][9].append(q4*multiplier)
			self.satData[item][variable][10].append(avx*multiplier)
			self.satData[item][variable][11].append(avy*multiplier)
			self.satData[item][variable][12].append(avz*multiplier)



	"""
	populate the time of the simulation in steps of 0.2

	"""

	def populateTime(self,upperBound):
		for i in range(upperBound*5.0):
			self.tSt.append(i/5.0)




def readInCSVs():
	ourJson = jsonObject("codgen_ver","simulationId","standalone_ver")
	ab_pose = pd.read_csv("pose.csv")
	ab_twist = pd.read_csv("twist.csv")
	ring1 = pd.read_csv("ring1.csv")
	ring2 = pd.read_csv("ring2.csv")
	ab_pose_asArray = np.array(ab_pose)
	ab_twist_asArray = np.array(ab_twist)
	# ring1_asArray = ring1.iterrows()
	# ring2_asArray = ring2.iterrows()


	#inser astrobee information
	for i in range(len(ab_twist_asArray)):
		x=float(ab_pose_asArray[i][4])
		y=float(ab_pose_asArray[i][5])
		z=float(ab_pose_asArray[i][6])
		vx=float(ab_twist_asArray[i][4])
		vy=float(ab_twist_asArray[i][5])
		vz=float(ab_twist_asArray[i][6])
		q1=float(ab_pose_asArray[i][7])
		q2=float(ab_pose_asArray[i][8])
		q3=float(ab_pose_asArray[i][9])
		q4=float(ab_pose_asArray[i][10])
		avx=float(ab_twist_asArray[i][7])
		avy=float(ab_twist_asArray[i][8])
		avz=float(ab_twist_asArray[i][9])
		ourJson.insertData(0,x,y,z,vx,vy,vz,q1,q2,q3,q4,avx,avy,avz)

	#insert ring1 information
	for i in ring1.iterrows():

		x= i[1]["field.pose.position.x"]
		y= i[1]["field.pose.position.y"]
		z= i[1]["field.pose.position.z"]
		vx=0.0
		vy=0.0
		vz=0.0
		q1=i[1]["field.pose.orientation.x"]
		q2=i[1]["field.pose.orientation.y"]
		q3=i[1]["field.pose.orientation.z"]
		q4=i[1]["field.pose.orientation.w"]
		avx=0.0
		avy=0.0
		avz=0.0
		ourJson.insertData(1,x,y,z,vx,vy,vz,q1,q2,q3,q4,avx,avy,avz)

	for i in ring2.iterrows():

		x= i[1]["field.pose.position.x"]
		y= i[1]["field.pose.position.y"]
		z= i[1]["field.pose.position.z"]
		vx=0.0
		vy=0.0
		vz=0.0
		q1=i[1]["field.pose.orientation.x"]
		q2=i[1]["field.pose.orientation.y"]
		q3=i[1]["field.pose.orientation.z"]
		q4=i[1]["field.pose.orientation.w"]
		avx=0.0
		avy=0.0
		avz=0.0
		ourJson.insertData(2,x,y,z,vx,vy,vz,q1,q2,q3,q4,avx,avy,avz,6)
	

	#create the json text and write to new file
	jsonObj = json.dumps(ourJson.__dict__)
	file = open("json.txt","w") 
	file.write(jsonObj) 

	
readInCSVs()





