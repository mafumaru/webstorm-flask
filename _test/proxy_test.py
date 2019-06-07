# https://www.youtube.com/watch?v=vjF9GgrY9c0
import requests

url = 'https://www.youtube.com/watch?v=vjF9GgrY9c0'
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
# url = 'https://www.youtube.com/comment_service_ajax?action_get_comment_replies=1&pbj=1&ctoken=EiYSC3ZqRjlHZ3JZOWMwwAEAyAEA4AEBogINKP___________wFAABgGMk8aTRIaVWd6SHhBODlhc3dsMEY1emJkRjRBYUFCQWciAggAKhhVQzR6eW9JQXptZHNncERaUWZPMS1sU0EyC3ZqRjlHZ3JZOWMwOABAAUgK&continuation=EiYSC3ZqRjlHZ3JZOWMwwAEAyAEA4AEBogINKP___________wFAABgGMk8aTRIaVWd6SHhBODlhc3dsMEY1emJkRjRBYUFCQWciAggAKhhVQzR6eW9JQXptZHNncERaUWZPMS1sU0EyC3ZqRjlHZ3JZOWMwOABAAUgK&itct=CO8BEMm3AiITCL7GkOfSnt0CFYa51Qodjw4I2w%3D%3D'
# url = 'https://twitter.com/HARUTYA1226/status/1036133716962115584?conversation_id=1036133716962115584'
r = requests.get(url,headers=headers).text

# proxy = {
#     "http": "http://localhost:1080",
#     "https": "https://localhost:1080"
# }
#
# url = 'https://www.youtube.com/watch?v=vjF9GgrY9c0'
# r = requests.get(url, proxies=proxy).text

print('end')