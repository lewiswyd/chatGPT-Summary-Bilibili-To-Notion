import requests
from bili_video_info_downloader.section_info import section_dict


class VideoInfoDownloader:
    def __init__(self, bv_id: str, cookie: str) -> None:
        self.bv_id = bv_id
        self.info_api = "https://api.bilibili.com/x/web-interface/view"
        self.tags_api = "https://api.bilibili.com/x/web-interface/view/detail/tag"
        self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Cookie': cookie
        }


    def _get_info(self):
        params = (
            ('bvid', self.bv_id),
        )
        response = requests.get(self.info_api, headers=self.headers, params=params)
        return response.json()['data']


    def _get_tags(self):
        params = (
            ('bvid', self.bv_id),
        )

        response = requests.get(self.tags_api, headers=self.headers, params=params)
        data = response.json()['data']
        if data:
            tags = [x['tag_name'] for x in data]
            if len(tags) > 5:
                tags = tags[:5]
        else:
            tags = []
        return tags
    

    def download_video_info(self):
        info = self._get_info()
        tags = self._get_tags()
        section = section_dict[info['tid']]
        return {
            "info": info,
            "tags": tags,
            "section": section,
            "bvid": self.bv_id
        }
