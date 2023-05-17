- ##### 进入wp-content目录，新建tmp文件夹，设置文件夹的权限为777

  ```
  cd wp-content
  mkdir tmp
  chmod -R 777 tmp
  ```

  

- ##### 设置wp-content目录中的plugins（插件）和themes（主题）文件夹权限为777

  ```
  chmod -R 777 plugins
  chmod -R 777 themes
  ```

  

- ##### 编辑wordpress/wp-config.php

  ```
  在
  if ( !defined('ABSPATH') )
  
  define('ABSPATH', dirname(__FILE__) . '/');
  后面添加下面的内容：
  
  define('WP_TEMP_DIR', ABSPATH.'wp-content/tmp');
   
  define("FS_METHOD", "direct");
   
  define("FS_CHMOD_DIR", 0777);
   
  define("FS_CHMOD_FILE", 0777);
  ```

  - 最终`wp-config.php`内代码

    <img src="https://img-blog.csdn.net/20170415005443000?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWxpdmVxZg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center">





