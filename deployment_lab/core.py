"""Validate local JSON settings without contacting a scheduler or starting a service."""
import re


def integer(value, label, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("{} must be an integer from {} to {}".format(label, low, high))
    return value


def fields(value, expected, label):
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError("{} requires exactly: {}".format(label, ", ".join(sorted(expected))))


def validate_deployment(data):
    fields(data, {"service", "replicas", "resources", "health"}, "Deployment")
    name = data["service"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,39}", name):
        raise ValueError("Service must start with a lowercase letter and use up to 40 letters, digits, or hyphens")
    replicas = integer(data["replicas"], "replicas", 1, 50)
    resources = data["resources"]
    fields(resources, {"cpu_millis", "memory_mb"}, "Resources")
    cpu = integer(resources["cpu_millis"], "cpu_millis", 1, 16000)
    memory = integer(resources["memory_mb"], "memory_mb", 16, 131072)
    if replicas * cpu > 64000 or replicas * memory > 524288:
        raise ValueError("Combined resource requests exceed the exercise's deployment budget")
    health = data["health"]
    fields(health, {"path", "interval_seconds", "timeout_seconds", "failure_threshold"}, "Health check")
    path = health["path"]
    if not isinstance(path, str) or not re.fullmatch(r"/(?:[A-Za-z0-9_-]+/?)*", path) or len(path) > 120:
        raise ValueError("Health path must be a simple absolute path of at most 120 characters")
    interval = integer(health["interval_seconds"], "interval_seconds", 1, 300)
    timeout = integer(health["timeout_seconds"], "timeout_seconds", 1, 60)
    threshold = integer(health["failure_threshold"], "failure_threshold", 1, 10)
    if timeout >= interval:
        raise ValueError("Health timeout must be shorter than its interval")
    return {"service": name, "replicas": replicas, "total_cpu_millis": replicas * cpu,
            "total_memory_mb": replicas * memory, "health_path": path,
            "configured_failure_window_seconds": interval * threshold}
