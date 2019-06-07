from framework.module.twitter.iframe import TwitterIframe

iframe = TwitterIframe()
iframe.init('1053967525199851525')
data = iframe.get_data()
print('')