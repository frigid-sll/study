Nginx是俄罗斯人Igor Sysoev编写的轻量级Web服务器，它的发音为 [ˈendʒɪnks] ，它不仅是一个高性能的HTTP和反向代理服务器，同时也是一个IMAP/POP3/SMTP 代理服务器。

截至2019年12月，差不多世界上每3个网站中就有1个使用Nginx。

![img](http://www.nginx.cn/wp-content/uploads/2019/12/4ffce04d92a4d6cb21c1494cdfcd6dc1.jpg)

Nginx以事件驱动的方式编写，所以有非常好的性能，同时也是一个非常高效的反向代理、负载平衡服务器。在性能上，Nginx占用很少的系统资源，能支持更多的并发连接，达到更高的访问效率；在功能上，Nginx是优秀的代理服务器和负载均衡服务器；在安装配置上，Nginx安装简单、配置灵活。

Nginx支持热部署，启动速度特别快，还可以在不间断服务的情况下对软件版本或配置进行升级，即使运行数月也无需重新启动。

在微服务的体系之下，Nginx正在被越来越多的项目采用作为网关来使用，配合Lua做限流、熔断等控制。

![img](http://www.nginx.cn/wp-content/uploads/2019/12/4ffce04d92a4d6cb21c1494cdfcd6dc1.png)

对于Nginx的初学者可能不太容易理解web服务器究竟能做什么，特别是之前用过Apache服务器的，以为Nginx可以直接处理php、java，实际上并不能。对于大多数使用者来说，Nginx只是一个静态文件服务器或者http请求转发器，它可以把静态文件的请求直接返回静态文件资源，把动态文件的请求转发给后台的处理程序，例如php-fpm、apache、tomcat、jetty等，这些后台服务，即使没有nginx的情况下也是可以直接访问的（有些时候这些服务器是放在防火墙的面，不是直接对外暴露，通过nginx做了转换）。