from extraction.main import parse_receptors
import re
import string
def clean(path, out_file):
    printable = string.printable
    with open(path, 'r') as f:
        with open(out_file, 'w+') as o:
            lines = f.readlines()
            for line in lines:
                tags = list(parse_receptors(line))
                tags = sorted(tags, key=lambda x: x[1], reverse=True)
                res = line
                for recept, start, end in tags:
                    res = res[:start] + ' ' + recept + ' ' + res[end+1:]

                res = ''.join(filter(lambda x: x in printable, res))
                res = re.sub('[^\w\s]|_', '', res)
                o.write(res)



if __name__ == "__main__":
    clean('../data/Serotonin2020.txt', '../data/Serotonin2020_postprocessed.txt')