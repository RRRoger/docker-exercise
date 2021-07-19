# Research Baidu Website

> Just For fun

## Docker run

- 1

```bash
cd docker-exercise/task_research_baidu

docker rm baidu_research

docker rmi baidu_research

docker build -t baidu_research .

docker run -d --name baidu_research \
    -e KEYWORD="三体" \
    -v ~/workdir/OUT_FOLDER:/app/OUTPUT \
    baidu_research
```

- 2

```bash
cd docker-exercise/task_research_baidu

docker rm research_iso

docker rmi research_iso

docker build -t research_iso .

docker run -d --name research_iso \
    -e KEYWORD="三体" \
    -v ~/workdir/OUT_FOLDER:/app/OUTPUT \
    research_iso
```

## Fonts

- [思源字体](https://github.com/adobe-fonts/source-han-serif/tree/release/)
- [霞婺文楷](https://github.com/lxgw/LxgwWenKai/releases) 

