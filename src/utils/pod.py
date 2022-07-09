import pdb
from kubernetes import client, config


from pydantic import BaseModel


class Pod(BaseModel):
    apiVersion: str = 'v1'
    pod_name: str = None
    command: list = None
    args: list = None
    namespace: str = None


def create_pod_object(pod_name='test1', file_name='/jmx/example.jmx'):

    secret_key_ref = client.V1SecretKeySelector(
        key='admin-user-token',
        name='middleware-influxdb'
    )
    value_from = client.V1EnvVarSource(secret_key_ref=secret_key_ref)

    persistent_volume_claim = client.V1PersistentVolumeClaimVolumeSource(
        claim_name='jmx-nfs-pvc'
    )

    container = client.V1Container(
        name="jmeter",
        image="mx2542/anti-jmeter:1.0",
        # command=["./apache-jmeter-5.4.3/bin/jmeter.sh"],
        # args=["-n", "-t", file_name],
        command=["sleep"],
        args=["infinity"],
        image_pull_policy='IfNotPresent',
        ports=[client.V1ContainerPort(container_port=1099)],
        # volume_mounts=[client.V1VolumeMount(mount_path='/jmx', name='jmx')],
        # env=[client.V1EnvVar(name='INFLUXDB_TOKEN', value_from=value_from)]
    )

    spec = client.V1PodSpec(
        restart_policy="Never",
        containers=[container],
        # volumes=[
        #     client.V1Volume(
        #         name='jmx', persistent_volume_claim=persistent_volume_claim
        #     )
        # ]
    )

    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=spec
    )
    return pod


def create_pod(api_instance, pod):
    resp = api_instance.create_namespaced_pod(body=pod, namespace="default")
    return resp


def get_pod(api_instance):
    resp = api_instance.read_namespaced_pod(name='test1', namespace="default")
    return resp


def delete_pod(api_instance):
    resp = api_instance.delete_namespaced_pod(
        name='test1', namespace="default")
    return resp


def main():

    a = Pod().apiVersion

    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    pod = create_pod_object()

    # resp = create_pod(core_v1, pod)

    resp = get_pod(core_v1)

    resp = delete_pod(core_v1)


if __name__ == "__main__":
    main()
    # pass
