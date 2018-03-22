from csv import DictReader
from deduplicate_whitespace import deduplicate_whitespace

NUMBERS_ONLY = "0123456789-."

def resolve_number(text, isSunHours=False):
	if text == "---" or text == "-":
		if isSunHours:
			return "", "N", ""
		else:
			return "", "N"
	
	estimated = "N"
	measurementVia = "Campbell Stokes recorder"
	numbersOnly = ""
	
	for character in text:
		if character in NUMBERS_ONLY:
			numbersOnly += character
	
	if "*" in text:
		estimated = "Y"
		measurementVia = ""
	elif "#" in text:
		measurementVia = "automatic Kipp & Zonen sensor"
	
	if isSunHours:
		return numbersOnly, estimated, measurementVia
	else:
		return numbersOnly, estimated

with open("formatted_data/locations_final.csv", "r", encoding="utf-8") as locationsCsvFile:
	refs = [row["ref"] for row in DictReader(locationsCsvFile)]
	
for ref in refs:
	with open(f"original_txt/{ref}.txt", "r", encoding="utf-8") as inFile:
		text = deduplicate_whitespace(inFile.read().replace("         ", "   ---   "))
	lines = [line.strip().split(" ") for line in text.split("hours\n")[1].splitlines()]
	
	output = "yyyy,mm,tmax_degc,tmin_degc,af_days,rain_mm,sun_hours,sun_hours_measurement_via,tmax_degc_estimated,tmin_degc_estimated,af_days_estimated,rain_mm_estimated,sun_hours_estimated,provisional"
	
	for line in lines:
		if not line[0][0].isdigit():
			continue
		
		while len(line) < 8:
			line.append("---")
		
		yyyy = line[0]
		mm = line[1]
		tmax_degc, tmax_degc_estimated = resolve_number(line[2])
		tmin_degc, tmin_degc_estimated = resolve_number(line[3])
		af_days, af_days_estimated = resolve_number(line[4])
		rain_mm, rain_mm_estimated = resolve_number(line[5])
		sun_hours, sun_hours_estimated, sun_hours_measurement_via = resolve_number(line[6], isSunHours=True)
		provisional = "Y" if line[7].upper() == "PROVISIONAL" else "N"
		
		output += f"\n{yyyy},{mm},{tmax_degc},{tmin_degc},{af_days},{rain_mm},{sun_hours},{sun_hours_measurement_via},{tmax_degc_estimated},{tmin_degc_estimated},{af_days_estimated},{rain_mm_estimated},{sun_hours_estimated},{provisional}"
	
	with open(f"output/{ref}.csv", "w", encoding="utf-8") as outFile:
		outFile.write(output)