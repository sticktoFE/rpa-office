from pathlib import Path
from langchain.utilities import BingSearchAPIWrapper
from ai_assistant.agent.browser import search_not
from ai_assistant.configs.model_config import BING_SEARCH_URL, BING_SUBSCRIPTION_KEY
import requests, re, json, io, base64, os, time
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image, PngImagePlugin
from langchain.docstore.document import Document

from general_spider.utils import web_driver_manager


# 抽取每天新闻的信息并结构化
def extract_news_info(news):
    news_info = {}
    news_info["date"] = news["date"]
    news_info["title"] = news["title"]
    news_info["content_fragment"] = news["body"]
    # content = self.get_news_content(news["url"])["content"]
    # content = re.sub("[^a-zA-Z\u4e00-\u9fa5]", " ", content)
    # news_info["content"] = content
    news_info["url"] = news["url"]
    news_info["source"] = news["source"]
    return news_info


def duckduck_go_search(keyword, result_len=3):
    driver = web_driver_manager.get_driver_ChromeDriver()
    driver.get(
        quote(
            f"https://duckduckgo.com/?q={str(keyword)}&va=v&t=ha&df=w&iar=news&ia=news",
            safe="/:?=.",
        )
    )
    for i in range(0, 20000, 350):
        time.sleep(0.1)
        driver.execute_script("window.scrollTo(0, %s)" % i)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all(class_="b_algo")
    relist = []
    for items in item_list:
        item_prelist = items.find("h2")
        item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_prelist))
        href_s = item_prelist.find("a", href=True)
        href = href_s["href"]
        relist.append([item_title, href])
    item_list = soup.find_all(class_="ans_nws ans_nws_fdbk")
    for items in item_list:
        for i in range(1, 10):
            item_prelist = items.find(
                class_=f"nws_cwrp nws_itm_cjk item{i}", url=True, titletext=True
            )
            if item_prelist is not None:
                url = item_prelist["url"].replace("\ue000", "").replace("\ue001", "")
                title = item_prelist["titletext"]
                relist.append([title, url])
    return relist
    ddgs_news_gen = ddgs.news(text, safesearch="off", timelimit="w", region="zh-cn")
    n = 0
    for onenew in ddgs_news_gen:
        n = n + 1
        if n <= result_len:
            yield Document(
                page_content=onenew["body"] if "body" in onenew.keys() else "",
                metadata={
                    "url": onenew["url"] if "url" in onenew.keys() else "",
                    "title": onenew["title"] if "title" in onenew.keys() else "",
                    "source": onenew["source"] if "source" in onenew.keys() else "",
                },
            )
        else:
            break


def search_web(keyword):
    driver = web_driver_manager.get_driver_ChromeDriver()
    driver.get(quote("https://cn.bing.com/search?q=" + str(keyword), safe="/:?=."))
    for i in range(0, 20000, 350):
        time.sleep(0.1)
        driver.execute_script("window.scrollTo(0, %s)" % i)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all(class_="b_algo")
    relist = []
    for items in item_list:
        item_prelist = items.find("h2")
        item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_prelist))
        href_s = item_prelist.find("a", href=True)
        href = href_s["href"]
        relist.append([item_title, href])
    item_list = soup.find_all(class_="ans_nws ans_nws_fdbk")
    for items in item_list:
        for i in range(1, 10):
            item_prelist = items.find(
                class_=f"nws_cwrp nws_itm_cjk item{i}", url=True, titletext=True
            )
            if item_prelist is not None:
                url = item_prelist["url"].replace("\ue000", "").replace("\ue001", "")
                title = item_prelist["titletext"]
                relist.append([title, url])
    return relist


def ext_zhihu(url):
    if "/answer" in url:
        rep = url.replace("https://www.zhihu.com/question/", "")
        rep_l = rep[rep.rfind("/answer") :][7:]
        rep = "https://www.zhihu.com/question/" + rep.replace("/answer" + rep_l, "")
        return rep
    else:
        return url


def search_zhihu_que(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all(class_="List-item")
    relist = []
    for items in item_list:
        item_prelist = items.find(
            class_="RichText ztext CopyrightRichText-richText css-1g0fqss"
        )
        item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_prelist))
        relist.append(item_title)
    return relist


def search_zhihu_zhuanlan(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find(class_="RichText ztext Post-RichText css-1g0fqss")
    item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list))
    return item_title


def search_baike(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    if "baike.sogou.com" in url:
        r = requests.get(url, headers=headers)
        html_s = r.text
        soup_s = BeautifulSoup(html_s, "html.parser")
        item_list_s = soup_s.find(class_="lemma_name")
        item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list_s))
        item_title = item_title.replace("编辑词条", "")
        r = requests.get(
            "https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="
            + item_title
            + "&bk_length=600",
            headers=headers,
        )
        resp = r.text.encode("utf-8").decode("gbk")
        resp_json = json.loads(resp)
        answer = resp_json.get("abstract")
        if answer == None:
            answer_f = soup_s.find(class_="abstract")
            item_title = re.sub(r"(<[^>]+>|\s)", "", str(answer_f))
            return item_title
        else:
            return resp_json.get("abstract")
    else:
        r = requests.get(
            "https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="
            + url
            + "&bk_length=600",
            headers=headers,
        )
        resp = r.text.encode("utf-8").decode("gbk")
        resp_json = json.loads(resp)
        answer = resp_json.get("abstract")
        return answer


