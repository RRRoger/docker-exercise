# Research Baidu Website

> Just For fun.
> Task to research baidu with your keyword, 
> And then save it as pdf on your local device.

## Download Fonts

> Download Chinese fonts to the directory `fonts`, otherwise there is no Chinese

- [思源字体](https://github.com/adobe-fonts/source-han-serif/tree/release/)
- [霞婺文楷](https://github.com/lxgw/LxgwWenKai/releases) 

## Docker Build

```bash
# Directory the Dockerfile reside
cd docker-exercise/task_research_baidu

# remove if exist
docker rm baidu_research
docker rmi baidu_research

# build image
docker build -t baidu_research .
```

## Docker run 

### 1. research 三体

```bash
docker run -it --name research_three_body_problem \
    -e KEYWORD="三体" \
    -v ~/workdir/OUT_FOLDER:/app/OUTPUT \
    baidu_research

# And after
docker start -i research_three_body_problem
```

### 2. research 周杰伦

```bash
docker run -it --name research_jay_chou \
    -e KEYWORD="周杰伦" \
    -v ~/workdir/OUT_FOLDER:/app/OUTPUT \
    baidu_research

# And after
docker start -i research_jay_chou
```
