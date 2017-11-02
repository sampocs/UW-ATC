import os, sys
deps_dir = os.path.dirname(os.path.abspath(__file__))
import json

def load_json (fileName):
	with open  (deps_dir + '/' + fileName) as data_file:
		return json.load(data_file)

def write_json (fileName, newFile):
	with open (deps_dir + '/' + fileName, 'w') as data_file:
		data_file.write(json.dumps(newFile, indent = 4, separators = (',', ':'), sort_keys=True))
		