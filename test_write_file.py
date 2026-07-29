from functions.write_file import write_file

tests = [
    ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
    ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
    ["calculator", "/tmp/temp.txt", "this should not be allowed"],
]

for (directory, file, content) in tests:
    print(write_file(directory, file, content))
