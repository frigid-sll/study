Go语言的strings包提供了一些常见的字符串处理函数，下面我们来详细介绍一下常见的函数和使用方法：



##### len函数 

len函数返回字符串的长度，它的格式如下：

```go
func len(s string) int
```

示例代码如下：

```go

package main
import "fmt"
func main() {
    str := "Hello, world!"
    fmt.Println(len(str))
}
```

输出结果为：

```
13
```



##### Index函数

Index函数返回子串在字符串中第一次出现的位置，若未找到则返回-1，它的格式如下：

```go
func Index(s, substr string) int
```

其中，s表示要查找的字符串，substr表示要查找的子串。示例代码如下：

```go
package main
import "fmt"
func main() {
    str := "Hello, world!"
    idx := strings.Index(str, "world")
    fmt.Println(idx)
}
```

输出结果为：

```
7
```



##### Split函数

Split函数将一个字符串按照指定的分隔符分割成多个子串，并返回一个**字符串切片**，它的格式如下：

```go
func Split(s, sep string) []string
```

其中，s表示要分割的字符串，sep表示分隔符。示例代码如下：

```go
package main
import (
    "fmt"
    "strings"
)
func main() {
    str := "apple,banana,orange"
    arr := strings.Split(str, ",")
    fmt.Println(arr)
}
```

输出结果为：

```
[apple banana orange]
```



##### Join函数

Join函数将一个**字符串切片**按照指定的分隔符拼接成一个字符串，它的格式如下：

**字符串切片不等于字符串！**字符串切片相当于python的列表，可以按下标取值

```go
func Join(a []string, sep string) string
```

其中，a表示要拼接的字符串切片，sep表示分隔符。示例代码如下：

```go
package main
import (
    "fmt"
    "strings"
)
func main() {
    arr := []string{"apple", "banana", "orange"}
    str := strings.Join(arr, ",")
    fmt.Println(str)
}
```

输出结果为：

```
apple,banana,orange
```

注：

```go
arr := []string{"apple", "banana", "orange"}
就等同于
str := "apple,banana,orange"
arr := strings.Split(str, ",")

结果为：
[apple banana orange]
```





##### Replace函数

Replace函数将字符串中指定的子串替换成另一个子串，并返回替换后的字符串，它的格式如下：

```go
func Replace(s, old, new string, n int) string
```

其中，s表示要替换的字符串，old表示要替换的子串，new表示替换后的子串，n表示替换的次数，**-1表示全部替换**。示例代码如下：

```go
package main
import (
    "fmt"
    "strings"
)
func main() {
    str := "hello, world!"
    newstr := strings.Replace(str, "hello", "hi", 1)
    fmt.Println(newstr)
}
```

输出结果为：

```
hi, world!
```



##### Trim函数

Trim函数将字符串前后指定的字符删除，并返回删除后的字符串，它的格式如下：

```go
func Trim(s string, cutset string) string
```

其中，s表示要删除的字符串，cutset表示要删除的字符集。示例代码如下：

```go
package main
import (
    "fmt"
    "strings"
)
func main() {
    str := "   hello, world!   "
    newstr := strings.Trim(str, " ")
    fmt.Println(newstr)
}
```

输出结果为：

```
hello, world!
```



##### ToUpper函数和ToLower函数

ToUpper函数将字符串中的字母全部转换成大写，ToLower函数将字符串中的字母全部转换成小写，它们的格式如下：

```go
func ToUpper(s string) string
func ToLower(s string) string
```

示例代码如下：

```go
package main
import (
    "fmt"
    "strings"
)
func main() {
    str := "Hello, world!"
    upperstr := strings.ToUpper(str)
    lowerstr := strings.ToLower(str)
    fmt.Println(upperstr)
    fmt.Println(lowerstr)
}
```

输出结果为：

```
HELLO, WORLD!
hello, world!
```