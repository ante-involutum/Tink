from kubernetes import client, config


service_name = "jmeter-master"


def create_service_object():

    spec = client.V1ServiceSpec(
        selector={"app": "jmeter-master"},
        ports=[client.V1ServicePort(
            protocol="TCP",
            name="metrics",
            port=9270,
        )],
        cluster_ip=None)

    service = client.V1Service(
        api_version='v1',
        kind='Service',
        metadata=client.V1ObjectMeta(
            name=service_name,
            labels={"app": 'jmeter-master'}
        ),
        spec=spec
    )
    return service


def create_service(api, service):

    resp = api.create_namespaced_service(
        body=service, namespace="default"
    )
    return resp


def update_service(api, service):

    service.spec.ports[0].name = "jmeter-metrics"

    resp = api.patch_namespaced_service(
        name=service_name, namespace="default", body=service
    )
    return resp


def delete_service(api):

    resp = api.delete_namespaced_service(
        name=service_name, namespace="default")
    return resp


def main():

    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    service = create_service_object()

    create_service(core_v1, service)
    update_service(core_v1, service)
    delete_service(core_v1)


if __name__ == "__main__":
    # main()
    pass
