#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import listdir
from os.path import isfile, join
import codecs
from file_types import ParseObject
import pickle as pkl
import time


def open_unicode_file(name):
    f = codecs.open(name, encoding='utf-8', mode='r').read()
    return f

from extraction import extract_topics, extract_species, extract_regions, extract_antagonists, extract_agonists, \
    extract_year, extract_methods, extract_receptor


def create_objs():
    count = 0
    mypath = "../data/subfiles"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    timers = [0] * 9
    for fname in onlyfiles:
        count += 1
        if count % 10 == 0:
            print(str(count) + " " + str(timers))
            timers = [0] * 9
        ld = open_unicode_file(mypath + "/" + fname)

        parse = ParseObject()
        t0 = time.time()
        parse.topics = extract_topics(ld)
        t1 = time.time()
        timers[0] += t1 - t0
        parse.species = extract_species(ld)
        t2 = time.time()
        timers[1] += t2 - t1
        parse.regions = extract_regions(ld)
        t3 = time.time()
        timers[2] += t3 - t2
        parse.antagonists = extract_antagonists(ld)
        t4 = time.time()
        timers[3] += t4 - t3
        parse.agonists = extract_agonists(ld)
        t5 = time.time()
        timers[4] += t5 - t4
        parse.year = extract_year(ld)
        t6 = time.time()
        timers[5] += t6 - t5
        parse.methods = extract_methods(ld)
        t7 = time.time()
        timers[6] += t7 - t6
        parse.receptors = extract_receptor(ld)
        t8 = time.time()
        timers[7] += t8 - t7
        pkl.dump(parse, open("../data/pkls/" + fname.replace(".txt", ".p"), "wb"))
        t9 = time.time()
        timers[8] += t9 - t8


def print_csv():
    count = 0
    mypath = "../data/pkls"
    csv = open("../results_test.csv", "w+")
    csv.write("Year,Receptor,Species,Methods,Agonist,Antagonist,Brain_Regions,Topic_Spec\n")

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for fname in onlyfiles:
        count += 1
        if count % 100 == 0:
            print(count)
        obj = pkl.load(open(mypath + "/" + fname, 'rb'))

        obj.species = remove_commas(obj.species)
        obj.agonists = remove_commas(obj.agonists)
        obj.antagonists = remove_commas(obj.antagonists)
        obj.regions = remove_commas(obj.regions)
        obj.topics = remove_commas(obj.topics)

        csv.write(obj.year + ",")
        csv.write(';'.join(obj.receptors) + ",")
        csv.write(';'.join(obj.species) + ",")
        csv.write(';'.join(obj.methods) + ",")
        csv.write(';'.join(obj.agonists) + ",")
        csv.write(';'.join(obj.antagonists) + ",")
        csv.write(';'.join(obj.regions) + ",")
        csv.write(';'.join(obj.topics) + ",")
        csv.write("\n")


def remove_commas(st):
    new_st = set()
    for element in st:
        new_str = ''
        for char in element:
            if char == ',':
                char = ''
            new_str += char
        new_st.add(new_str)
    return new_st


def create_parse(ld):
    parse = ParseObject()
    parse.topics = remove_commas(extract_topics(ld))

    parse.species = remove_commas(extract_species(ld))
    print(parse.species)

    parse.regions = remove_commas(extract_regions(ld))
    print(parse.regions)
    parse.antagonists = remove_commas(extract_antagonists(ld))

    parse.agonists = remove_commas(extract_agonists(ld))

    parse.year = remove_commas(extract_year(ld))

    parse.methods = remove_commas(extract_methods(ld))

    parse.receptors = remove_commas(extract_receptor(ld))
    return parse

def parse_receptors(ld):
    return extract_receptor(ld, True)

if __name__ == "__main__":  create_objs()



