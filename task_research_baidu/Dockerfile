FROM python:3.8-alpine

# Generate locale C.UTF-8 for scripts and general locale data
ENV LANG C.UTF-8
ENV LANGUAGE=C.UTF-8

LABEL author="RRRoger<chenpeng.0418@163.com>"

# 搜索关键词
# ENV KEYWORD=odoo

# 使用阿里的源
ENV SERVER=mirrors.aliyun.com
ENV PY_MIRROR=http://$SERVER/pypi/simple/

RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
ADD task_save_baidu_research.py task_save_baidu_research.py

# Install Libaries and wkhtmltopdf
RUN pip install --no-cache-dir -r requirements.txt \
        -i $PY_MIRROR --trusted-host $SERVER \
    && apk add --no-cache wkhtmltopdf

# 复制字体到字体目录，如果宿主机没有准备好字体文件，这里可以换成使用wget去下载
COPY fonts/SourceHanSansSC-VF.otf /usr/share/fonts/

# 假装需要暴露端口
# EXPOSE 8888

COPY entrypoint.sh /usr/local/bin/

# For testing in terminal
# CMD [ "tail", "-f", "task_save_baidu_research.py" ]

ENTRYPOINT ["entrypoint.sh"]
CMD [""]
