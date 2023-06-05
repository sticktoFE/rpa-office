import json
import glob
from general_infor_extractor import GeneralNewsExtractor


if __name__ == "__main__":
    html_list = glob.glob("visiable_test/khan/*.html", recursive=True)
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
            normalize=False,
            use_visiable_info=True,
        )
        print(f">>>>>>>>>>>>>{html_file}>>>>>>>>>>>>>")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
