from __future__ import unicode_literals
#reference : http://www.richyli.com/name/index.asp
raw_data = open("raw_name")
d = dict()
for i in raw_data:
    d["People"] = i.split("、")


import json

import codecs
fp = codecs.open('output.txt', 'a+', 'utf-8')
fp.write(json.dumps(d,ensure_ascii=False))
fp.close()
