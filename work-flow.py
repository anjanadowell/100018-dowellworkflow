''' Work Flow related functions   '''


# Assuming the predefined workflow
work_flow_predefined = {
	'invoice': {
		'document_prepared_by'    : { 'name': 'abc', 'staff_id': 1, 'email': 'abc@dowell.com'	},
		'request_approved_by'     : { 'name': 'abc', 'staff_id': 2, 'email': 'abc@dowell.com'	},
		'payment_initiated_by'    : { 'name': 'abc', 'staff_id': 3, 'email': 'abc@dowell.com'	},
		'payament_approved_by'    : { 'name': 'abc', 'staff_id': 4, 'email': 'abc@dowell.com'	},
		'payment_received_by'     : { 'name': 'abc', 'staff_id': 5, 'email': 'abc@dowell.com'	},
		'documented_by'           : { 'name': 'abc', 'staff_id': 6, 'email': 'abc@dowell.com'	},
	}
}


# Assuming the Document object
class Document():
	doc_name = None
	doc_type = None
	work_flow = None

	def __init__(self, name, doc_type):
		self.doc_name = name
		self.doc_type = doc_type

	def __repr__(self):
		return f'{self.doc_name} has type {self.doc_type} is assigned to {self.work_flow}'


# process 200
def process_200(doc_type):
	''' if no process available create process'''
	new_process = {
		'document_prepared_by'    : { 'name': 'abc', 'staff_id': 1, 'email': 'abc@dowell.com'	},
		'request_approved_by'     : { 'name': 'abc', 'staff_id': 2, 'email': 'abc@dowell.com'	},
		'payment_initiated_by'    : { 'name': 'abc', 'staff_id': 3, 'email': 'abc@dowell.com'	},
		'payament_approved_by'    : { 'name': 'abc', 'staff_id': 4, 'email': 'abc@dowell.com'	},
		'payment_received_by'     : { 'name': 'abc', 'staff_id': 5, 'email': 'abc@dowell.com'	},
		'documented_by'           : { 'name': 'abc', 'staff_id': 6, 'email': 'abc@dowell.com'	},
	}
	# saving new process in our predefined work_flow for later user
	work_flow_predefined[doc_type] = new_process

	return new_process

# first function to be called on doc
def assign_work_flow(doc):
	if doc.doc_type == None:
		doc.work_flow = None

	# checking for availability of work_flow and assigning it
	if doc.doc_type in work_flow_predefined.keys():
		doc.work_flow = work_flow_predefined[doc.doc_type]
	else:
		#if work_flow not available call process_200 for creation
		doc.work_flow = process_200(doc.doc_type)
	return doc



# *******************   work-flow execution part  **************************
# pip install apscheduler

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
 
#signing simulation
def simulating_signing_process(**kwargs):
	print('Sent document for signing at', kwargs['to'])
	import time
	time.sleep(15)
	print('Document Signed by: ', kwargs['to']['staff_id'])


#event listner for scheduler fired each time job is completed
def scheduler_event_listener(event):
	if event.exception:
		print('The job crashed :(')
	else:
		print('The job executed :)')


def document_signing_process(doc):
	# initializing schedular
	scheduler = BackgroundScheduler(executors={'default': {'type':'threadpool', 'max_workers': 1}})
	
	# adding Event Listner to scheduler
	scheduler.add_listener(scheduler_event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
	
	#starting scheduler
	scheduler.start()

	#for each step in work-flow adding jobs in sheduler
	for step in doc.work_flow.keys():
		print('Step In work-flow', step)
		scheduler.add_job(simulating_signing_process, misfire_grace_time=None, kwargs={'to':doc.work_flow[step]})

	return doc




# raising exception when running file directly but in flask framework I tested No exception occured 
if __name__ == '__main__':
	# creating the document object
	doc = Document('Document Name', 'invoice')
	doc = assign_work_flow(doc)
	doc = document_signing_process(doc)
