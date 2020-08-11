# PMon 边界网络端口持续监控

## 1. 概述
PMon是为了持续监控网络端口而设计，主要适用外网边界端口持续监控。可以在有效资源内，实现端口发现、监控、动态更新等基础安全风险动态管理能力。
关于系统设计思路理念，可以关注微信公众号"安小记"，查看公众号文章："如何做好边界端口持续监控".


## 2. 简要说明

整个监控系统分为三大组件，分别是：
- server： 后台，负责任务下发调度、后台API 
- work：执行扫描任务Agent，负责执行具体扫描工作，并将结果返回给`server`
- admin：前端展示，使用 `vue-element-admin`前端框架


## 3. 组件列表

- 数据库:
  - Mongodb： 系统主要数据库;

- 后台服务 - `server`：

  - Flask：Python轻量级Web开发框架，提供基础Web功能；

  - flask-restful： Flask的Restful Api插件，实现后台Api与节点之间的通讯；

  - APScheduler：Python任务调度模块，实现后台任务管理、节点任务定时下发功能；

  - gunicorn：Python WSGI服务，用于部署Flask应用;
  - Supervisor: 后台进程管理服务，用于保证后台服务持续运行；

- 任务节点 - `work`：

  - Celery： 分布式任务队列，实现节点任务执行；

  - Flower： Celery组件，实现Celery节点监控以及任务下发和监控的Web Api；
  - Redis: Key-Value数据库，Celery任务管理存储调度；

- 前端框架 - `admin`：
  - vue-element-admin: 基于Vue和element的前端开发框架，实现系统可视化展示；


## 4. 部署

由于各部分是相互独立的，请进各自目录，完成组件安装，详见各目录下`README.md`；

另外，`admin`目录是前端框架，是基于vue-element-admin二次开发而成，这里就直接使用README的文档。
感谢[vue-element-admin](https://github.com/PanJiaChen/vue-element-admin)提供那么简单易用的框架。

**注意： 因系统环境差异大，请根据实际情况部署。个人只是安全运营人员，非专业开发，出现问题可能需要使用人员有一定看代码和解决问题能力。**



## 5. 更多

由于是个人业余开发，精力有效，程序逻辑较为复杂，建议使用人员具备一定的python编程经验，最好能够熟练上述各开源组件，如有疑问，我尽力解答哈。

也是第一次尝试开源自己做的东西，文档什么的也没准备的太好，还请各位大佬见谅！


如有建议、指导，欢迎关注公众号`安小记`，或加微信，期待和各位大佬交流；

![AnSecNote](https://raw.githubusercontent.com/chiww/PMon/master/pic/AnSecNote.jpg)

另外，为了更方便交流，新建了该项目的微信群，欢迎各位扫描加入：

<img src="https://raw.githubusercontent.com/chiww/PMon/master/pic/Wechat_PMon.JPG" width = "258" height="343" alt="Wechat" />


## 6. 鸣谢

2020.08.11 感谢 [yolylight](https://github.com/yolylight) 完善部署文档和修改小BUG；
