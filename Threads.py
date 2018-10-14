import threading

#generates a new thread and start executing function passed with arguments
#------------------------------------------------------------------------------	
def newThread(function, *args, **kwargs):
	thread = threading.Thread(target=function, args=(*args,), kwargs=kwargs)
	thread.start()