from csv import DictReader
from deduplicate_whitespace import deduplicate_whitespace

EXPECTED_CHARS = "0123456789-.#*"

with open("formatted_data/locations_final.csv", "r", encoding="utf-8") as locationsCsvFile:
	refs = [row["ref"] for row in DictReader(locationsCsvFile)]
	
for ref in refs:
	print(ref)
	
	with open(f"original_txt/{ref}.txt", "r", encoding="utf-8") as inFile:
		text = deduplicate_whitespace(inFile.read())
	
	lines = [line.strip() for line in text.split("hours\n")[1].splitlines()]
	for line in lines:
		printedLine = False
		for piece in line.split(" "):
			for character in piece:
				if character not in EXPECTED_CHARS:
					print(f"\t{line}")
					printedLine = True
					break
			if printedLine:
				break