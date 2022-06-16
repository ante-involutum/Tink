import os
from fastapi import FastAPI
from kubernetes import client, config
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from src.utils.job import *
from src.utils.service import *

jobs = []

app = FastAPI()


class Item(BaseModel):
    name: str
    jmx: str


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


@app.post("/job")
async def job_create(item: Item):
    job = create_job_object(item.name, item.jmx)
    resp = create_job(batch_v1, job)
    jobs.append(item.name)
    return resp.status.to_dict()


@app.get("/job/{job_name}")
async def job_status(job_name):
    resp = get_job_status(batch_v1, job_name)
    return resp.status.to_dict()


@app.patch("/job/{job_name}")
async def job_update(job_name):
    job = create_job_object(job_name)
    resp = update_job(batch_v1, job, job_name)
    return resp.status.to_dict()


@app.delete("/job/{job_name}")
async def job_delete(job_name):
    resp = delete_job(batch_v1, job_name)
    jobs.remove(job_name)
    return resp.status


@app.get("/jobs")
async def job_create():
    return jobs
