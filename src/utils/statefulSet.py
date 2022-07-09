import datetime
import pytz
from kubernetes import client, config

stateful_set_name = "jmeter-master"


def create_stateful_set_object(file_name="/jmx/example.jmx"):

    secret_key_ref = client.V1SecretKeySelector(
        key='admin-user-token', name='middleware-influxdb')
    value_from = client.V1EnvVarSource(secret_key_ref=secret_key_ref)

    container = client.V1Container(
        name="jmeter-master",
        image="mx2542/anti-jmeter:1.0",
        command=["sleep"],
        args=["infinity"],
        # command=["./apache-jmeter-5.4.3/bin/jmeter.sh"],
        # args=["-n", "-t", file_name],
        ports=[client.V1ContainerPort(container_port=9270)],
        image_pull_policy='IfNotPresent',
        volume_mounts=[client.V1VolumeMount(mount_path='/jmx', name='jmx')],
        # env=[client.V1EnvVar(name='INFLUXDB_TOKEN', value_from=value_from)]
    )

    persistent_volume_claim = client.V1PersistentVolumeClaimVolumeSource(
        claim_name='jmx-nfs-pvc')

    template = client.V1PodTemplateSpec(

        metadata=client.V1ObjectMeta(
            labels={"app": "jmeter-master"}
        ),
        spec=client.V1PodSpec(
            containers=[container],
            volumes=[
                client.V1Volume(
                    name='jmx', persistent_volume_claim=persistent_volume_claim)
            ]
        )
    )

    spec = client.V1StatefulSetSpec(

        selector={
            "matchLabels": {"app": "jmeter-master"}
        },
        service_name="jmeter-master",
        replicas=2,
        template=template,
    )

    stateful_set = client.V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(name=stateful_set_name),
        spec=spec
    )
    return stateful_set


def create_stateful_set(api, stateful_set):

    resp = api.create_namespaced_stateful_set(
        body=stateful_set, namespace="default"
    )
    return resp


def update_stateful_set(api, stateful_set):

    stateful_set.spec.template.spec.containers[0].command = ["sleep"]
    stateful_set.spec.template.spec.containers[0].args = ["infinity"]
    # stateful_set.spec.replicas = 3

    resp = api.patch_namespaced_stateful_set(
        name=stateful_set_name, namespace="default", body=stateful_set
    )
    return resp


def restart_stateful_set(api, stateful_set):

    stateful_set.spec.template.metadata.annotations = {
        "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow()
        .replace(tzinfo=pytz.UTC)
        .isoformat()
    }

    resp = api.patch_namespaced_stateful_set(
        name=stateful_set_name, namespace="default", body=stateful_set
    )
    return resp


def delete_stateful_set(api):

    resp = api.delete_namespaced_stateful_set(
        name=stateful_set_name,
        namespace="default",
    )
    return resp


def main():

    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    stateful_set = create_stateful_set_object()

    create_stateful_set(apps_v1, stateful_set)
    update_stateful_set(apps_v1, stateful_set)
    restart_stateful_set(apps_v1, stateful_set)
    delete_stateful_set(apps_v1)


if __name__ == "__main__":
    # main()
    pass
