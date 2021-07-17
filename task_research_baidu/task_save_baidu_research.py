# -*- coding: utf-8 -*-

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
from os import path as osp
from urllib.parse import quote_plus


# Page set
PAGES = [0, 1, 2]

WKHTMLTOPDF = "/usr/local/bin/wkhtmltopdf"
URL = "https://www.baidu.com/s?wd={wd}&pn={pn}"

help_c = """Task to research baidu with your keyword, and then save it as pdf."""
help_output = "Output directory, like: ~/Desktop."
help_wd = "The keyword what you want to resarch."

def test_new_file(path):
    with open(path, "a") as f:
        f.write(path)
    return True


@click.command()
@click.help_option("-h", "--help", help=help_c)
@click.option("-o", "--output-dir", "output_dir", help=help_output, type=str, default="./OUTPUT")
@click.option("-wd", "--keyword", "keyword", help=help_wd, type=str, required=True)
def main(output_dir, keyword):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    wd = quote_plus(keyword)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    file_prefix = f"{keyword}-{today}"

    for page in PAGES:
        this_file_name = f"{file_prefix}_page{page+1}.pdf"
        pn = page * 10
        url = URL.format(wd=wd, pn=pn)
        path = osp.join(output_dir, this_file_name)
        cmd = f'{WKHTMLTOPDF} "{url}" "{path}"'
        print(cmd)
        test_new_file(path)
        # os.system(cmd)

    print("All are Done.....")

if __name__ == '__main__':
    main()

"""
docker run -d --name baidu_research \
    -p 8888:8888 \
    -e LANG=zh_CN.UTF-8 \
    -e KEYWORD=odoo \
    -v ~/workdir/OUT_FOLDER:/app/OUTPUT \
    baidu_research
"""