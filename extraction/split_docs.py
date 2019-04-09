#!/usr/bin/env python
# coding: utf-8


from extraction import extract_receptor
import re
names = set()
def invalid(text):
    receptors = extract_receptor(text)
    m = re.search(r"\"(.*?)\"", text.split("\n")[0])
    if not m:
        print text
        return False
    title = re.compile('[^a-zA-Z0-9]+').sub('', m.group(1).lower())
    if title in names:
        return True
    else:
        names.add(title)
    if len(receptors) == 0:
        return True
    if "review" in text.lower():
        return True
    return False
docs = open("../data/db.txt", "r")
def run():
    new_db = open("../data/db_new.txt", "w")
    count = 0
    curr_doc = ""
    size = 0
    for nl in docs:
        if re.match(r"^\s*$",nl):
            if size > 1:
                if not invalid(curr_doc):
                    out = open("../data/subfiles/doc" + str(count) + ".txt", "w")
                    out.write(curr_doc)
                    out.close()
                    new_db.write(curr_doc + "\n")
            curr_doc = ""
            count+=1
            size = 0
        else:
            curr_doc += nl + "\n"
            size += 1
    new_db.close()



if __name__ == "__main__": run()




