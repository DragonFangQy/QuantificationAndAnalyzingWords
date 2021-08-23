from hashlib import md5

import requests


class Word(object):
    def __init__(self, word, word_means=[]):
        self.word = word
        self._word_means = word_means

        self.get_word_means()

    @property
    def word_means(self):
        return self._word_means

    @staticmethod
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def get_word_means(self):
        headers = {
            "Host": "fanyi.baidu.com"
            , "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0     "
            , "Accept": "*/*"
            , "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
            , "Accept-Encoding": "gzip, deflate, br"
            , "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8  "
            , "Origin": "https://fanyi.baidu.com"
            , "Connection": "keep-alive"
            ,
            "Cookie": "BAIDUID=A989AE06769E67B0C02E1456CC82426E:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1627606976; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1627607065; __yjs_duid=1_5ff3fa948460575c29e23101d136ea751627606976041; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_Y2VkNGZkMjQzNmQ2ZDBkMGE1OGExYjM1OTFhYTNiYWQ1ZGM4YTI5YTMyNzYzMDhjYzQyYzgwYjk1MGQ5ZTJlMjEyN2Y0Y2NlZWUwZDk5ZTExYmRiOTBjNmRmMzY3ZWM0MzQwZGEzMDA5NmU5ZmI4ZmJjYjI1NjI4MjdkMThkNmExMjQ3NmE4NGRiNDgwYWM4Yzk2NWUxNGM1NWJlMmQ3Ng==; __yjs_st=2_ODJlMDQ5ZTUxOWZkYTYzZTZiMTAwNzE0N2YwNTExZWI1NTFiMGUyOTJlMGZmOWEzY2NkM2MwNWFiYWY0NjZlM2IwNzk2MmRlOTkwMDZlYWZiZjYyNWE2ZTEwNzhhZTRiZGVkNzU0ZjAyZGE4OTBjYzA3OWQxNWIxMWVhM2IxMjdmM2Q4MzE0MTkyZTVhZWQ1NDVmMmM4NmRkZTk5NmI0ODEzMzNhMjcwN2RmNjYzOTFlY2Q0OWExZjdkYWUyOTg0NjQ4NjZlNDNjYmQ4NjliOTMzNTlhZWNkZjY0ZTUzZDIzODgzMGNmNTg3MjUwNGRhY2E1OTQyYWIxYTBkNTA1NV83XzJkYzMzYjRm"
            , "Content-Length": "116"
            , "Pragma": "no-cache"
            , "Cache-Control": "no-cache"
        }

        data = {
            "from": "en"
            , "to": "zh"
            , "query": "clear"
            , "simple_means_flag": "3"
            , "sign": "50105.270472"
            , "token": "29344f3b138d76b53ad6532849e35ba8"
            , "domain": "common"
        }
        result = requests.post("https://fanyi.baidu.com/v2transapi?from=en&to=zh", data=data, headers=headers)

        self._word_means.extend(list(
            set(result.json()["dict_result"]["simple_means"]["word_means"]) | set(result.json()["liju_result"]["tag"])))


if __name__ == '__main__':
    word_ = Word("American")
    # word_.get_word_means()
    word_.word_means = 'nihni'
    print(word_.word_means)
