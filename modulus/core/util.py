import os


def flatten_resources(toml_data):
    flat = {}
    for resource_type, resources in toml_data.items():
        if isinstance(resources, dict):
            for name, res in resources.items():
                flat[(resource_type, name)] = res
    return flat