student = {"name": "Aryan", "age": 22, "courses": ["python", "javascript"]}


#returns error
#print(student["phone"])

#returns "None"
print(student.get("phone"))

#setting default value
print(student.get("phone", "Not Found"))

#adding/updating the dictionary
student["phone"] = "9803732718"

#updating in a single step, all that needs be
student.update({"name": "Aryan Karki", "address": "kapan, kathmandu"})

#deleting key-value
del student ["courses"]

#popping from the dict and into a new variable
age = student.pop("age")

#keys and values separately and together
print(student.keys())
print(student.values())
print(student.items())

#printing each pair on separate lines  
for key, value in student.items():
    print (key,value)

print(student)
print(age)
