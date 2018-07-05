import pandas as pd
from ast import literal_eval
import gmplot


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


if __name__ == "__main__":
	trainSet = pd.read_csv(
		'datasets/train_set.csv',
		converters={"Trajectory":literal_eval}
	)

	trainTraj = trainSet['Trajectory']

	jour_ids=[]

	for en,journ in enumerate(trainSet.journeyPatternId):
		if journ not in jour_ids:
			jour_ids.append(journ)
			print "{",en,",",journ,"}"
			latitudes, longitudes = get_latlon(trainTraj[en])
			avglat, avglon = center_latlon(latitudes, longitudes)
			gmap = gmplot.GoogleMapPlotter(avglat, avglon, 10)
			gmap.plot(latitudes, longitudes, 'green', edge_width=2)
			image="visual_data/jour_" + str(journ) + ".html"
			gmap.draw(image)


		if len(jour_ids) == 5:
			break



