import json


def store_job_by_id(**kwargs):  # id for lookup and job is string/filepath
    with open('job_data.json', "r") as jsondata:
        job_data = json.load(jsondata)
    job_data.update(kwargs)
    with open("job_data.json", "w") as write_json:
        json.dump(job_data, write_json)


def search_job_by_id(jobid):
    with open('job_data.json', "r") as jsondata:
        job_data = json.load(jsondata)

    # load the json data
    if jobid in job_data:
        return job_data[jobid]
    else:
        return None

def remove_job_by_id(jobid):
    with open('job_data.json', "r") as jsondata:
        job_data = json.load(jsondata)
    if jobid in job_data:
    	del job_data[jobid]
    with open("job_data.json", "w") as write_json:
        json.dump(job_data, write_json)

store_job_by_id(jobid_1='xyz', jobid_2='abc')
x = "jobid_2"
print(search_job_by_id(x))
remove_job_by_id("jobid_1")
store_job_by_id(jobid_3='xyzv')

