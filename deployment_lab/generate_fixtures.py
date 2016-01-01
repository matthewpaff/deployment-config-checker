"""Original mock deployment inputs and independently specified outcomes."""


def make_case(index):
    kind = index % 10
    replicas, cpu, memory = 1 + index % 4, 100 + index % 5 * 100, 128 + index % 8 * 64
    interval = 10 + index % 6
    data = {"service": "sample-{}".format(index), "replicas": replicas,
            "resources": {"cpu_millis": cpu, "memory_mb": memory},
            "health": {"path": "/ready", "interval_seconds": interval, "timeout_seconds": 2, "failure_threshold": 3}}
    if kind == 0:
        data["replicas"] = 0
        description = "reject deployments without any replicas"
    elif kind == 1:
        data["resources"]["cpu_millis"] = True
        description = "reject boolean CPU requests"
    elif kind == 2:
        data["health"]["timeout_seconds"] = interval
        description = "reject probe timeouts equal to their intervals"
    elif kind == 3:
        data["health"]["path"] = "ready"
        description = "reject health paths without a leading slash"
    elif kind == 4:
        data["service"] = "Invalid Name"
        description = "reject uppercase or spaced service names"
    elif kind in (5, 6):
        path = "/live" if kind == 6 else "/ready"
        data["health"]["path"] = path
        expected = {"service": data["service"], "replicas": replicas, "total_cpu_millis": replicas * cpu,
                    "total_memory_mb": replicas * memory, "health_path": path,
                    "configured_failure_window_seconds": interval * 3}
        description = "calculate bounded deployment resource totals and probe windows"
    elif kind == 7:
        data["replicas"], data["resources"]["cpu_millis"] = 50, 16000
        description = "reject aggregate CPU requests above the deployment budget"
    elif kind == 8:
        data["resources"]["memory_mb"] = 0
        description = "reject zero-sized memory requests"
    else:
        data["image"] = "unrecognized"
        description = "reject unrecognized deployment settings"
    case = {"id": "deployment-{:04d}".format(index), "description": description, "input": data}
    case.update({"expected": expected} if kind in (5, 6) else {"expected_error": True})
    return case
