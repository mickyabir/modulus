from modulus.core.parser import TomlParser

def verify_llm(resource_type, config):
    print(resource_type)
    for resource, llm_config in config[resource_type].items():
        print(resource)
        print(llm_config)

def verify():
    config_file = "modulus.toml"
    parser = TomlParser()
    config = parser.parse(config_file)
    for resource_type, resources in config.items():
        if resource_type == "llm":
            verify_llm(resource_type, config)