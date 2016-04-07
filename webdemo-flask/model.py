import os

defaultargs = {
	"word" : [],
	"number_of_concordances" : 10,
	"output" : "corpus.json",
	"backup_off" : None,
	"bazword_generator" : "RANDOM",
	"continue_from_backup" : None,
	"max_per_page" : None,
	"part_of_speech" : None,
	"backup_file" : "backup",
	"disable_english_filter" : None,
	"encoding" : None,
	"verbosity" : 0,
	"format" : "json",
	"extend_corpus" : None,
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
	args['part_of_speech'] = 'x'
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

	return 'OK'

def get_status(jobid):
	f = open(DIR+jobid+"/status","r")
	status = f.readlines()[-1].strip()
	f.close()
	return status

def get_target(jobid):
	f = open(DIR+jobid+"/backup","r")
	b = f.read()
	f.close()
	args = eval(b)
	return args['word'][0]

def browse_jobs():
	print(os.listdir(DIR))
	return os.listdir(DIR)
	

if __name__ == "__main__":
	for j in browse_jobs():
		print(get_status(j),get_target(j))
