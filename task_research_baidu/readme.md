# Research Baidu Website

> Just For fun

## Docker run

- 1

```bash
cd docker-exercise/task_research_baidu

docker rm baidu_research

docker rmi baidu_research

docker build -t baidu_research .

docker run -it --name directly_research \
    -e KEYWORD="三体" \
    -v ~/workdir/OUT_FOLDER:/app/OUTPUT \
    directly_research

# And after
docker start directly_research
```

## Fonts

- [思源字体](https://github.com/adobe-fonts/source-han-serif/tree/release/)
- [霞婺文楷](https://github.com/lxgw/LxgwWenKai/releases) 

