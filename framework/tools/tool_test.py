str='''Host: docs.google.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://bluesilvertranslations.wordpress.com/2014/12/10/004-otherworldly-tang-sans-first-hidden-weapon/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7
'''
list = str.split('\n')
dict={}
for item in list:
    if item:
        temp = item.index(':')
        dict[item[0:temp]]=item[temp+1:].strip()
print('end')
