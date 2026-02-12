#!/usr/bin/env python3
# Enhanced CLI Calculator
#This is a Demo for Jira Automation
#Final Testing

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero!"
    return x / y

def power(x, y):
    return x ** y

def modulo(x, y):
    if y == 0:
        return "Error: Division by zero!"
    return x % y

def display_menu():
    print("\n" + "="*30)
    print("ENHANCED CLI CALCULATOR")
    print("="*30)
    print("Select operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Power (^)")
    print("6. Modulo (%)")
    print("7. Exit")
    print("="*30)

def get_numbers():
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return num1, num2
        except ValueError:
            print("Invalid input! Please enter numbers only.")

def display_result(operation, num1, num2, result):
    if isinstance(result, str):  # Error message
        print(f"\n{result}")
    else:
        print(f"\nResult: {num1} {operation} {num2} = {result:.6f}")

def main():
    history = []
    print("Welcome to the ENHANCED CLI Calculator!")

    while True:
        display_menu()
        choice = input("Enter choice (1-7): ").strip()

        if choice == '7':
            print("\nExiting calculator. Thank you for using our calculator!")
            if history:
                print("\nYour Calculation History:")
                for entry in history:
                    print(entry)
            break

        operations = {
            '1': ('+', add),
            '2': ('-', subtract),
            '3': ('*', multiply),
            '4': ('/', divide),
            '5': ('^', power),
            '6': ('%', modulo)
        }

        if choice in operations:
            num1, num2 = get_numbers()
            symbol, func = operations[choice]
            result = func(num1, num2)
            display_result(symbol, num1, num2, result)

            # Store in history
            history.append(f"{num1} {symbol} {num2} = {result if isinstance(result, str) else round(result, 6)}")
        else:
            print("\nInvalid choice! Please select a valid option (1-7).")

if __name__ == "__main__":
    main()
    print("Calculator session ended successfully")
