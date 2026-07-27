from functions.get_file_content import get_file_content

tests = [
    ["calculator", "main.py"],
    ["calculator", "pkg/calculator.py"],
    ["calculator", "/bin/cat"],
    ["calculator", "pkg/does_not_exist.py"],
]

lorem_name = "lorem.txt"
lorem_result = get_file_content("calculator", lorem_name)
print(f"{lorem_name} length: {len(lorem_result)}")
print(f"{lorem_name} truncated: {'truncated' in lorem_result}")

for test in tests:
    print(get_file_content(test[0], test[1]))

