##### **Grep 命令的快速示例**

您可能已经知道要在文件中搜索特定文本或模式，您必须像这样使用 grep：

```text
grep search_pattern filename
```

##### grep：对信息进行过滤筛选

- 对文件信息进行过滤

  ```
  grep "oldgril" oldboy.txt
  ```

  - 对文件信息筛选出来的信息上一行也显示出来

    ```
    grep -B 1 "oldgirl" /oldboy.txt
    
    B:before
    1:上一行
    ```

  - 对文件信息筛选出来的信息下一行页显示出来

    ```
    grep -A 1 "oldgirl" /oldboy.txt
    
    A:after
    1:后一行
    ```

  - 既想看前一行也想看后一行

    ```
    grep -C 1 "oldgril" /oldboy.txt
    
    C:center
    1:上一行和下一行
    ```

- 对命令信息进行过滤

  ```
  ss -lntup | grep "22"
  ```

- 统计文件中某字符有多少行

  ```
  grep -c "oldgril" /oldboy.txt
  
  c:count 计数
  ```



让我们看看 grep 命令的几个常见用例。



##### **不区分大小写的搜索**

默认情况下，使用 grep 进行的搜索区分大小写，-i您可以使用以下选项忽略大小写匹配：

```text
grep -i search_pattern filename
```

这样，grep 将返回与 和 匹配的Holmes行holmes。



##### **显示匹配行之前和之后的行**

默认情况下，您只会看到匹配的行，但是，当您对某些问题进行故障排除时，在匹配行之前和/或之后查看几行会有所帮助。

您可以使用-A来显示匹配行之后的行。

> 请记住，A 代表 After。

下面的命令将显示匹配的行以及匹配后的 5 行。

```text
grep -A 5 search_pattern filename
```

同样，您可以使用该-B选项在匹配行之前显示行。

> 请记住，B 代表之前。

下面的命令将在匹配行之前显示 5 行以及匹配行。

```text
grep -B 5 search_pattern filename
```

我最喜欢的是该选项-C，因为它显示了匹配行之前和之后的行。

> 请记住，这里的 C 代表圆。

下面的命令将显示匹配行之前的 5 行、匹配行和 matchine 行之后的 5 行。

```text
grep -C 5 search_pattern filename
```



##### **显示不匹配的行**

您可以使用 grep 显示与给定模式不匹配的所有行。此“反转匹配”与以下-v选项一起使用：

```text
grep -v search_pattern filename
```

您可以组合-i和-v选项。



##### **计算匹配行数**

-c您可以使用选项获取与模式匹配的行数，而不是显示匹配的行。这是小写的c。

```text
grep -c search_pattern filename
```

您可以结合-cand-v选项来获取与给定模式不匹配的行数。您当然可以使用不区分大小写的选项-i。



##### **显示匹配行的行号**

要显示匹配行的行号，您可以使用该-n选项。

```text
grep -n search_pattern filename
```

您可以对反向搜索执行相同的操作。



##### **在多个文件中搜索**

您可以提供多个文件供 grep 搜索。

```text
grep search_pattern file1 file2
```

这可能有效，但更实际的示例是搜索特定类型的文件。例如，如果您只想在 shell 脚本中查找字符串（以 .sh 结尾的文件），您可以使用：

```text
grep search_pattern *.sh
```



##### **递归搜索目录中的所有文件**

您可以使用 grep option执行递归搜索-r。它将在当前目录及其子目录中的所有文件中搜索给定的模式。

```text
grep -r search_pattern directory_path
```



##### **仅显示文件名**

默认情况下，grep 显示匹配的行。如果您对多个文件运行了搜索，并且只想查看哪些文件包含该字符串，则可以使用该-l选项。

```text
grep -l search_pattern files_pattern
```

假设您想查看哪些 Markdown 文件包含“手册”一词，您可以使用：

```text
grep -l handbook *.md
```



##### **仅搜索全词**

默认情况下，grep 将显示包含给定字符串的所有行。你可能并不总是想要那个。如果您正在搜索单词“done”，它还会显示包含“doner”或“abandoned”字样的行。

要使 grep 仅搜索完整的单词，您可以使用以下选项-w：

```text
grep -w search_string file
```

这样，如果您搜索单词“done”，它只会显示包含“done”的行，而不是“doner”或“abandoned”。



##### **搜索正则表达式模式**

您可以使用正则表达式模式为您的搜索提供超级动力。有一个允许使用正则表达式模式的专用选项-e和-E一个允许使用扩展正则表达式模式的选项。

```text
grep -e regex_pattern file
```

 

##### **搜索这个或那个模式**

您可以在同一个 grep 搜索中搜索多个模式。如果要查看包含一种模式或另一种模式的行，可以使用 OR 运算符|。

> 但是，您必须以下列方式转义此特殊字符。

```text
grep 'pattern1\|pattern' filename
```

您可以将多个模式与 OR 运算符一起使用。

AND 运算符没有特定选项。为此，您可以多次使用 grep 和管道重定向。



##### **搜索二进制文件**

Grep 默认忽略二进制文件。-a您可以使用该选项使其在二进制文件中搜索，就好像它是文本文件一样。

```text
grep -a pattern binary_file
```



##### 显示匹配过程

```
grep -o "."  1.txt
```

