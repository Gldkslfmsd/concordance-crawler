import os
from time import time, ctime
import shutil

defaultargs = {
	"backup_off" : None,
	"number_of_concordances" : 10,
	"buffer_size" : 1000000,
	"disable_english_filter" : None,
	"extend_corpus" : None,
	"verbosity" : 0,
	"encoding" : None,
	"max_per_page" : None,
	"output" : "",
	"part_of_speech" : ".*",
	"bazword_generator" : "RANDOM",
	"format" : "json",
	"word" : [],
	"backup_file" : "ConcordanceCrawler.backup",
	"continue_from_backup" : None,
}

DIR = 'static/jobs/'

def get_next_job_id():
	try:
		with open("jobid","r") as f:
			id = int(f.read())+1
	except FileNotFoundError:
		id = 1
	finally:
		f = open("jobid","w")
		f.write(str(id))
		f.close()
	return id

def create_new_job(data):
	args = defaultargs.copy()
	for k,v in data.items():
		if k=='target': continue
		args[k] = v
	args['number_of_concordances'] = int(args['number_of_concordances'])
	args['max_per_page'] = int(args['max_per_page'])
	args['word'] = data['target'].split()

	id = get_next_job_id()
	path = DIR+'job'+str(id)
	os.makedirs(path)
	
	args['output'] = path+'/corpus.json'

	backup = open(path+'/backup',"w")
	backup.write(str(args))
	backup.close()

	status = open(path+'/status','w')
	status.write('CREATED\n')
	status.close()

	tf = open(path+'/time','w')
	tf.write(str(time()))
	tf.close()

	return 'OK'

def get_status(jobid):
	f = open(DIR+jobid+"/status","r")
	status = f.readlines()[-1].strip()
	f.close()
	return status

def get_args(jobid):
	f = open(DIR+jobid+"/backup","r")
	b = f.read()
	f.close()
	args = eval(b)
	return args

def get_target(jobid):
	return " ".join(get_args(jobid)['word'])

def get_pos(jobid):
	return get_args(jobid)['part_of_speech']

def get_max_per_page(jobid):
	return get_args(jobid)['max_per_page']
def get_english_filter(jobid):
	return get_args(jobid)['disable_english_filter']
def get_bazgen(jobid):
	return get_args(jobid)['bazword_generator']
def get_encoding(jobid):
	return get_args(jobid)['encoding']

def get_time(jobid):
	'''returns submition time in unix format as float'''
	f = open(DIR+jobid+"/time","r")
	t = float(f.read().strip())
	f.close()
	return t

def get_ctime(jobid):
	'''returns submition time as string in human readable form'''
	t = get_time(jobid)
	return ctime(t).strip()


zero_crawling_status = """serp		0 (0 errors)
links crawled	0 (0 filtered because of format suffix, 0 crawled repeatedly)
pages visited	0 (0 filtered by encoding filter, 0 filtered by language filter, 0 errors)
concordances	0 (0 crawled repeatedly)""".split("\n")

def get_crawling_status(jobid):
	try:
		f = open(DIR+jobid+"/logfile.txt","r")
	except FileNotFoundError:
		return zero_crawling_status
	cs = []
	i = -1
	for line in f:
		if "STATUS: Crawling status" in line:
			i = 0
			cs = []
		if 1 <= i <= 4:
			cs.append(line.strip())
		if i==4:
			i = -1
		elif i!=-1:
			i += 1
	f.close()
	if not cs:
		return zero_crawling_status
	return cs

def get_concordances_crawled(jobid):
	'''returns number of concordances actually crawled after restart'''
	num = get_crawling_status(jobid)[-1].split()[1]
	return int(num)

def get_number_of_concordances(jobid):
	'''returns desired number of concordances'''
	return get_args(jobid)['number_of_concordances']

def get_percent_str(j):
	return str(int(min(100,get_concordances_crawled(j)/get_number_of_concordances(j)*100)))


def delete_job(jobid):
	try:
		shutil.rmtree(DIR+jobid)
	except FileNotFoundError:
		return "ERROR"
	else:
		return "OK"

def get_corpus(jobid, start=0, limit=None):
	f = open(DIR+jobid+"/corpus.json","r")
	corp = f.readlines()
	f.close()
	if limit is None:
		limit = len(corp)
	return corp[start:start+limit]


def browse_jobs():
	return os.listdir(DIR)

if __name__ == "__main__":
	for j in browse_jobs():
		break
		print(get_status(j),get_target(j))
		print(j)
		print("\n".join(get_crawling_status(j)))
		print(get_time(j))
		break


#	print(zero_crawling_status)#[-1].split("\t"))
#	print(get_percent_str("job37"))

	print(delete_job("job37"))

