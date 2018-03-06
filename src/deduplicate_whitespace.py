def deduplicate_whitespace(text):
	onSpace = True
	onLine = True
	
	processed = ""
	
	for character in text:
		if character == " ":
			onLine = False
			
			if not onSpace:
				processed +=" "
				onSpace = True
		elif character == "\n" or character == "\r":
			onSpace = False
			
			if not onLine:
				processed +="\n"
				onLine = True
		else:
			processed += character
			onLine = False
			onSpace = False
	
	return processed