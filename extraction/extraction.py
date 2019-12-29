#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from file_types import Receptor,ReceptorFamily,ReceptorSubtype,ReceptorPrefix,Method
import data.animals as animals
import data.Brain_Regions as br
import data.Agonists as ag
import data.Antagonists as antag
import data.Serotonin_Topics as topics
def match(s, compiled):
    matches = []
    i = 0
    for comp in compiled:
        i += 1
        if(comp.search(s)):
            matches.append((i, comp.pattern))
    return matches
def get_family(suff):
    fam_map = {
        ReceptorFamily._1 : r"(?i)1",
        ReceptorFamily._2 : r"(?i)2",
        ReceptorFamily._3 : r"(?i)3",
        ReceptorFamily._4 : r"(?i)4",
        ReceptorFamily._5 : r"(?i)5",
        ReceptorFamily._6 : r"(?i)6",
        ReceptorFamily._7 : r"(?i)7"
    }
    val = ReceptorFamily.NONE
    for k,v in fam_map.iteritems():
        if(re.search(v,suff)):
            return k, re.search(v,suff).end()
    return ReceptorFamily.NONE,0
def get_sub(suff):
    sub_map = {
        ReceptorSubtype.a : r"(?i)a",
        ReceptorSubtype.b : r"(?i)b",
        ReceptorSubtype.c : r"(?i)c",
        ReceptorSubtype.d : r"(?i)d",
        ReceptorSubtype.e : r"(?i)e",
        ReceptorSubtype.f : r"(?i)f"
    }
    val = ReceptorSubtype.NONE
    for k,v in sub_map.iteritems():
        if(re.search(v,suff)):
            return k
    return ReceptorSubtype.NONE
def extract_receptor(doc, indices=False):
    recepts = set()
    pre = re.compile(ReceptorPrefix._5HT.value)
    for x in pre.finditer(doc):
        suffix = doc[x.end():(x.end()+10)]
        suffixes = re.split(",|/",suffix.replace("(", "").replace(")", "").replace("-", ""))
        pre_family = ReceptorFamily.NONE
        for suff in suffixes:
            recept = Receptor()
            recept.pre = ReceptorPrefix._5HT
            
            suff = suff.strip()
            match = pre.search(suff)
            if match and match.start() == 0:
                continue
            if len(suff) > 0:
                suff_fam,end = get_family(suff[0])
                if suff_fam == ReceptorFamily.NONE:
                    suff_fam = pre_family
                pre_family = suff_fam
                recept.fam = suff_fam
                suff = suff[end:].strip()
                if len(suff) > 0:
                    if len(suff) <= 1 or not suff[1].isalnum():
                        sub = get_sub(suff[0])
                        recept.sub = sub
            if recept.fam != ReceptorFamily.NONE:
                if indices:
                    recepts.add((str(recept), x.start(), x.end()))
    return recepts
def extract_agonists(doc):
    compiled = list(map(lambda x : re.compile(x), ag.strs))
    found = set()
    p1 = re.compile(u'α')
    pattern = re.compile('[^a-zA-Z0-9\s]+')
    doc = pattern.sub('', p1.sub('a', doc)).lower()
    res = match(doc,compiled) 
    
    if len(res) > 0:
        ls = list(map(lambda x : str(x), res))
        for st in ls:
            found.add(st)
    return found
def extract_antagonists(doc):
    compiled = list(map(lambda x : re.compile(x), antag.strs))
    found = set()
    p1 = re.compile(u'α')
    pattern = re.compile('[^a-zA-Z0-9\s]+')
    doc = pattern.sub('', p1.sub('a', doc)).lower()
    res = match(doc,compiled) 
    if len(res) > 0:
        ls = list(map(lambda x : str(x), res))
        for st in ls:
            found.add(st)
    return found

def extract_regions(doc):
    compiled = list(map(lambda x : re.compile(x), br.pats))
    count = 0
    found = set()
    res = match(doc,compiled) 
    if len(res) > 0:
        ls = list(map(lambda x : str(x), res))
        for st in ls:
            found.add(st)
    return found
def extract_species(doc):
    compiled = list(map(lambda x : re.compile(x), animals.pats))
    count = 0
    found = set()
    res = match(doc,compiled) 
    if len(res) > 0:
        ls = list(map(lambda x : str(x), res))
        for st in ls:
            found.add(st)
    return found
def extract_topics(doc):
    compiled = list(map(lambda x : re.compile(x), topics.strs))
    found = set()
    p1 = re.compile(u'α')
    pattern = re.compile('[^a-zA-Z0-9\s]+')
    doc = pattern.sub('', p1.sub('a', doc)).lower()
    res = match(doc,compiled) 
    if len(res) > 0:
        ls = list(map(lambda x : str(x), res))
        for st in ls:
            found.add(st)
    return found
def extract_methods(doc):
    method_map = {
        Method.KNOCKOUT : r"(?i)(knockout)|(([^\w]|$|^(\s+))ko([^\w]|$|^(\s+)))",
        Method.AGONIST : r"(?i)(([^\w]|$|^)agonis[tm])",
        Method.ANTAGONIST : r"(?i)(([^\w]|$|^(\s+))antagonis[tm])",
        Method.OPTOGENETICS : r"(?i)(optogenetic)",
        Method.PET : r"(?i)(positron\s+emission\s+tomography)|(([^\w]|$|^(\s+))pet([^\w]|$|^(\s+)))",
        Method.STAINING : r"(?i)([^\w]|$|^(\s+))(immuno)?(-)?stain",
        Method.STIMULATION : r"(?i)((elec[a-zA-Z]+?)|\(?hz\)?|deep\s+brain)([^\w]|$|^(\s+))stimulat",
        Method.KNOCKDOWN : r"(?i)knockdown",
        Method.IMMUNOHISTOCHEMISTRY : r"(?i)(immuno)(-|\s+)?(histo)(-|\s+)?(chem)"}
    val = set()
    for k,v in method_map.iteritems():
        if(re.search(v,doc)):
            val.add(str(k))
    return val
def extract_year(doc):
    pat = re.compile(r"\(?\b(19|20)\d{2}\b\)?")
    return pat.search(doc).group(0).replace("(", "").replace(")", "")

