# hath-rust_Packer

## 如何使用？

下载 release 中的 deb 包，使用 `dpkg -i hath-gnu.deb` 安装

使用命令

```
hath --cache-dir /var/lib/hath/cache --data-dir /var/lib/hath/data --download-dir /var/lib/hath/download --log-dir /var/lib/hath/log --temp-dir /var/lib/hath/tmp
```

完成首次启动，按照提示配置你的 hath 客户端

使用以下命令让 hath 保持后台运行

```
# 启动开机自启
systemctl enable hath

# 关闭开机自启
systemctl disable hath

# 启动
systemctl start hath

# 关闭
systemctl stop hath

# 重启
systemctl restart hath

# 查看控制台输出
journalctl -u hath
```

## 如何选择 gnu 和 musl

gnu 使用系统中的动态库，musl 则是静态编译（自带库）

因此，gnu 理论上会更省内存，musl 会有更好的兼容性，性能上无显著差别。

所以先尝试 gnu，跑不起来就卸了装 musl，原则就是哪个能用用哪个。