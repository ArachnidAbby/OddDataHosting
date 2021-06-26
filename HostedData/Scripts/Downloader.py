import Lib, requests
Lib.Register("get",__name__)

@Lib.Decorators.Custom
def web(addr, url,file):
    r = requests.get(url, allow_redirects=True)
    return r.content,file,True,Lib.Tools.Status.NEXTPACKET