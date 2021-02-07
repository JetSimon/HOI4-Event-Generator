import os,io

def IntToBool(n):
    return False if n == 0 else True

def GetNamesAsList(l):
    out = []
    for i in l:
        out.append(i.name)
    return out

def SaveMod(mod):
    with open("mods/"+mod.name + '.txt', 'w') as fp:
        fp.write(mod.GenerateTextFile())

    with open("mods/"+mod.name + '.yml', 'w') as fp:
        fp.write(mod.GenerateLangFile())

def FindObjectWithName(name, namespaces):
    print(name)
    for n in namespaces:
        if(n.name == name):
            print("FOUND " + name)
            return n
    return None