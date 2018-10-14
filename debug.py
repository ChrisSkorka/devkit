"""
Debug provides methods for code debigging purposes

"""



import sys
import time

#debugging statement print
#acts as print() but inserts caller stack frame information as first argument
#------------------------------------------------------------------------------
def log(*args, **kwargs):

	#create fake exception to create a stack trace
	try:
		raise FakeException("Fake Exception")
	except Exception:
		#get second last stack frame (dprint caller)
		frame = sys.exc_info()[2].tb_frame.f_back
	
	#get object of name self in frames function call if exists
	object = frame.f_locals.get("self", None)
	
	#begin string composition
	details = "DEBUG " + time.strftime('%Y/%m/%d %H:%M:%S') + " "
	
	#if function call included self add containing class name
	if object:
		details += object.__class__.__name__ + "::"
	
	#add function name and line number
	details += frame.f_code.co_name + "() line " + str(frame.f_lineno) + ":"
	
	#print details and given parameters
	print(details, *args, **kwargs)

#measures time taken to execute a function
#forwards all given parameters to the function specified in first parameter
#executes given function, returns time taken and functions return value
#------------------------------------------------------------------------------	
def measureTime(function, *args, **kwargs):
	
	timeStart = time.time()
	returnValues = function(*args, **kwargs)
	timeEnd = time.time()
	
	return timeEnd - timeStart, returnValues