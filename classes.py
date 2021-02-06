class Mod:
    def __init__(self, name):
        self.name = name
        self.namespaces = []
    
    def AddNamespace(self, n):
        self.namespaces.append(n)

    def GenerateTextFile(self):
        out = ""
        out += self.NamespacesToTextHeader()
        out += self.NamespacesToText()
        return out

    def GenerateLangFile(self):
        out = "l_english:\n\n"
        for namespace in self.namespaces:
            out += namespace.EventsToLang()
        return out

    def NamespacesToTextHeader(self):
        out = ""
        for namespace in self.namespaces:
            out += "add_namespace = " + namespace.name + "\n"
        out += "\n"
        return out
    
    def NamespacesToText(self):
        out = ""
        for namespace in self.namespaces:
            out += "#EVENTS IN NAMESPACE '" + namespace.name + "'\n\n"
            out += namespace.EventsToText()
        return out
    


class Namespace:
    def __init__(self, name):
        self.name = name
        self.events = []
    
    def EventsToText(self):
        out = ""
        id = 0
        for event in self.events:
            out += event.EventToText(id)
            id += 1
        return out

    def EventsToLang(self):
        out = ""
        id = 0
        for event in self.events:
            out += event.EventToLang(id)
            id += 1
        return out


class Event:
    def __init__(self, namespace, eventType, title, desc, picture=None, option=None, fire_only_once=False, is_triggered_only=False, hidden=False, trigger=None):
        namespace.events.append(self)
        self.name = title
        self.desc = desc
        self.trigger = trigger if trigger != None else {}
        #this namespace is just a string
        self.namespace = namespace.name
        #types: country, news, unit_leader, state
        self.type = eventType
        self.options = []
        self.picture = picture
        self.fire_only_once = fire_only_once
        self.is_triggered_only = is_triggered_only
        self.hidden = hidden

    def EventToText(self, idInt):
        id = self.namespace + "." + str(idInt)
        
        out = "#" + self.name + "\n" + self.type + "_event = {\n"
        
        #required fields
        out += "\tid = " + id + "\n"
        out += "\ttitle = " + id + ".t #" + self.name + "\n"
        out += "\tdesc = " + id + ".d #" + self.desc + "\n"

        #optional fields
        out += "\tpicture = " + self.picture + "\n" if self.picture else ""
        out += "\tis_triggered_only = yes\n" if self.is_triggered_only else ""
        out += "\tfire_only_once = yes\n" if self.fire_only_once else ""
        out += "\thidden = yes\n" if self.hidden else ""

        #triggers
        if(len(self.trigger) > 0):
            out += "\ttrigger = {\n"
            for t in self.trigger:
                out+= "\t\t" + t + " = " + self.trigger[t]
            out += "\n\t}\n"
        else:
            out += "\ttrigger = {}\n"

        out += self.OptionsToText(id)

        out += "\n}\n\n"
        return out

    def EventToLang(self, idInt):
        id = self.namespace + "." + str(idInt)
        
        #required fields
        out = id + ".t:0 \"" + self.name + "\"\n"
        out += id + ".d:0 \"" + self.desc + "\"\n"

        out += self.OptionsToLang(id)

        out+= "\n"

        return out

    def OptionsToText(self, id):
        out = ""
        charID = 97
        for option in self.options:
            optionID = id + "." + chr(charID)
            out += option.OptionToText(optionID)
            charID += 1

        return out

    def OptionsToLang(self, id):
        out = ""
        charID = 97
        for option in self.options:
            optionID = id + "." + chr(charID)
            out += option.OptionToLang(optionID)
            charID += 1
        out += "\n"
        return out

class Option:
    #trigger and effects should both be dicts
    def __init__(self, name, trigger=None, ai_chance=1, original_recipient_only=False, effects=None):
        self.name = name
        self.trigger = trigger if trigger != None else {}
        self.ai_chance = str(ai_chance)
        self.original_recipient_only=original_recipient_only
        self.effects= effects if effects != None else {}
    def OptionToText(self, id):
        out = "\toption = {\n"
        out+= "\t\tname = " + id + " #" + self.name + "\n"
        out+= "\t\tai_chance = { factor = " + self.ai_chance + " }\n"

        #triggers
        if(len(self.trigger) > 0):
            out += "\t\ttrigger = {\n"
            for t in self.trigger:
                out+= "\t\t\t" + t + " = " + self.trigger[t]
            out += "\n\t\t}\n"
        else:
            out += "\t\ttrigger = {}\n"

        #optional  
        out+= "\t\toriginal_recipient_only = yes\n" if self.original_recipient_only else ""
        
        #effects
        if(len(self.effects) > 0):
            out += "\t\teffect = {\n"
            for e in self.effects:
                out+= "\t\t\t" + e + " = " + self.effects[e]
            out += "\n\t\t}"
        out+="\n\t}"
        return out
    
    def OptionToLang(self, id):
        return id + ":0 \"" + self.name + "\""