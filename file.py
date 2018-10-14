


def readTextFile(filename):

	string = None

	with open(filename,'r') as file:
		string = file.read()

	return string

def readBinaryFile(filename):

	data = bytes()

	with open(filename,'rb') as file:
		string = file.read()
		data = bytes(string)

	return data