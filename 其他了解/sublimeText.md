##### 自定义python环境

```
{
        //"shell_cmd": "make"
        "cmd": ["D:/Python/python.exe","-u","$file"],
         "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
         "selector": "source.python",
        //"encoding": "cp936"                    #该行也可
        "env": {"PYTHONIOENCODING": "utf8"}      #encoding 和 env两行任选其一，经测试都可解决中文乱码问题
    }
```







##### 第 1 步

打开 Sublime Text

##### 第 2 步

使用命令 Ctrl+shift+p 打开命令面板

键入以下内容，直到出现该选项并选择它。Package Control: Install Package

注意：如果您是第一次使用包控制，则需要安装它。

输入入“Terminus”并选择它。等待它完成安装并重新启动 sublime text。

##### 第 3 步

现在转到Preferences >Package Settings > Terminus > Command Palette

代码粘贴至文件

```
[
   {
        "caption": "Terminal (panel)",
        "command": "terminus_open",
        "args"   : {
           "cmd": "/bin/zsh",
           "cwd": "${file_path:${folder}}",
           "title": "Command Prompt",
           "panel_name": "Terminus"
        }
   },
]  

```

注意：以上代码适用于 mac 用户，对于 Windows 用户，您必须输入“cmd.exe”代替“bash”

##### 第 4 步

现在转到Preferences >Package Settings > Terminus > Key Bindings

将此代码粘贴到 Default sublime Keymap 并保存：

```
[
   {
       "keys": ["alt+1"],
       "command": "terminus_open",
       "args" : {
           "cmd": "/bin/zsh",
           "cwd": "${file_path:${folder}}",
           "panel_name": "Terminus"
       }
   }
] 

```

注意：以上代码适用于mac用户，Windows用户需要输入“cmd.exe”代替“bash”，这里我们保留快捷键为“alt+1”，您可以使用自己的键。

##### 第 5 步

每当您想使用终端时，请按alt+1并在终端中关闭终端类型 exit 并按 Enter。
