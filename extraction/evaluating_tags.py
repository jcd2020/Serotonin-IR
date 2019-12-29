#!/usr/bin/env python
# coding: utf-8
from os import listdir
from os.path import isfile, join
import random
from shutil import copy
from main import parse_receptors, open_unicode_file
import re

def get_abstracts():
    onlyfiles = [f for f in listdir("../data/subfiles") if isfile(join("../data/subfiles", f))]
    count = 0
    for f in onlyfiles:
        if random.random() > .2 and count < 100:
            count += 1
            copy('../data/subfiles/' + f, '../data/tagged_files')


def extract_tags(text):
    all_tags = []

    while True:
        r1 = re.search(r"##(.*?)##(.*?)##", text)
        if r1:
            tags = r1.group(2).split(", ")
            literal = r1.group(0)
            original = r1.group(1)
            start = r1.start()
            text = text[:start] + original + text[start+len(literal):]
            for tag in tags:
                all_tags.append((tag, start, start+len(original)))
        else:
            break
    return all_tags,text


def find_gt_label(label, start_idx, ground_truth):
    for lab, strt, _ in ground_truth:
        if lab == label and strt == start_idx:
            return True
    return False

def eval_tags(parse_res, ground_truth):
    tp, fp = 0, 0

    for label,start_idx,_ in parse_res:
        if(find_gt_label(label, start_idx, ground_truth)):
            tp += 1.
        else:
            fp += 1.

    tp, fn = 0, 0
    for label, start_idx, _ in ground_truth:
        if(find_gt_label(label, start_idx, parse_res)):
            tp += 1.
        else:
            fn += 1.

    return tp,fp,fn
def open_tagged_file():
    onlyfiles = [f for f in listdir("../data/tagged_files_CamComplete") if isfile(join("../data/tagged_files_CamComplete", f))]
    total = 0
    tp,fp,fn = 0.,0.,0.
    for f in onlyfiles:
        text = open_unicode_file("../data/tagged_files_CamComplete/" + f)
        tags_extracted, clean_text = extract_tags(text)
        total += len(tags_extracted)
        parse = parse_receptors(clean_text)
        tp1,fp1,fn1 = eval_tags(parse, tags_extracted)
        tp += tp1
        fp += fp1
        fn += fn1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    print(precision)
    print(recall)
    print(total)

if __name__ == "__main__":  open_tagged_file()

