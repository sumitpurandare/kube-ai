from kubernetes import client, config

def get_pods(namespace: str):
    from kubernetes import client, config

    config.load_kube_config()
    v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=namespace)

    pod_names = [pod.metadata.name for pod in pods.items]

    return pod_names

def get_pod_logs(namespace: str, pod_name: str, container: str = None):
    config.load_kube_config()  # loads ~/.kube/config

    v1 = client.CoreV1Api()

    logs = v1.read_namespaced_pod_log(
        name=pod_name,
        namespace=namespace,
        container=container
    )

    return logs