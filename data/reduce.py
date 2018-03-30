
'''
Labo 3 - Visualisation de données 3D avec VTK
Author : Mathieu Monteverde, Sathiya Kirushnapillai

This file reduces altitudes.txt to 30x30 matrices for test purpose

'''
import csv

# Read input file and return a matrix
def readCSV(inputFile, outputFile):

	nbLines = 31
	nbAltitudes = 30

	with open(outputFile, 'w') as output:

		output.write("30 30\n")

		with open(inputFile, 'r') as input:

			nbCurrentLines = 0

			# For each line
			for line in input:
				if(nbCurrentLines == 0):
					nbCurrentLines += 1
					continue

				nbCurrentAltitude = 0

				# For each altitude
				for altitude in line.split():
					output.write(altitude + " ")
					nbCurrentAltitude += 1

					if(nbCurrentAltitude >= nbAltitudes):
						break
				
				output.write("\n")
				nbCurrentLines += 1
				if(nbCurrentLines >= nbLines):
					break
					

readCSV("altitudes.txt", "output.txt")


