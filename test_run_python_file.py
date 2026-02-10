from functions.run_python_file import run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print("Prints calculator usage instructions")
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Returns calculators result")
    print(result)

    result = run_python_file("calculator", "tests.py")
    print("Runs calculator test")
    print(result)

    result= run_python_file("calculator", "../main.py")
    print("Returns results for '../main.py'")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print("Returns results for nonexistent file")
    print(result)

    result = run_python_file("calculator", "lorem.txt")
    print("Returns result for lorem.txt file")
    print(result)

if __name__ == "__main__":
    test()
