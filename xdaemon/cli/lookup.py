import json


def store_job_by_id(**kwargs):  # id for lookup and job is string/filepath
    with open("job_data.json", "w") as write_json:
        json.dump(kwargs, write_json)


def search_job_by_id(jobid):
    with open('job_data.json', "r") as jsondata:
        job_data = json.load(jsondata)

    # load the json data
    if jobid in job_data:
        return True
    else:
        return False

store_job_by_id(jobid_1='xyz', jobid_2='abc')
x = "jobid_2"
print(search_job_by_id(x))
