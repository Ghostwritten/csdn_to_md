# csdn 文章批量转换markdown格式下载至本地

## 1. 背景

最近准备搭建新博客,尽管csdn的在线编辑、发布、专栏、自定义模块、模板等比较成熟,但实在没有美感,这一点令人比较失望，但在线编辑确实速度会很快，做笔记非常方便，检索也还算可以,前阵[阿里云开发者社区](https://developer.aliyun.com/)、[infoQ中国社区](https://www.infoq.cn/)运营人员相继邀请去他们平台发布，但我更想尝试本地利用[Obsidian](https://obsidian.md/)工具编写笔记试试，并同步[github](https://github.com/)或[gitee](https://gitee.com/)仓库存储,博客也许会以github page依托利用[hexo](https://hexo.io/zh-cn/)、[Jekyll](https://jekyllcn.com/)等工具发布，如果还可以同步[notion](https://www.notion.so/)或[云雀](https://www.yuque.com/)就更完美。

## 2.功能

- 1. 通过传入id确立个人用户主页；
- 2. 创建个人博客目录，专栏目录；
- 3. 获取专栏URL、名称、篇数量；
- 4. 依靠专栏URL获取对应的多页文章URL、标题；
- 5. 遍历文章URL通过cookie获取文章内容并转换markdown格式。

## 3. 下载

```bash
$ git clone https://github.com/Ghostwritten/csdn_to_md.git 
```

## 4. 配置

chrome浏览器登陆csdn平台，按"F12"找到自己网页cookie,选择部分cookie内容复制至csdn_to_md.py脚本109行。

![获取cookie](https://github.com/Ghostwritten/csdn_to_md/blob/main/cookie.png)

## 5. 演示
* [观看视频](https://www.youtube.com/watch?v=vVJJDB0xQfA&t=25s)

```bash
$ python3 csdn_to_md.py -i  xixihahalelehehe
download blog markdown blog:【helm】helm_快速学习手册
download blog markdown blog:【helm】如何开发一个完整的Helm_charts应用实例
download blog markdown blog:【helm】helm_将yaml文件转换json的插件helm-schema-gen
download blog markdown blog:【helm】helm_NOTES.txt
download blog markdown blog:【helm】helm_test_测试详解
download blog markdown blog:【helm】helm_charts_入门指南
download blog markdown blog:【helm】openshift_Certified_Helm_Charts_实践
download blog markdown blog:【helm】Helm_Values.yaml
......


$ cd xixihahalelehehe 

$ /xixihahalelehehe# tree 
.
├── ansible
│   ├── anible_【模块】_notify.md
│   ├── ansbile【模块】replace_替换.md
│   ├── ansbile_模块开发-自定义模块.md
│   ├── ansible_assert_模块.md
│   ├── ansible_become配置.md
│   ├── ansible_cron_模块.md
│   ├── ansible_debug模块.md
│   ├── ansible_delegate_to_模块.md
│   ├── ansible_file模块详解.md
│   ├── ansible_gather_facts配置.md
│   ├── ansible_hosts_and_groups配置.md
│   ├── ansible_jinja2详解.md
│   ├── ansible-playbook_role角色.md
│   ├── ansible-playbook实战.md
│   ├── ansible_script模块.md
│   ├── ansible_set_fact模块.md
│   ├── ansible_URI模块.md
│   ├── ansible【任务】安装httpd.md
│   ├── ansible变量.md
│   ├── ansible_安装.md
│   ├── ansible_快速学习手册.md
│   ├── ansible【模块】add_host.md
│   ├── ansible【模块】blockinfile.md
│   ├── ansible_【模块】find.md
│   ├── ansible【模块】include_tasks.md
│   ├── ansible【模块】linefile_文件行处理.md
│   ├── ansible【模块】modprobe.md
│   ├── ansible【模块】pause.md
│   ├── ansible_【模块】sysctl.md
│   ├── ansible【模块】systemd.md
│   ├── ansible【模块】template.md
│   ├── ansible【模块】yum.md
│   ├── ansible_系统选择性执行脚本.md
│   ├── ansible远程容器机种方法.md
│   └── ansible_配置.md
├── blog
│   ├── github如何搭建一个博客.md
│   ├── jekyll的一个主题TeXt-theme拆解.md
│   ├── jekyll配置管理github博客.md
│   ├── 如何使用jekyll插件.md
│   ├── 如何安装jekyll并搭建一个博客.md
│   └── 如何购买域名.md
├── c++
│   └── makefile入门.md
├── camera
│   ├── A7R2_图标列表.md
│   ├── sony_A7R2介绍.md
│   └── SONY_A7R2_基础操作.md
├── Cisco
│   ├── 运维之思科篇_-----1.VLAN_、_Trunk_、_以太通道及DHCP.md
│   ├── 运维之思科篇_-----2.vlan间通讯_、_动态路由.md
│   ├── 运维之思科篇_-----3.HSRP（热备份路由协议），STP（生成树协议），PVST（增强版PST）.md
│   ├── 运维之思科篇_-----4._标准与扩展ACL_、_命名ACL.md
│   ├── 运维之思科篇_-----5._NAT及静态转换_、_动态转换及PAT.md
│   ├── 运维之思科篇_-----6..md
│   └── 运维之思科篇_-----6.思科项目练习.md

```
## 6. 技术

- [python json](https://blog.csdn.net/xixihahalelehehe/article/details/106550900)
- [python os](https://blog.csdn.net/xixihahalelehehe/article/details/104253123)
- [python time](https://blog.csdn.net/xixihahalelehehe/article/details/108998768)
- [python request](https://blog.csdn.net/xixihahalelehehe/article/details/108996025)
- [python argparse](https://blog.csdn.net/xixihahalelehehe/article/details/121199110)
- [python re](https://blog.csdn.net/xixihahalelehehe/article/details/106247378)
- [python bs4](https://blog.csdn.net/xixihahalelehehe/article/details/124152439)

- [python split()](https://blog.csdn.net/xixihahalelehehe/article/details/124547771)
- [python list 列表](https://blog.csdn.net/xixihahalelehehe/article/details/104437743)
- [python 计算之除法](https://blog.csdn.net/xixihahalelehehe/article/details/124549366)
- [python range()](https://ghostwritten.blog.csdn.net/article/details/124549150)

## 7. 参考
- [https://blog.csdn.net/pang787559613/article/details/105444286](https://blog.csdn.net/pang787559613/article/details/105444286)


---
