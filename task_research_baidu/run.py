#coding:utf-8

"""
\b
* * * * * * * * * * * * * * * * * * * * * * * * *
Task to research baidu with your keyword, 
And then save it as pdf on your local device.
Please set proxy info in file `proxy_list.txt`

\b
使用百度搜索关键词, 
然后保存pdf在本地, 
请先在`proxy_list.txt`里配置代理

\b 
Author: Roger;
Python Version: python 3.7+;
Python Libraries:
    click: https://click-docs-zh-cn.readthedocs.io/zh/latest/
    pdfkit: https://pypi.org/project/pdfkit/
* * * * * * * * * * * * * * * * * * * * * * * * *
"""

import click
import datetime
import os
import pdfkit
import threading
import time
from os import path as osp
from urllib.parse import quote_plus


SUCCESS, ERROR, WARNING = 'SUCCESS', 'ERROR', 'WARNING'
def _log(info, directory=None, level=SUCCESS):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('%s - %s - %s' % (level, now, info))
    
    if directory:
        log_path = osp.join(directory, f"_log_{level.lower()}.log")
    else:
        log_path = f"_log_{level.lower()}.log"

    with open(log_path, 'a+') as f:
        f.write('%s %s %s\n' % (level, now, info))


class myThread(threading.Thread):
    def __init__(self, file_prefix, wd, output_dir, types, proxy, debug):
        threading.Thread.__init__(self)
        self.file_prefix = file_prefix
        self.wd = wd
        self.output_dir = output_dir
        self.types = types
        self.proxy = proxy
        self.debug = debug

    def run(self):
        print("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        start2create_pdf(self.file_prefix, self.wd, self.output_dir, self.types, self.proxy, self.debug)
        # 释放锁，开启下一个线程
        threadLock.release()


threadLock = threading.Lock()
threads = []


# Page set
PAGES = [0, 1, 2]

# WKHTMLTOPDF = "/usr/local/bin/wkhtmltopdf"
WKHTMLTOPDF = "wkhtmltopdf"
WEB_URL = "https://www.baidu.com/s?wd={wd}&pn={pn}"
NEWS_URL = "https://www.baidu.com/s?tn=news&word={wd}&pn={pn}"


help_c = __doc__
help_output = "导出的文件夹地址, like: `~/Desktop`"
help_wd = "搜索的关键词, 用英文分号(`;`)分隔"
help_debug = "Debug模式, 不使用pdfkit去拉数据"
help_multi_progress = "多进程模式"


def test_new_file(path):
    with open(path, "a") as f:
        f.write(path)
    return True


def getsize(path):
    """ return float with UNIT `KB` """
    if os.path.exists(path):
        return round(os.path.getsize(path) / 1024, 2)
    else:
        return 0


def real_create_pdf(path, url, proxy, debug):
    """use WKHTMLTOPDF get data"""
    if debug:
        time.sleep(1)
        with open(path, "w") as f:
            f.write(url)
        return True
    pdfkit.from_url(
        output_path=path,
        options={
            '--proxy': f'http://{proxy}',
        },
        url=url
    )
    return True


def start2create_pdf(file_prefix, wd, output_dir, types, proxy, debug):
    """Create Pdf"""
    for _type in types:

        if _type == 'web':
            base_url = WEB_URL
        elif _type == 'news':
            base_url = NEWS_URL

        for page in PAGES:
            this_file_name = f"{file_prefix}_{_type}_({proxy})_page{page+1}.pdf"
            pn = page * 10
            url = base_url.format(wd=wd, pn=pn)
            path = osp.join(output_dir, this_file_name)

            try:
                if os.path.exists(path):
                    _log(f"Exists!! {_type} - {proxy} - [{this_file_name}]", output_dir, WARNING)
                    continue

                real_create_pdf(path, url, proxy, debug)
                fsize = getsize(path)
                _log(f"{_type} - {proxy} - [{this_file_name}] -  {fsize}KB", output_dir)
            except Exception as e:
                _log(f"{_type} - {proxy} - [{this_file_name}] - e: {e}", output_dir, ERROR)

    _log(f"[Process] Pdf creation finished... {_type} - {proxy}.....", output_dir)
    return True


@click.command()
@click.help_option("-h", "--help", help=help_c)
@click.option("-wd", "--keyword", "keywords", help=help_wd, type=str, required=True)
@click.option("-mp", "--multi-progress", "multi_progress", help=help_multi_progress, is_flag=True, default=True)
@click.option("-o", "--output-dir", "output_dir", help=help_output, type=str, default="./OUTPUT")
@click.option("-d", "--debug", "debug", help=help_debug, is_flag=True)
def main(output_dir, keywords, debug, multi_progress):
    today = datetime.datetime.now().strftime('%Y.%m.%d')
    output_dir = osp.join(output_dir, today)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    _log("Start to research .....", output_dir)

    keywords = keywords.split(";")
    for keyword in keywords:

        wd = quote_plus(keyword)
        file_prefix = f"{keyword}-{today}"

        with open("./proxy_list.txt", "r") as f:
            proxy_data = f.read()

            proxy_list = []
            for proxy in proxy_data.split("\n"):
                if proxy:
                    proxy_list.append(proxy)

            for proxy in proxy_list:
                for _type in ['web', 'news']:
                    if multi_progress:
                        this_thread = threading.Thread(target=start2create_pdf, args=(
                            file_prefix, wd, output_dir, [_type], proxy, debug
                        ))
                        this_thread.start()
                    else:
                        start2create_pdf(file_prefix, wd, output_dir, [_type], proxy, debug)

            # for t in threads:
            #     t.join()
            # print("退出主线程")


if __name__ == '__main__':
    main()
