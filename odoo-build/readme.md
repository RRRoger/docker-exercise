## Commands

```bash
docker start <odoo-container-name>   # 启动odoo服务  odoo为第一次启动时指定的别名
docker stop <odoo-container-name>  # 停止odoo服务
docker restart <odoo-container-name>  # 重启
docker logs -f <odoo-container-name>   # 查看日志信息

docker ps

# 交互式终端
docker exec -it <odoo-container-name> /bin/bash

# 不进入容器，直接对容器执行指定的命令
docker exec -it <odoo-container-name> <命令>
```