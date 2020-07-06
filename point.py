import math

class Point:

    def __init__(self):
        self.value = []
        self.membership = {}
        self.bestMembership = 0
        self.bestClusterIndex = 0

    def setValue(self, value):
        self.value = value

    def setMembership(self, clusterIndex, value):
        self.membership[clusterIndex] = value
        if value > self.bestMembership:
            self.bestClusterIndex = clusterIndex
            self.bestMembership = value

    def __str__(self):
        string = "[ "
        for val in self.value:
            string += str(val) + " "
        return string + " ]"

