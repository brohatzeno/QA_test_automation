#functions

def greet():
    name = input("what is your name: ")
    print(f"Hello! {name}, Welcome to Python!")
    #perform a task

greet()

def get_greeting():
    nme = input("What is your name: ")
    return f"Hello {nme}, welcome to python"
    #return a value

print(get_greeting())