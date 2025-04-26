# The-first-blog-site-for-newbies-Cnblogs
My first phase establishes web with python_django
Note the seeting of mysql , to alert you own sql, username, password
注意：启动时避免日志并发问题输入命令 ： python manage.py runserver --noreload
# Cnblogs
## 实现功能

- **用户的登录与注册**
	- username \ password \ email \ 
	- 随机刷新的验证码， 并且点击刷新(pillow库)
	- 头像更新， 建立的是项目内文件储存更新
	- 同时运用mysql进行数据存储与更新
-	**博客主页** 
	- 具有用户认证功能， 验证是否登录	
	-	将文章乱序输出， 带有title 和 summary
	-	标题具有跳转文章detail的功能
	-	主页拥有上固定的标题栏包括：登录、注册、编辑账户信息、注销(未完善)、首页返回按钮、分类筛选文章
	-	左侧有伸缩目录：发表文章、我的评论、我的文章(对文章进行删除)
		-	发表文章是用的kindeditor富文本编辑框， 具有xss攻击过滤功能， 丰富的字体样式
	-	所有文章只要属于自己都可以点击进入文章进行修改，包括文章分类
	- 文章detail还设置了虚拟点赞button， 并未建立sql表进行维护。
