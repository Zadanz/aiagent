from functions.run_python_file import run_python_file

def test_write_file():
    print("Result for file 'main.py':")
    print(run_python_file("calculator", "main.py"))

    print("Result for file 'main.py' with extra args:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print("Result for file 'tests.py':")
    print(run_python_file("calculator", "tests.py"))

    print("Result for file '../main.py':")
    print(run_python_file("calculator", "../main.py"))

    print("Result for file 'nonexistent.py':")
    print(run_python_file("calculator", "nonexistent.py"))

    print("Result for file 'lorem.txt':")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    test_write_file()