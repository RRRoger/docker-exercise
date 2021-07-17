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

# Install Libaries
RUN pip install --no-cache-dir -r requirements.txt \
 -i $PY_MIRROR --trusted-host $SERVER

# 假装需要暴露端口
# EXPOSE 8888
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["entrypoint.sh"]
# CMD [""]

# ENTRYPOINT [ "python" ]
CMD [ "tail", "-f", "task_save_baidu_research.py" ]
# CMD [ "python", "task_save_baidu_research.py", "-wd", $KEYWORD ]
