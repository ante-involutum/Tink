import os
from fastapi import FastAPI
from kubernetes import client, config
from fastapi.middleware.cors import CORSMiddleware


from src.utils.job import *
from src.model.job import Item
from src.utils.service import *
from src.utils.statefulSet import *

jobs = []

app = FastAPI()


origins = [
    # "http://localhost",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv('KUBENETES_ENV') == 'production':
    config.load_incluster_config()
else:
    config.load_kube_config()
batch_v1 = client.BatchV1Api()
core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


@app.post("/tink/job")
async def job_create(item: Item):
    job = create_job_object(item.name, item.jmx)
    resp = create_job(batch_v1, job)
    jobs.append(item.name)
    return resp.status.to_dict()


@app.get("/tink/job/{job_name}")
async def job_status(job_name):
    resp = get_job_status(batch_v1, job_name)
    return resp.status.to_dict()


@app.patch("/tink/job/{job_name}")
async def job_update(job_name):
    job = create_job_object(job_name)
    resp = update_job(batch_v1, job, job_name)
    return resp.status.to_dict()


@app.delete("/tink/job/{job_name}")
async def job_delete(job_name):
    resp = delete_job(batch_v1, job_name)
    jobs.remove(job_name)
    return resp.status


@app.get("/tink/jobs")
async def job_create():
    return jobs


@app.get("/tink/plan")
async def plan_create():
    service = create_service_object()
    stateful_set = create_stateful_set_object()

    create_service(core_v1, service)
    create_stateful_set(apps_v1, stateful_set)

    return jobs
