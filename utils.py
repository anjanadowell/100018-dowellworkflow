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

def document_signing_process(document_object, work_flow):
	# initializing schedular
	scheduler = BackgroundScheduler(executors={'default': {'type':'threadpool', 'max_workers': 1}})
	# adding Event Listner to scheduler
	scheduler.add_listener(scheduler_event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
	#starting scheduler
	scheduler.start()

	#for each step in work-flow adding jobs in sheduler
	for step in work_flow.steps.all():
		print('Step In work-flow', step)
		try:
			scheduler.add_job(simulating_signing_process, misfire_grace_time=None, kwargs={'to':step})
		except:
			pass

	return document_object


