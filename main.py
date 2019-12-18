from LangEngine import LangEngine

if __name__ == "__main__":
    engine = LangEngine()
    engine.InitEngine("config/lang.json")
    engine.RapidMove(x=1, y=2, z=2)
    engine.LinearMove(x=1, y=2, z=2)
    engine.Home(x=1.5, y=2, z=2)
    engine.Pause(p=10)
    engine.SetMilimeters()
    engine.SetAbsolute()
    engine.SetRelative()
    engine.SaveCode("")