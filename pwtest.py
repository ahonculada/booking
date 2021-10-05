with open("./secrets/password.txt") as file:
    Lines = file.readlines()

for line in Lines:
    print(line.strip())
