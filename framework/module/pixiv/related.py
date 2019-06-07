from framework.core.crawlercore.url import PageUrl


class PixivRelatedUrl(PageUrl):
    def get_url(self, sortdict_key="default"):
        return "https://www.pixiv.net/illust_recommendation.php?illust_id="+self.request_key_param+"&p="+str(self.offset)