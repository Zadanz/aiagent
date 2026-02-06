from functions.get_file_content import get_file_content

def test_get_file_content():
    print("Result for file 'lorem.txt':")
    print(get_file_content("calculator", "lorem.txt"))

    print("Result for file 'main.py':")
    print(get_file_content("calculator", "main.py"))

    print("Result for file 'pkg/calculator.py':")
    print(get_file_content("calculator", "pkg/calculator.py"))
    
    print("Result for file '/bin/cat':")
    print(get_file_content("calculator", "/bin/cat"))

    print("Result for file 'pkg/does_not_exist.py':")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    test_get_file_content()