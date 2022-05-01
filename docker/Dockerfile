# 指定基础镜像
FROM python:3.8
# 指定镜像的维护者
MAINTAINER AnlakHui "AnlakHui@gmail.com"
# 设置工作目录
WORKDIR /root
# 从版本控制克隆代码
RUN git clone https://github.com/AnlakHui/msg2bark.git
# 设置工作目录
WORKDIR /root/msg2bark
# 安装项目依赖项
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
# 为启动脚本添加执行权限
RUN chmod 755 run.sh
# 容器启动时要执行的命令
ENTRYPOINT ["./run.sh"]
# 暴露端口
EXPOSE 80