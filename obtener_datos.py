import json

def obtener():	
	with open('data.json') as f:
		data = json.load(f)
	return data