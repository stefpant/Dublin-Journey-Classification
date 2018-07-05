import numpy as np
import pandas as pd
import time

from operator import itemgetter
from ast import literal_eval
from gmplot import gmplot
from distance_ops import computeDTW,createLCSS


def get_latlon(x):
	lon = [a[1] for a in x]
	lat = [a[2] for a in x]
	return lat,lon

#compute average of lat and lon
def center_latlon(lat,lon):
	avglat=0
	avglon=0
	if len(lat) != 0 :
		avglat = sum(lat)/float(len(lat))
		avglon = sum(lon)/float(len(lon))

	return avglat,avglon


if __name__ =="__main__":

	#read dataset
	trainSet = pd.read_csv(
		'./datasets/train_set.csv',
		converters={"Trajectory": literal_eval})


	testSet1 = pd.read_csv(
		'./datasets/test_set_a1.csv',
		sep = '|',
		converters=dict(Trajectory=literal_eval))

	testSet2 = pd.read_csv(
		'./datasets/test_set_a2.csv',
		sep = '|',
		converters=dict(Trajectory=literal_eval))

	traj = trainSet['Trajectory']
	tid = trainSet['tripId']
	jour = trainSet['journeyPatternId']


	
	#for q2 A1
	for nn,i in enumerate(testSet1.Trajectory):
		start = time.time()
		dists=[]
		
		for en,j in enumerate(trainSet.Trajectory):
			dists.append((en,computeDTW(i,j)))
		
		dists.sort(key=itemgetter(1)) #sort by distance
		if len(dists) > 5 :
			dists = dists[:5]#keep first k neighbors
		
		elapsedtime = int(time.time() - start) #seconds passed
		print "time passed: ",elapsedtime
		
		latitudes, longitudes = get_latlon(i)
		avglat, avglon = center_latlon(latitudes, longitudes)
		gmap = gmplot.GoogleMapPlotter(avglat, avglon, 10)
		gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=2)
		image="query1/map" + str(nn) + "/map.html"
		gmap.draw(image)

		imgs=[image]

		for en,j in enumerate(dists):
			print "id:",j[0],",dist:",j[1],",journ:",jour[j[0]]
			latitudes, longitudes = get_latlon(traj[j[0]])
			avglat, avglon = center_latlon(latitudes, longitudes)
			gmap = gmplot.GoogleMapPlotter(avglat, avglon, 10)
			gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=2)
			image="query1/map" + str(nn) + "/res" + str(en) + ".html"
			imgs.append(image)
			gmap.draw(image)

	

	#for q2 A2 
	for nn,i in enumerate(testSet2.Trajectory):
		start = time.time()
		match=[]

		for en,j in enumerate(trainSet.Trajectory):
			match.append( (en,) + createLCSS(j,i) )

		match.sort(key=itemgetter(1),reverse=True) #sort by matched points
		if len(match) > 5 :
			match = match[:5]#keep first 5 neighbors

		elapsedtime = int(time.time() - start) #seconds passed
		print "time passed: ",elapsedtime

		latitudes, longitudes = get_latlon(i)
		avglat, avglon = center_latlon(latitudes, longitudes)
		gmap = gmplot.GoogleMapPlotter(avglat, avglon, 12)
		gmap.plot(latitudes, longitudes, 'green', edge_width=2)
		image="query2/map" + str(nn) + "/map.html"
		gmap.draw(image)

		imgs=[image]

		for en,j in enumerate(match):
			print j[0],",",j[1],",",jour[j[0]]#j = (id , mp , list(mp)) , where mp=matched points
			latitudes, longitudes = get_latlon(traj[j[0]])
			avglat, avglon = center_latlon(latitudes, longitudes)

			gmap = gmplot.GoogleMapPlotter(avglat, avglon, 10) #center map on train traj
			gmap.plot(latitudes, longitudes, 'green', edge_width=2)

			latitudes, longitudes = get_latlon(j[2]) #from matched points
			gmap.plot(latitudes, longitudes, 'red', edge_width=2)

			image="query2/map" + str(nn) + "/res" + str(en) + ".html"
			imgs.append(image)
			gmap.draw(image)

	#match= list(id,num(matchedpoints),list(matchedpoints))
	





