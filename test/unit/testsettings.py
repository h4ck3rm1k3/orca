import orca.settings

def myglobals () :
    g = globals()
    for x in g :
        v = g[x]
        print (x,v)

def settings():
    for item in dir(orca.settings):
        if not item.startswith("__"):
            print (item)
            print(getattr(orca.settings,item))
        

settings()
