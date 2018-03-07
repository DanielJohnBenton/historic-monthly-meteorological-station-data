import os
from deduplicate_whitespace import deduplicate_whitespace

originalTxtDir = "original_text"
outputDir = "output"

fileNames = [fileName for fileName in os.listdir(originalTxtDir) if fileName.lower().endswith(".txt")]

locationOutput = "name,easting,northing,grid,lat,lon,metres_amsl,changed_location,prev_easting,prev_northing,prev_lat,_prev_lon,prev_metres_amsl,last_year_location_1,last_month_location_1,first_year_location_2,first_month_location_2"

for fileName in fileNames:
	with open(f"{originalTxtDir}/{fileName}", "r", encoding="utf-8") as inFile:
		text = deduplicate_whitespace(inFile.read())
	lines = [line.strip() for line in text.splitlines()]
	
	# a few files need manual intervention as they have details about changed locations
	if not lines[2].startswith("Estimated"):
		print(f"File requires manual intervention: {lines[0]}")
		locationOutput += f"\n{lines[0]},,,,,,,Y,,,,,,,,,"
		continue
	
	tokens = lines[1].split(" ")
	
	easting = tokens[1]
	northing = tokens[2][:-1] # remove ,
	
	if tokens[3] == "(Irish":
		grid = "Irish"
		lat = tokens[6]
		lon = tokens[8][:-1] # remove ,
		metresAmsl = tokens[9]
	else:
		grid = "British"
		lat = tokens[4]
		lon = tokens[6][:-1] # remove ,
		metresAmsl = tokens[7]
	
	if metresAmsl.lower().endswith("m"):
		metresAmsl = metresAmsl[:-1] # remove m
	if easting.lower().endswith("e"):
		easting = easting[:-1] # remove e
	if northing.lower().endswith("n"):
		northing = northing[:-1] # remove n
	
	locationOutput += f"\n{lines[0]},{easting},{northing},{grid},{lat},{lon},{metresAmsl},N,,,,,,,,,"
	
with open(f"{outputDir}/locations_initial_output.csv", "w", encoding="utf-8") as outFile:
	outFile.write(locationOutput)