def search_wx(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find(class_="rich_media_wrp")
    item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list))
    return item_title


def search_news_sohu(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find(class_="article")
    item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list))
    return item_title


def search_news_163(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find(class_="post_body")
    item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list))
    return item_title


def search_bilibili(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find(class_="article-content")
    item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list))
    return item_title


def search_csdn(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find(class_="article_content clearfix")
    item_title = re.sub(r"(<[^>]+>|\s)", "", str(item_list))
    return item_title


def get_config():
    with open(f"{Path(__file__).parent.parent}/configs/config.json") as f:
        return json.load(f)


def search_github(keyword):
    token = get_config().get("Web").get("git_token")
    if not token == None:
        headers = {"Authorization": "token " + str(token)}
    else:
        headers = {}
    new_key = ""
    for ch in keyword:
        if not "\u4e00" <= ch <= "\u9fff":
            new_key += ch
    url = quote(
        "https://api.github.com/search/repositories?q=" + str(new_key) + "&order=desc",
        safe="/:?=.&",
    )
    r = requests.get(url, headers=headers)
    resp_json = json.loads(r.text)
    items = resp_json.get("items")
    items = items[0:1]
    item_json = json.dumps(items[0])
    item_json = json.loads(str(item_json))
    addr = item_json.get("full_name")
    url = quote("https://api.github.com/repos/" + str(addr) + "/readme", safe="/:?=.&")
    r = requests.get(url, headers=headers)
    repo_json = json.loads(r.text)
    readme = repo_json.get("download_url")
    r = requests.get(
        str(readme).replace(
            "https://raw.githubusercontent.com/", "https://raw.fastgit.org/"
        ),
        headers=headers,
    )
    relist = [addr, r.text]
    return relist


def test_if_url_ignore(test_url):
    for url in get_config().get("Web").get("ignore_url"):
        if url in test_url:
            return True
    return False


def search_main(item, feature):
    web_list = search_web(item)
    return_list = []
    flist = []
    print(feature)
    # print(web_list)
    if "百科" in feature:
        ans = str(search_baike(item))
        if not ans == "":
            return_list.append(ans)
    if "GitHub" in feature:
        githubresp = search_github(item)
        ans = githubresp[1]
        if not ans == "":
            return_list.append(ans)
            flist.append("https://github.com/" + githubresp[0])
    for items in web_list:
        if "zhihu.com/question/" in items[1] and "知乎回复" or "All(Preview)" in feature:
            return_list.append(str(search_zhihu_que(ext_zhihu(items[1]))))
            flist.append(items[1])
        if "baike.sogou.com" in items[1] and "百科" or "All(Preview)" in feature:
            return_list.append(str(search_baike(items[1])))
            flist.append(items[1])
        if "mp.weixin.qq.com" in items[1] and "微信公众号" or "All(Preview)" in feature:
            return_list.append(str(search_wx(items[1])))
            flist.append(items[1])
        if "zhuanlan.zhihu.com" in items[1] and "知乎专栏" or "All(Preview)" in feature:
            return_list.append(str(search_zhihu_zhuanlan(items[1])))
            flist.append(items[1])
        if "163.com/dy/article/" in items[1] and "新闻" or "All(Preview)" in feature:
            return_list.append(str(search_news_163(items[1])))
            flist.append(items[1])
        if "sohu.com/a/" in items[1] and "新闻" or "All(Preview)" in feature:
            return_list.append(str(search_news_sohu(items[1])))
            flist.append(items[1])
        if "bilibili.com/read/" in items[1] and "B站专栏" or "All(Preview)" in feature:
            return_list.append(str(search_bilibili(items[1])))
            flist.append(items[1])
        if "blog.csdn.net" in items[1] and "CSDN" or "All(Preview)" in feature:
            return_list.append(str(search_csdn(items[1])))
            flist.append(items[1])
        if "All(Preview)" in feature:
            if (
                not "zhihu.com/question/"
                or not "baike.sogou.com"
                or not "mp.weixin.qq.com"
                or not "zhuanlan.zhihu.com"
                or not "163.com/dy/article/"
                or not "sohu.com/a/"
                or not "bilibili.com/read/"
                or not "blog.csdn.net" in items[1]
            ):
                if not test_if_url_ignore(items[1]):
                    ans = search_not(items[1])
                    if ans is not None:
                        return_list.append(ans)
                        flist.append(items[1])
    return [flist, return_list]


if __name__ == "__main__":
    results = search_web("银行产品")
    print(results)
