with open('settings.txt', encoding='utf-8') as f:
    for line in f.readlines():
        text = "self." + line
        print(text)
