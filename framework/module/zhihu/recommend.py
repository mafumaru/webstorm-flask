from framework.core.crawlercore.parse import JsonParseStrategy
from framework.core.crawlercore.request import SingleRequest
from framework.core.crawlercore.url import Url


class ZhihuRecommendUrl(Url):
    def get_url(self, sortdict_key="default"):
        return "https://api.zhihu.com/topstory/recommend?action=down&scroll=up&limit=10&start_type=cold"


class ZhihuRecommendParseStrategy(JsonParseStrategy):
    def parse(self):
        return self.parser['data']


class ZhihuRecommend(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = ZhihuRecommendUrl()
        self.parse_strategy = ZhihuRecommendParseStrategy()
        self.headers = {'x-api-version': '3.0.95', 'cache_temp_json': 'true',
                        'x-ad-styles': 'brand_card_article=4;brand_card_article_multi_image=5;brand_card_article_video=4;brand_card_multi_image=2;brand_card_normal=3;brand_card_question=4;brand_card_question_multi_image=5;brand_card_question_video=4;brand_card_video=2;brand_feed_active_right_image=6;brand_feed_hot_small_image=1;brand_feed_small_image=3;plutus_card_image=13;plutus_card_image_30=2;plutus_card_image_31=1;plutus_card_image_31_download=1;plutus_card_image_8=1;plutus_card_image_8_download=5;plutus_card_multi_images=5;plutus_card_multi_images_30=5;plutus_card_multi_images_30_download=3;plutus_card_multi_images_8=1;plutus_card_multi_images_8_download=1;plutus_card_small_image=5;plutus_card_small_image_8=1;plutus_card_small_image_8_download=1;plutus_card_video=5;plutus_card_video_30=3;plutus_card_video_8=4;plutus_card_video_8_download=4;plutus_card_window=2;plutus_card_window_8=2;plutus_card_word=4;plutus_card_word_30=2;plutus_card_word_30_download=3;plutus_card_word_8=1;plutus_card_word_8_download=1;plutus_card_image_30_download=4;plutus_card_slide_image_30=3;plutus_card_slide_image_30_download=3;plutus_card_slide_image_31=1;plutus_card_slide_image_31_download=1;plutus_card_slide_image_8=3;plutus_card_slide_image_8_download=1;plutus_card_video_30_download=4',
                        'User-Agent': 'com.zhihu.android/Futureve/5.30.3 Mozilla/5.0 (Linux; Android 5.1; m1 metal Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.146 Mobile Safari/537.36',
                        'x-app-version': '5.30.3',
                        'x-app-za': 'OS=Android&Release=5.1&Model=m1+metal&VersionName=5.30.3&VersionCode=1002&Product=com.zhihu.android&Width=1080&Height=1920&Installer=%E9%AD%85%E6%97%8F%E5%BA%94%E7%94%A8%E5%95%86%E5%BA%97&DeviceType=AndroidPhone&Brand=Meizu',
                        'x-app-flavor': 'meizu', 'x-app-build': 'release', 'x-network-type': 'WiFi',
                        'X-ZST-82': '1.0ANDgwbYgkA4MAAAASwUAADEuMDTc91sAAAAAs_g_Ekqo5eazPOvTkUB5kt1PdI0=',
                        'x-udid': 'AADhBiGe7gxLBRpED6VCzidmUci2ZciRLiw=',
                        'Authorization': 'Bearer gt2.0AAAAAAck18AM7p4hBuEAAAAAAAxNVQJgAgD106JaTaaqyi-GkDhOTsKDpNYx1Q==',
                        'Host': 'api.zhihu.com', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
