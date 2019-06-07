import hashlib
# appkey
# 6f90a59ac58a4123
# appsecret
# 0bfd84cc3940035173f35e6777508326

src='aid=21989705&appkey=6f90a59ac58a4123&build=591181&from=3&mobi_app=android&plat=0&platform=android&ts=15501053950bfd84cc3940035173f35e6777508326'
m2 = hashlib.md5()
m2.update(src.encode('utf-8'))
print(m2.hexdigest())