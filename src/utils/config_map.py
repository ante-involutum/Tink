"""
Creates, updates, and deletes a configmap object.
"""


import os
from minio import Minio

from kubernetes import client, config


config.load_kube_config()


namespace = os.getenv('NAMESPACE')


minioClient = Minio(
    '192.168.100.10:31447',
    access_key='admin',
    secret_key='changeme',
    secure=False
)


obj = minioClient.get_object('jmx', 'example.jmx')

metadata = client.V1ObjectMeta(name='config-demo')

config_map = client.V1ConfigMap(

    api_version='v1',
    kind='ConfigMap',
    data={
        'example.yaml': obj.data.decode('utf-8')
    },
    metadata=metadata

)

core_v1 = client.CoreV1Api()

result = core_v1.create_namespaced_config_map(
    namespace=namespace,
    body=config_map,

)
