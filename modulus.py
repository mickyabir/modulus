# from modulus.cli.main import app
# 
# if __name__ == "__main__":
#     app()


from modulus.core.parser import TomlParser


if __name__ == "__main__":
    parser = TomlParser()
    result = parser.parse("examples/schema.toml")
    for resource_type, resources in result.items():
        print(f"Resource type: {resource_type}")
        for name, resource in resources.items():
            print(f"  {name}: {resource}")
