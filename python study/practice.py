while True:
    num = int(input("What is your selected range: "))
    count = 0
    for n in range(num+1): 
        if n % 2 == 0:
            count += 1
            print(f"{n} is even")
        else:
            print(f"{n} is not even")
        

    print(f"there are {count} even numbers")
