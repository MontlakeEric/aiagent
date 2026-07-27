from functions.get_files_info import get_files_info

def print_result(result, friendly_name):
    print(f"Result for {friendly_name} directory:")
    if result[0] == "-":
        print(result.replace("-", "  -"))
    else:
        print("    " + result)

tests = [
    ["calculator", ".", "current"],
    ["calculator", "pkg", "'pkg'"],
    ["calculator", "/bin", "'/bin'"],
    ["calculator", "../", "'../'"],
]

for test in tests:
    print_result(get_files_info(test[0], test[1]), test[2])

