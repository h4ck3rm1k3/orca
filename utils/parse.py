import re
import formatting_consts
f = open ('formatting_data.py')

for l in f.readlines():
    l = formatting_consts.replace(l)
    print (l)

# #    if l.find(':') >0 :
# #        pass
# #    else:
# #    if l.find('#add') >0 :
#     l = re.findall(r'\'(\w+)\'',l)
#     for g in l :
#         n = g.upper()
#         v = g
# #        print("STR_%s = '%s'" % (n,v))
#             #print (l)
