import logging
import time
from configparser import ConfigParser

import requests
from myutils.image_convert import get_shot_bytes
# 3、通过IP访问独立服务器
class OCRRequestNet:
    def upload_ocr_info_ip(self, qPixmap):
        shot_bytes = get_shot_bytes(qPixmap)
        filename = "shot" + str(time.time()).split('.')[0] + '.jpg'
        files = {"file": (filename, shot_bytes, "image/jpeg")}
        cfg = ConfigParser()
        cfg.read('config.ini')
        headers = {"Cookie": cfg.get("picbed", 'cookie')}
        try:
            res = requests.post(cfg.get("picbed", 'api'),
                                data={'compress': 960},
                                files=files,
                                headers=headers)
            status_code = res.json()['code']
            if status_code == 200:
                return res.json()['data']['raw_out']
            else:
                logging.information('服务非正常返回', f"not 200, code: {res.status_code}")
        except Exception as e:
            print(e.args)   