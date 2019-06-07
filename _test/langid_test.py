from langid import langid

s1 = '中文'
s2 = 'contenders'
s3= 'こにちは'
s4 = '規定'
s5 = '上げる'
s6 = '寝る'
l=[]
l.append(langid.classify(s1))
l.append(langid.classify(s2))
l.append(langid.classify(s3))
l.append(langid.classify(s4))
l.append(langid.classify(s5))
l.append(langid.classify(s6))
print('https://sp1.baidu.com/5b11fzupBgM18t7jm9iCKT-xh_/sensearch/selecttext?cb=jQuery110205234840516971939_1540970393811&q=content')