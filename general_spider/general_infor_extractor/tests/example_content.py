import json
import glob
import chardet

import requests
from general_infor_extractor import GeneralNewsExtractor
from myutils.info_out_manager import dump_json_table, get_temp_folder

out_folder = get_temp_folder(des_folder_path=__file__, is_clear_folder=True)


def test_content_from_html(
    files_path="mytools/general_infor_extractor/tests/content/**/*.html",
):
    html_list = glob.glob(files_path, recursive=True)
    for html_file in html_list:
        with open(html_file, encoding="utf-8") as f:
            html = f.read()
        extractor = GeneralNewsExtractor()
        result = extractor.extract(
            html,
            host="https://www.xxx.com",
            # body_xpath='//div[@class="show_text"]',
            noise_node_list=[
                '//div[@class="comment-list"]',
                '//*[@style="display:none"]',
                '//div[@class="statement"]',
            ],
            use_visiable_info=False,
        )
        print(f">>>>>>>>>>>>>{html_file}>>>>>>>>>>>>>")
        # print(json.dumps(result, indent=2, ensure_ascii=False))
        dump_json_table(result, f"{out_folder}/bank_news.json")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


def test_content_from_url(url):
    response = requests.get(url)
    response.encoding = chardet.detect(response.content)["encoding"]
    html = response.text
    extractor = GeneralNewsExtractor()
    result = extractor.extract(
        html,
        host="https://www.xxx.com",
        # body_xpath='//div[@class="show_text"]',
        noise_node_list=[
            '//div[@class="comment-list"]',
            '//*[@style="display:none"]',
            '//div[@class="statement"]',
        ],
        use_visiable_info=False,
    )
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    dump_json_table(result, f"{out_folder}/bank_news.json")


if __name__ == "__main__":
    test_content_from_url(
        "https://finance.sina.com.cn/roll/2023-05-18/doc-imyuenya8398648.shtml"
    )
