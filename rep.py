def replace():
    f = open("text.txt", "r")
    text = f.read
    replacing = input("What do you want to replace?")
    replaced = input("What do you want to replace it with?")
    replaced_text = text.replace(f"{replacing,}", f"{replaced}")
    print(replaced_text)

replace()