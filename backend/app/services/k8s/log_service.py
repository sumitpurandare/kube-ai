from kubernetes import client, config

def get_k8s_client():
    config.load_kube_config()
    return client.CoreV1Api()

def get_pod_logs(namespace: str, pod_name: str):
    v1 = get_k8s_client()
    return v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)