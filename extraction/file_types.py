from enum import Enum
import re
class ParseObject:
    def __init__(self):
        self.year = 0
        self.methods = set() #closed set - see ENUM
        self.species = set() #latently discovered set - wordnet
        self.antagonists = set() #latently discovered set - dep-parse based
        self.agonists = set() #latently discovered set - dep-parse based
        self.receptors = set() #closed set 
        self.regions = set() #
        self.topics = None #discover via clustering
class Method(Enum):
    KNOCKOUT = r"(?i)(knockout)|(([^\w]|$|^(\s+))ko([^\w]|$|^(\s+)))"
    AGONIST = r"(?i)(([^\w]|$|^)agonis[tm])"
    ANTAGONIST = r"(?i)(([^\w]|$|^(\s+))antagonis[tm])"
    OPTOGENETICS = r"(?i)(optogenetic)"
    PET = r"(?i)(positron\s+emission\s+tomography)|(([^\w]|$|^(\s+))pet([^\w]|$|^(\s+)))"
    STAINING = r"(?i)([^\w]|$|^(\s+))(immuno)?(-)?stain"
    STIMULATION = r"(?i)((elec[a-zA-Z]+?)|\(?hz\)?|deep\s+brain)([^\w]|$|^(\s+))stimulat"
    KNOCKDOWN = r"(?i)knockdown"
    IMMUNOHISTOCHEMISTRY = r"(?i)(immuno)(-|\s+)?(histo)(-|\s+)?(chem)"

class ReceptorPrefix(Enum):
    _5HT = r"(?i)5(-)?ht|(serotonin)"
    NONE = ""
class ReceptorFamily(Enum):
    _1 = r"(?i)1"
    _2 = r"(?i)2"
    _3 = r"(?i)3"
    _4 = r"(?i)4"
    _5 = r"(?i)5"
    _6 = r"(?i)6"
    _7 = r"(?i)7"
    NONE = ""
class ReceptorSubtype(Enum):
    a = r"(?i)a"
    b = r"(?i)b"
    c = r"(?i)c"
    d = r"(?i)d"
    e = r"(?i)e"
    f = r"(?i)f"
    NONE = ""
class Receptor:
    #Prefix and family are required, subtype optional. Sometimes occur in form
    #PrefixFamily(Sub1/Sub2) -> two different receptors
    def __init__(self):
        self.pre = ReceptorPrefix.NONE
        self.fam = ReceptorFamily.NONE
        self.sub = ReceptorSubtype.NONE
    def __str__(self):
        return (self.pre.value.replace("(-)?","").replace("|(serotonin)", "") + self.fam.value + self.sub.value).replace("(?i)","")


