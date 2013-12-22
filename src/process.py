from orca.formatting_braille_data import load_data

d = load_data()
for num in d:
    for action in d[num]:
        code = d[num][action]
        print "def action_%s_%s ():\n\treturn %s" % (num, action, code)
        print "action_%s_%s ()\n" % (num, action)
