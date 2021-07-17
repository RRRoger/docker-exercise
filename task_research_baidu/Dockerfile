FROM python:3.8-alpine

# 支持中文
ENV LANG=zh_CN.UTF-8

LABEL author="RRRoger<chenpeng.0418@163.com>"

# 搜索关键词
# ENV KEYWORD=三体

# Python国内镜像
# ENV PY_MIRROR=http://mirrors.aliyun.com/pypi/simple/

RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
ADD task_save_baidu_research.py task_save_baidu_research.py

# Install Libaries
RUN pip install --no-cache-dir -r requirements.txt

# 假装需要暴露端口
EXPOSE 8888

RUN echo $KEYWORD
RUN echo $LANG

# CMD ["python", "task_save_baidu_research.py", "-wd $KEYWORD"]

ENTRYPOINT [ "python3" ]
CMD ["task_save_baidu_research.py", "-wd", $KEYWORD]
