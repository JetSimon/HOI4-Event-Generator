import os,io
import tkinter as tk

# mod = Mod("TEST")

# namespace = Namespace("testspace")

# e = Event(namespace, "country", "test event", "test desc", "GFX_TEST")

# o = Option("OPTION", effects={"promote_leader":"yes"}, trigger={"promote_leader":"yes"})

# e.options.append(o)

# e2 = Event(namespace, "news", "test event 2", "test desc 2", "GFX_TEST_2", None, True, True, trigger={"test":"yessir"})

# mod.AddNamespace(namespace)

def GetNamesAsList(l):
    out = []
    for i in l:
        out.append(i.name)
    return out

def SaveMod(mod):
    with open(mod.name + '.txt', 'w') as fp:
        fp.write(mod.GenerateTextFile())

    with open(mod.name + '.yml', 'w') as fp:
        fp.write(mod.GenerateLangFile())

def FindObjectWithName(name, namespaces):
    print(name)
    for n in namespaces:
        if(n.name == name):
            print("FOUND " + name)
            return n
    return None