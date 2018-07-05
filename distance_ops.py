from haversine import haversine

def harv_distance(a,b):
	return haversine((a[1],a[2]),(b[1],b[2]))


#a,b are [[int float float]]
#(ignoring the first int)
#returns their distance
def computeDTW(a,b):
	m=len(a)
	n=len(b)
	infinity=10000000 #~'northing'
	Matrix=[[0 for x in range(m+1)] for y in range(n+1)] #Matrix[n][m]
	#Matrix[0][0]=0 #first time get as min 0
	for x in range(1,m+1):
		Matrix[0][x]=infinity
	for y in range(1,n+1):
		Matrix[y][0]=infinity

	for x in range(1,m+1):
		for y in range(1,n+1):
			Matrix[y][x] = harv_distance(a[x-1],b[y-1]) + min(Matrix[y-1][x-1],Matrix[y-1][x],Matrix[y][x-1])
	#print Matrix[n][m]
	return Matrix[n][m]

#a: list of points from train
#b= list of points from test
#returns tuple (c,d) where
#	c=matched points
#	d=list of those matching points from test list b
def createLCSS(a,b):
	m=len(a)
	n=len(b)

	Matrix=[[0 for x in range(m+1)] for y in range(n+1)] #Matrix[n][m] init with 0s

	for x in range(1,m+1):
		for y in range(1,n+1):
			if harv_distance(a[x-1],b[y-1]) < 0.2 :
				Matrix[y][x] = Matrix[y-1][x-1] + 1
			else :
				Matrix[y][x] = max(Matrix[y-1][x],Matrix[y][x-1])

	c = Matrix[n][m] #matched points

	#lets backtrack now
	P=n
	Q=m
	d=[]
	while( Matrix[P][Q] != 0 ):
		if Matrix[P-1][Q] >= Matrix[P][Q] :
			P-=1
		elif Matrix[P][Q-1] >= Matrix[P][Q] :
			Q-=1
		else :
			d.append(b[P-1])
			Q-=1
			P-=1
	d = d[::-1]

	return c,d

