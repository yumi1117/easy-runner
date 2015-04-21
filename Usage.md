# 介绍 #

一个Python实现的简单压测工具


# Details #

Easy Runner主要实现了多线程压测,类似LoadRunner,能得出QPS和RT,并能通过matlibplot画出曲线图.
## 特性 ##
  1. 支持多scenario同时执行
  1. 可为不同scenario设置think time和线程数
  1. 支持warming
  1. 可画出性能曲线
  1. 使用方便,启动迅速,一条命令即可开始压测
## 优势 ##
  1. scenario直接使用python编写scenario,使天然支持多协议
  1. Easy Runner一共300来行代码,维护方便
## 劣势 ##
  1. 是通过多线程来加大压力,对客户端要求较高,不能有太多的线程数


# 使用说明 #

## 设置篇 ##

见easy\_runner下的setting.py进行配置
  * MONITOR\_INTERVAL = 1        #设置性能监控的时间间隔,默认为1s,设的越小数据越正确
  * SCENARIOS\_PATH=("./scenario",)     #设置剧本的存放路径,可以设置多个路径,程序会从设置的路径载入剧本
  * LOG\_PATH\_AND\_FILE\_NAME = "D:\\tmp\\runner.log"  #设置log存放路径,压测信息都会记录在这个log下,以便分析和作图
  * PIC\_SAVE\_PATH\_AND\_PREFIX = "D:\\tmp\\pic_"   #设置性能曲线的生成路径和文件前缀.可设为None,如果为None,生成的图片会直接以窗口方式打开
  * THREAD\_RULE=(10,3)  #线程预热规则,前一个参数表示预热间隔,后一个参数表示每次预热会启动的线程数,可设为None,如果为None,则无预热_

## 剧本编写篇 ##
例子见附件中的easy\_runner\scenario\example.py 这是一个压测剧本
其中
  * thread\_num=200 为为这个剧本开启的并发线程数
  * think\_time = 0 为这个剧本执行时的think time 单位为秒
  * run\_count = 1000 为这个脚本的执行次数
  * name="update" 指定这个剧本的名字,如果不同的剧本使用相同的名字,那么在最后做性能曲线时,相同名字的数据会进行合并显示

  * def init(self):  剧本初始化函数
  * def action(self):  剧本会被重复执行的函数..需要返回True为成功,False为失败
  * def destory(self): 剧本执行完后的资源释放函数

注意,剧本的类名必须是class Scenario(core.scenario.abstract\_scenario):

## 使用篇 ##
如果已经做好了设置,也编写好了脚本即可以开始压测了.
开始压测很简单,直接在命令行键入python starter.py 就会开始压测.
这个时候会根据MONITOR\_INTERVAL设置的时间间隔,直接输出QPS和RT信息,并同时开始记log (注:如果log已存在的话,原log会被重命名)
如果需要停止压测,在命令行直接输入q 回车 即可结束压测.

## 生成图形篇 ##
生成图形也很简单,直接在命令行键入python plot.py 就是自动分析刚才的log文件生成图形(plot.py需要matlibplot的支持~)

图形样例如下:
  * 返回成功的QPS:
> > ![http://pic.yupoo.com/zephyrleaves/Bg97VkM4/medish.jpg](http://pic.yupoo.com/zephyrleaves/Bg97VkM4/medish.jpg)
  * 返回失败的QPS:
> > ![http://pic.yupoo.com/zephyrleaves/Bg97Vvdt/medish.jpg](http://pic.yupoo.com/zephyrleaves/Bg97Vvdt/medish.jpg)
  * 总QPS(失败+成功):
> > ![http://pic.yupoo.com/zephyrleaves/Bg97VJtv/medish.jpg](http://pic.yupoo.com/zephyrleaves/Bg97VJtv/medish.jpg)
  * 响应时间
> > ![http://pic.yupoo.com/zephyrleaves/Bg97VBCA/medish.jpg](http://pic.yupoo.com/zephyrleaves/Bg97VBCA/medish.jpg)