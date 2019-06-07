import re


class ZhihuAnswerTool():
    @classmethod
    def clear_details(cls,str):
        s=re.sub("<img src=\"data:[\s\S]*?hd\.jpg\">","",str)
        s=re.sub("<img","<img class=\"img-responsive\"",s)
        s=re.sub("src=\"data:[\s\S]*?svg&gt;\"","",s)
        s=re.sub("data-actualsrc","src",s)
        s=re.sub("<noscript>","",s)
        s=re.sub("</noscript>","",s)
        s=re.sub("data-caption[\s\S]*?r.jpg\"","",s)
        s=re.sub("data-size[\s\S]*?r.jpg\"","",s)
        s=re.sub("\"<>\"","",s)
        return s