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
from os import path as osp
from urllib.parse import quote_plus
from subprocess import PIPE, Popen

SUCCESS, ERROR, WARNING = 'SUCCESS', 'ERROR', 'WARNING'
def _log(info, directory, level=SUCCESS):
    print(info)
    log_path = osp.join(directory, 'log.log')
    with open(log_path, 'a+') as f:
        f.write('%s %s %s\n' % (level, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), info))


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


# Page set
PAGES = [0, 1, 2]

# WKHTMLTOPDF = "/usr/local/bin/wkhtmltopdf"
WKHTMLTOPDF = "wkhtmltopdf"
URL = "https://www.baidu.com/s?wd={wd}&pn={pn}"

help_c = """Task to research baidu with your keyword, and then save it as pdf."""
help_output = "Output directory, like: ~/Desktop."
help_wd = "The keyword what you want to resarch."


def test_new_file(path):
    with open(path, "a") as f:
        f.write(path)
    return True


def getsize(path):
    """ return float with UNIT KB """
    if os.path.exists(path):
        return round(os.path.getsize(path) / 1024, 2)
    else:
        return 0


@click.command()
@click.help_option("-h", "--help", help=help_c)
@click.option("-o", "--output-dir", "output_dir", help=help_output, type=str, default="./OUTPUT")
@click.option("-wd", "--keyword", "keyword", help=help_wd, type=str, required=True)
def main(output_dir, keyword):

    _log("Start to research .....", output_dir)

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
        cmd = f'{WKHTMLTOPDF} "{url}" "{path}"'        # cmd = 'echo "Hello World!!"'
        _log(cmd, output_dir)

        # execute command
        var = cmdline(cmd)
        
        fsize = getsize(path)
        _log(f"[{this_file_name}]  {fsize}KB", output_dir)

    _log("All are done.....", output_dir)

if __name__ == '__main__':
    main()