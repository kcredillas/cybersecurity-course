import re
def textprocessing():
    text = "Today is Tuesday"
    match = re.split("[^a-zA-z0-9]", text)
    processed = ""
    for word in match:
        processed += word
    print (processed)

textprocessing()
