import os
import subprocess
from model import  *
from time import sleep
import signal
import sys

run_job = 'ConcordanceCrawler  --continue-from-backup '+DIR+'{0}/backup --extend-corpus '+DIR+'{0}/corpus.json'

class Job:
	def __init__(self, jobid):
		self.path = DIR+jobid
		self.jobid = jobid
		self.process = None

	def update_state(self, state):
		f = open(self.path+"/status","a")
		f.write(state+"\n")
		f.close()

	def launch(self,new_state="STARTED"):
		f = open(self.path+"/corpus.json","w")
		f.write('[\n')
		f.close()
		self.process = subprocess.Popen(run_job.format(self.jobid).split(),stderr=open(self.path+"/err","a"))
		self.update_state(new_state)

	def pause(self):
		self.process.send_signal(19)
	
	def resume(self):
		self.process.send_signal(18)

	def running_status(self):
		s = self.process.poll()
		if s is None:
			return "RUNNING"
		if s==0:
			return "FINISHED"
		return "ERROR"

	def __repr__(self):
		return str(self.jobid)

	def interrupt(self):
		if self.running_status()=="RUNNING":
			self.update_state("ABORTED")
		self.process.kill()


class Manager:
	def __init__(self):
		self.running = []
		self.paused = []
		self.maxrunning = 1

	def pause(self):
		if not self.running:
			return
		job = self.running.pop(0)
		job.pause()
		self.paused.append(job)
		print("pausing job",job.jobid)

	def resume(self):
		if not self.paused:
			return
		job = self.paused.pop(0)
		job.resume()
		self.running.append(job)
		print("resuming job",job.jobid)

	def create_job(self,jobid,new_state="STARTED"):
		job = Job(jobid)
		job.launch(new_state)
		print('creating job',jobid)
		self.running.append(job)
		if len(self.running)>self.maxrunning:
			self.pause()

	def check_finished_jobs(self):
		while self.running and self.running[0].running_status()!="RUNNING":
			job = self.running[0]
			rs = job.running_status()
			if rs != "RUNNING":
				self.running.pop(0)
				job.update_state(rs)
				print("job",job.jobid,rs)

	def check(self):
		print("checking")
		for j in browse_jobs():
			if get_status(j) == 'CREATED':
				self.create_job(j)
			if get_status(j) == "ABORTED":
				self.create_job(j,"RESTARTED")
		self.check_finished_jobs()
		for i in range(min(self.maxrunning, len(self.paused))):
			self.pause()
			self.resume()
		print("check end")

	def loop(self):
		while True:
			self.check()
			print("running",self.running, "paused",self.paused)
			sleep(3)

	def interrupt(self,_=None,__=None):
		print("interrupting manager")
		for job in self.running+self.paused:
			job.interrupt()
		sys.exit(1)

manager = Manager()
for signum in (signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
	signal.signal(signum, manager.interrupt)
manager.loop()
