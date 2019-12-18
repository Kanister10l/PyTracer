import json
import re
from pprint import pprint

class LangEngine(object):
    language = None
    moves = None

    def InitEngine(self, lang_location):
        self.language = json.load(open(lang_location, "r"))
        self.moves = []
    def ReplaceVariable(self, handler, code, var, val):
        if var in handler["variables"] and val is not None:
            code = code.replace("%" + var, var + str(val))
        else:
            code = code.replace("%" + var, "")
        return code

    def ClearUnused(self, handler, code):
        for var in handler["variables"]:
            code = code.replace("%" + var, "")
        code = re.sub('\s+', ' ', code).strip()
        return code

    def ClearCode(self):
        self.moves = []

    def PrintCode(self):
        for move in self.moves:
            print(move)
    
    def SaveCode(self, location):
        f = open(location, "w")
        for move in self.moves:
            f.write(move)
        f.flush()
        f.close()

    def LinearMove(self, x=None, y=None, z=None):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "linear_move"][0]
        except:
            print("ERROR: Missing linear move handler")
            return
        output = handler["translation"]
        output = self.ReplaceVariable(handler, output, "X", x)
        output = self.ReplaceVariable(handler, output, "Y", y)
        output = self.ReplaceVariable(handler, output, "Z", z)
        output = self.ClearUnused(handler, output)
        self.moves += [output]
    
    def RapidMove(self, x=None, y=None, z=None):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "rapid_move"][0]
        except:
            print("ERROR: Missing rapid move handler")
            return
        output = handler["translation"]
        output = self.ReplaceVariable(handler, output, "X", x)
        output = self.ReplaceVariable(handler, output, "Y", y)
        output = self.ReplaceVariable(handler, output, "Z", z)
        output = self.ClearUnused(handler, output)
        self.moves += [output]
    
    def Pause(self, p=None):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "pause"][0]
        except:
            print("ERROR: Missing pause handler")
            return
        output = handler["translation"]
        output = self.ReplaceVariable(handler, output, "P", p)
        output = self.ClearUnused(handler, output)
        self.moves += [output]

    def Home(self, x=None, y=None, z=None):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "home"][0]
        except:
            print("ERROR: Missing home handler")
            return
        output = handler["translation"]
        output = self.ReplaceVariable(handler, output, "X", x)
        output = self.ReplaceVariable(handler, output, "Y", y)
        output = self.ReplaceVariable(handler, output, "Z", z)
        output = self.ClearUnused(handler, output)
        self.moves += [output]

    def SetMilimeters(self):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "set_milimeters"][0]
        except:
            print("ERROR: Missing set milimeters handler")
            return
        output = handler["translation"]
        output = self.ClearUnused(handler, output)
        self.moves += [output]
    
    def SetAbsolute(self):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "set_absolute"][0]
        except:
            print("ERROR: Missing set absolute handler")
            return
        output = handler["translation"]
        output = self.ClearUnused(handler, output)
        self.moves += [output]

    def SetRelative(self):
        handler = None
        try:
            handler = [lang for lang in self.language["commands"] if lang["handler"] == "set_relative"][0]
        except:
            print("ERROR: Missing set relative handler")
            return
        output = handler["translation"]
        output = self.ClearUnused(handler, output)
        self.moves += [output]