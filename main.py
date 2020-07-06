from fcm import FCM
from point import Point

f = open("sample1.csv", "r")
f.readline()
points = []
for line in f:
    pointLine = line.replace("\n","").split(",")
    value = []
    point = Point()
    for val in pointLine:
        value.append(float(val))
    point.setValue(value)
    points.append(point)

fcm = FCM(points, m=2, minCluster=2, maxCluster=10)
fcm.run()
