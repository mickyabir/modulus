import os
from colorama import Fore, Style, init as colorama_init
from modulus.core.parser import TomlParser
from modulus.core.util import flatten_resources

colorama_init()

STATE_FILE = ".modulus.state.toml"
CONFIG_FILE = "modulus.toml"

def plan():
    parser = TomlParser()
    config_data = parser.parse(CONFIG_FILE)
    config_resources = flatten_resources(config_data)

    if os.path.isfile(STATE_FILE):
        state_data = parser.parse(STATE_FILE)
        state_resources = flatten_resources(state_data)
    else:
        state_resources = {}

    planned_add = []
    planned_change = []
    planned_delete = []

    existing_resources = state_resources.copy()

    def diff_dict(old, new):
        diffs = []
        all_keys = set(old.keys()) | set(new.keys())
        for key in sorted(all_keys):
            old_val = old.get(key)
            new_val = new.get(key)

            if isinstance(old_val, dict) and isinstance(new_val, dict):
                # Flatten nested dict changes as individual entries
                sub_keys = set(old_val.keys()) | set(new_val.keys())
                for sub_key in sorted(sub_keys):
                    old_sub = old_val.get(sub_key)
                    new_sub = new_val.get(sub_key)

                    if sub_key not in old_val:
                        diffs.append(f"    + {sub_key} = {new_sub!r}")
                    elif sub_key not in new_val:
                        diffs.append(f"    - {sub_key} (was {old_sub!r})")
                    elif old_sub != new_sub:
                        diffs.append(f"    ~ {sub_key}: {old_sub!r} -> {new_sub!r}")
            else:
                if key not in old:
                    diffs.append(f"    + {key} = {new_val!r}")
                elif key not in new:
                    diffs.append(f"    - {key} (was {old_val!r})")
                elif old_val != new_val:
                    diffs.append(f"    ~ {key}: {old_val!r} -> {new_val!r}")

        return list(dict.fromkeys(diffs))

    for key, attrs in config_resources.items():
        attrs = vars(attrs)
        attrs = {k: v for k, v in attrs.items() if k != "name"}
        if key not in state_resources:
            planned_add.append((key[0], key[1], attrs))
        else:
            existing = vars(state_resources[key])
            existing = {k: v for k, v in existing.items() if k != "name"}

            if existing != attrs:
                changes = diff_dict(existing, attrs)
                planned_change.append((key[0], key[1], changes))

            existing_resources.pop(key)

    planned_delete = list(existing_resources.keys())

    if not planned_add and not planned_change and not planned_delete:
        print(f"{Fore.GREEN}No changes to be made.{Style.RESET_ALL}")
    else:
        print("Planned changes:")
        for rt, name, _ in planned_add:
            print(f"{Fore.GREEN}  + create {rt}.{name}{Style.RESET_ALL}")
        for rt, name, changes in planned_change:
            print(f"{Fore.YELLOW}  ~ update {rt}.{name}{Style.RESET_ALL}")
            for line in changes:
                prefix = line.strip()[0]
                color = (
                    Fore.GREEN if prefix == "+" else
                    Fore.RED if prefix == "-" else
                    Fore.YELLOW
                )
                print(f"{color}{line}{Style.RESET_ALL}")
        for rt, name in planned_delete:
            print(f"{Fore.RED}  - delete {rt}.{name}{Style.RESET_ALL}")
