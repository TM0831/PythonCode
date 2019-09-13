import time
import random
import requests
from lxml import etree


headers = {
    "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}


def is_chinese(word):
    # 判断是不是中文
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def get_page(url):
    # 请求页面
    time.sleep(random.randint(1, 4))
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    # 解析网页
    et = etree.HTML(res.text)
    text_list = et.xpath('//*[@id="article"]/div/p/span/text()')
    result = []
    for text in text_list:
        if is_chinese(text[0]):
            pass
        else:
            if text[1] == "：":
                result.append(text.split("：")[1])
            else:
                result.append(text.split(":")[1])
    # print("\n".join(result))
    save_text(result)


def save_text(text):
    # 保存结果
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(text))


def crawl_main():
    # 爬取主函数
    start_url = "https://baijiahao.baidu.com/s?id=1608464841941419175&wfr=spider&for=pc"
    get_page(start_url)


if __name__ == "__main__":
    crawl_main()
