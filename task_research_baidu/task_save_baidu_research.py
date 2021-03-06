#coding:utf-8

"""
* * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    Task to research baidu with your keyword, 
        And then save it as pdf on your local device.

    Author: Roger
    Python Version: python3+
* * * * * * * * * * * * * * * * * * * * * * * * * * * * 
"""

import click
import datetime
import sys
import os
import pdfkit
import threading
import time
from os import path as osp
from urllib.parse import quote_plus


SUCCESS, ERROR, WARNING = 'SUCCESS', 'ERROR', 'WARNING'
def _log(info, directory, level=SUCCESS):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('%s - %s - %s' % (level, now, info))
    log_path = osp.join(directory, f"log_{level.lower()}.log")
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
        start2create_pdf(self.file_prefix, self.wd, self.output_dir, self.types, self.proxy, debug)
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


help_c = """Task to research baidu with your keyword, and then save it as pdf."""
help_output = "Output directory, like: ~/Desktop."
help_wd = "The keyword what you want to resarch."
help_debug = "Debug mode, don't use WKHTMLTOPDF."


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
    """
        use WKHTMLTOPDF get data
    """
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
        url=url,
    )
    return True


def start2create_pdf(file_prefix, wd, output_dir, types, proxy, debug):
    """Create Pdf"""
    # _proxy_ip = proxy.split(":")[0]
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
                    _log(f"Exists!! [{this_file_name}] - {_type} - {proxy}", output_dir, WARNING)
                    continue

                real_create_pdf(path, url, proxy, debug)
                fsize = getsize(path)
                _log(f"[{this_file_name}] - {_type} - {proxy} - {fsize}KB", output_dir)
            except Exception as e:
                _log(f"[{this_file_name}] - {_type} - {proxy} - e: {e}", output_dir, ERROR)

    _log(f"Pdf created {_type} - {proxy}.....", output_dir)
    return True


@click.command()
@click.help_option("-h", "--help", help=help_c)
@click.option("-o", "--output-dir", "output_dir", help=help_output, type=str, default="./OUTPUT")
@click.option("-wd", "--keyword", "keywords", help=help_wd, type=str, required=True)
@click.option("-d", "--debug", "debug", help=help_debug, type=bool, default=False)
def main(output_dir, keywords, debug):

    _log("Start to research .....", output_dir)
    today = datetime.datetime.now().strftime('%Y.%m.%d')

    output_dir = osp.join(output_dir, today)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

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
                this_thread = threading.Thread(target=start2create_pdf, args=(file_prefix, wd, output_dir, ['web', 'news'], proxy, debug))
                this_thread.start()

            # for t in threads:
            #     t.join()
            # print("退出主线程")


if __name__ == '__main__':
    main()
