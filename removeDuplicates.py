#!/usr/bin/env python

import inkex
from simplepath import parsePath
from lxml import *

def distance(a, b):
    return sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def isInTotalPaths(path, totalPaths, tolerance):
	for totalPath in totalPaths:
        commonPoints = 0
        for (pathPoint, totalPathPoint) in (path, totalPath):
            if distance(pathPoint, totalPathPoint) <= tolerance:
                commonPoints += 1
        if commonPoints >= len(path):
            return True
    return False


class removeDuplicates(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--title")
		self.OptionParser.add_option("-r", "--radius",
						action="store", type="float",
						dest="radius", default=0.0,
						help="Maximum radius (px)")
        self.OptionParser.add_option("-rev", "--reverse",
						action="store", type="bool",
						dest="reverse", default=0.0,
						help="Consider reversed paths as equals")
		self.OptionParser.add_option("--tab",
						action="store", type="string",
						dest="tab",
						help="The selected UI-tab when OK was pressed")

	def effect(self):
		totalPathCoords = []

		for node in self.document.getroot().iter():
			if node.tag == '{http://www.w3.org/2000/svg}path': # TODO: Ugly
				d = node.get('d')
				path = parsePath(d)

                pathCoords = []
				for point in path:
					x = point[1][0]
					y = point[1][1]
					pathCoords.append([x, y])

				revPathCoords = pathCoords[:] # TODO: Ugly
				revPathCoords.reverse()

				if isInTotalPaths(pathCoords, totalPathCoords, self.options.radius):
					inkex.debug("I WANT TO BREAK FREE")
					node.getparent().remove(node)
				elif self.options.reverse and isInTotalPaths(revPathCoords, totalPathCoords, self.options.radius):
					inkex.debug("I WANT TO BREAK FREE")
					node.getparent().remove(node)
				else:
					totalPathCoords.append(pathCoords)

		inkex.debug('done')

if __name__ == '__main__':
	e = removeDuplicates()
	e.affect()
