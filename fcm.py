from math import sqrt, pow, log, inf
from point import Point
from random import random
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


class FCM:

    def __init__(self, points, m, minCluster, maxCluster):
        self.points = points
        self.centers = []
        self.m = m
        self.minCluster = minCluster
        self.maxCluster = maxCluster
        self.c = 2
        self.sensivity = 0.01
        pass

    def setInitialCenters(self):
        self.centers = []
        for i in range(self.c):
            point = Point()
            point.setValue([random() for i in range(len(self.points[0].value))])
            self.centers.append(point)

    def getDistance(self, point1, point2):
        dim = len(point1.value)
        sum = 0
        for i in range(dim):
            sum += pow(point1.value[i]-point2.value[i], 2)
        return sqrt(sum)

    def setNewMembeship(self, clusterIndex, point):
        sum = 0
        for i in range(self.c):
            sum += pow(self.getDistance(point, self.centers[clusterIndex])
                       /self.getDistance(point, self.centers[i]),
                       2/(self.m-1))
        point.setMembership(clusterIndex, 1/sum)

    def setNewCenter(self, clusterIndex):
        points = self.points
        sum1 = np.array([0.0 for i in range(len(points[0].value))])
        sum2 = 0
        for point in points:
            membership = pow(point.membership[clusterIndex], self.m)
            newPoint = np.array([i * membership for i in point.value])
            sum1 = np.add(sum1, newPoint)
            sum2 += membership
        self.centers[clusterIndex].setValue((sum1/sum2).tolist())

    def checkTerminationCondition(self, oldCenters, newCenters):
        allDiffs = []
        for i in range(len(oldCenters)):
            diffs = []
            for j in range(len(oldCenters[0].value)):
                diffs.append(abs(newCenters[i].value[j]-oldCenters[i].value[j]))
            allDiffs.append(max(diffs))
        return max(allDiffs) < self.sensivity

    def getEntropy(self):
        sum = 0
        for i in range(len(self.centers)):
            for point in self.points:
                sum += point.membership[i] * log(point.membership[i])
        entropy = -sum / log(self.c)
        print("C = " + str(self.c) + " -> Entropy is", entropy)
        return entropy

    def getBestAnswer(self, answers):
        minEntropy = inf
        finalAnswer = None
        for answer in answers:
            if minEntropy > answers[answer]["entropy"]:
                minEntropy = answers[answer]["entropy"]
                finalAnswer = answer
        self.c = finalAnswer
        self.centers = answers[finalAnswer]["centers"]

    def fcmAlgorithm(self):
        answers = {}
        for c in range(self.minCluster, self.maxCluster):
            self.c = c
            self.setInitialCenters()
            centers = self.centers
            while True:
                oldCenters = deepcopy(centers)
                for i in range(len(centers)):
                    for point in self.points:
                        self.setNewMembeship(i, point)
                for i in range(len(centers)):
                    self.setNewCenter(i)
                if self.checkTerminationCondition(oldCenters, centers):
                    answers[c] = {"entropy": self.getEntropy(), "centers": centers}
                    break
        self.getBestAnswer(answers)

    def run(self):
        self.fcmAlgorithm()
        for i in range(len(self.centers)):
            print("Cluster Center #" + str(i+1) + " : " + str(self.centers[i]))
        self.plot()

    def getDecisionBoundaries(self, minX, maxX, minY, maxY):
        density = 6
        backpointsX = [(minX + j * (maxX-minX)/density) for j in range(density) for i in range(density)]
        backpointsY = [(minY + i * (maxY-minY)/density) for j in range(density) for i in range(density)]
        backpoints = []
        for backpointX in backpointsX:
            for backpointY in backpointsY:
                backpoint = Point()
                backpoint.value = [backpointX, backpointY]
                for c in range(self.c):
                    self.setNewMembeship(c, backpoint)
                backpoints.append(backpoint)
        return backpoints

    def plot(self):
        points = self.points
        if len(points[0].value) == 2:
            centers = self.centers
            pointsX = []
            pointsY = []
            for point in points:
                pointsX.append(point.value[0])
                pointsY.append(point.value[1])
            centersX = []
            centersY = []
            for center in centers:
                centersX.append(center.value[0])
                centersY.append(center.value[1])
            backpoints = self.getDecisionBoundaries(min(pointsX)-0.05, max(pointsX)+0.05, min(pointsY)-0.2, max(pointsY)+0.2)
            for point in backpoints:
                plt.scatter(point.value[0], point.value[1], color=str(point.bestClusterIndex/self.c), s=400)
            plt.plot(pointsX, pointsY, 'ro')
            plt.plot(centersX, centersY, 'bs')
            plt.show()
