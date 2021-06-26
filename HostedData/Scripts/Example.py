import Lib,requests
from Lib import Tools, Decorators

Lib.Register("EXAMPLE",__name__)

# @Lib.Decorators.OnJoin
# def join(addr,username):
#     Lib.Tools.Console.Warn("Hi")

@Lib.Decorators.Execute
def myfunc(addr):
    return "It Works","Shell",False,Tools.Status.SUCCESS

@Lib.Decorators.Custom
def pog(addr):
    return "Champ","Shell",False,Tools.Status.SUCCESS

@Lib.Decorators.Custom
def google(addr):
    url = "http://example.com"
    r = requests.get(url, allow_redirects=True)
    return r.content,"example.html",True,Tools.Status.NEXTPACKET

print(Lib.GlobalData.Data)