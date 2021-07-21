FROM leoossais/python-wkhtmltopdf

# Generate locale C.UTF-8 for scripts and general locale data
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

LABEL author="RRRoger<chenpeng.0418@163.com>"

# the keyword what you want to research
# ENV KEYWORD=odoo

# pip mirror source
ENV SERVER=mirrors.aliyun.com
ENV PY_MIRROR=http://$SERVER/pypi/simple/

RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
ADD task_save_baidu_research.py task_save_baidu_research.py

# Install Libaries and wkhtmltopdf
RUN pip install --no-cache-dir -r requirements.txt \
        -i $PY_MIRROR --trusted-host $SERVER

# copy chinese font to container
# You can download it from the url below
# https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/Variable/OTF/SourceHanSansSC-VF.otf
COPY fonts/* /usr/share/fonts/

COPY entrypoint.sh /usr/local/bin/

# Part1
ENTRYPOINT ["entrypoint.sh"]

# Part2
# CMD [ "tail", "-f", "task_save_baidu_research.py" ]
