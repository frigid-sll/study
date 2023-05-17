#### fmt库 

fmt库提供了一些基本的输入/输出函数，如Printf、Sprintf、Fprintf、Scanf、Sscanf、Fscanf等。 示例代码：

##### Println函数

Println函数将字符串原样输出

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	str := "hello, hello world!"
	res := strings.Replace(str, "hello", "hi", -1)
	fmt.Println(res)
}
```





##### Printf函数

Printf函数将格式化的字符串输出到标准输出中，它的格式如下：

```go
func Printf(format string, a ...interface{}) (n int, err error)
```

其中，format是格式化字符串，a是一个可变参数，表示需要格式化的数据。示例代码如下：

```go
package main
import "fmt"
func main() {
    var age int = 18
    var name string = "Tom"
    fmt.Printf("My name is %s, and I am %d years old.\n", name, age)
}
```

输出结果为：

```
My name is Tom, and I am 18 years old.
```



##### Sprintf函数

Sprintf函数将格式化的字符串输出到一个字符串中，它的格式如下：

```go
func Sprintf(format string, a ...interface{}) string
```

其中，format是格式化字符串，a是一个可变参数，表示需要格式化的数据。示例代码如下：

```go
package main
import "fmt"
func main() {
    var age int = 18
    var name string = "Tom"
    str := fmt.Sprintf("My name is %s, and I am %d years old.\n", name, age)
    fmt.Println(str)
}
```

输出结果为：

```
My name is Tom, and I am 18 years old.
```



##### Fprintf函数

Fprintf函数将格式化的字符串输出到一个文件中，它的格式如下：

```go
func Fprintf(w io.Writer, format string, a ...interface{}) (n int, err error)
```

其中，w是一个io.Writer类型的参数，表示输出的目标文件，format是格式化字符串，a是一个可变参数，表示需要格式化的数据。示例代码如下：

```go
package main
import (
    "fmt"
    "os"
)
func main() {
    var age int = 18
    var name string = "Tom"
    f, _ := os.Create("output.txt")
    fmt.Fprintf(f, "My name is %s, and I am %d years old.\n", name, age)
    f.Close()
}
```

运行该程序会在当前目录下创建一个output.txt文件，并将格式化的字符串输出到该文件中。 



##### Scanf函数

Scanf函数从标准输入中读取格式化的数据，它的格式如下：

```go
func Scanf(format string, a ...interface{}) (n int, err error)
```

其中，format是格式化字符串，a是一个可变参数，表示需要读取的变量。示例代码如下：

```go
package main
import "fmt"
func main() {
    var age int
    var name string
    fmt.Println("Please enter your name and age:")
    fmt.Scanf("%s %d", &name, &age)
    fmt.Printf("My name is %s, and I am %d years old.\n", name, age)
}
```

运行该程序后，程序会提示用户输入姓名和年龄，并将输入的数据格式化输出。 



##### Sscanf函数

Sscanf函数从一个字符串中读取格式化的数据，它的格式如下：

```go
func Sscanf(str string, format string, a ...interface{}) (n int, err error)
```

其中，str是需要读取的字符串，format是格式化字符串，a是一个可变参数，表示需要读取的变量。示例代码如下：

```go
package main

import (
	"fmt"
)

func main() {
	var age int
	var name string
	str := "Tom 18"
	fmt.Sscanf(str, "%s %d", &name, &age)
	fmt.Println(name, age)
}
```

运行该程序后，程序会从字符串中读取姓名和年龄

```
Tom 18
```





##### Fscanf函数

Fscanf函数从一个文件中读取格式化的数据，它的格式如下：

```go
func Fscanf(r io.Reader, format string, a ...interface{}) (n int, err error)
```

其中，r是一个io.Reader类型的参数，表示输入的目标文件，format是格式化字符串，a是一个可变参数，表示需要读取的变量。示例代码如下：

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	var age int = 18
	var name string = "Tom"
	f, _ := os.Create("output.txt")
	fmt.Fprintf(f, "My name is %s, and I am %d years old.\n", name, age)
	f.Close()

	var age2 int
	var name2 string
	f2, _ := os.Open("input.txt")
	fmt.Fscanf(f2, "%s %d", &name2, &age2)
	fmt.Printf("My name is %s, and I am %d years old.\n", name, age)

}
```

先创建output.txt，然后读取，输出结果为：

```
My name is Tom, and I am 18 years old.
```





##### fmt.Fprintln

`fmt.Fprintln`是Go语言标准库fmt中的一个函数，用于将数据格式化为字符串并输出到指定的输出流中。函数签名为：

```go
goCopy code
func Fprintln(w io.Writer, a ...interface{}) (n int, err error)
```

参数说明：

- `w`：表示输出流，通常使用`os.Stdout`表示标准输出。
- `a...`：表示要输出的数据，可以是任意类型的值。 返回值说明：
- `n`：表示成功写入的字节数。
- `err`：表示写入过程中遇到的错误。 下面是一个示例程序：

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	var name string
	var age int
	var height float64
	fmt.Fprintln(os.Stdout, "Please enter your name, age and height:")
	n, err := fmt.Fscanf(os.Stdin, "%s %d %f", &name, &age, &height)
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		return
	}
	fmt.Fprintf(os.Stdout, "Name: %s\nAge: %d\nHeight: %.2f\n", name, age, height)
	fmt.Fprintf(os.Stdout, "Successfully read %d parameters.\n", n)
}

```

这个程序使用`fmt.Fprintln`函数将数据输出到标准输出中。输出的数据包括用户的姓名、年龄和身高。运行示例程序，输出如下结果：

```
Please enter your name, age and height:
pert 23 176
Name: pert
Age: 23
Height: 176.00
Successfully read 3 parameters.
```

可以看到，这个程序成功地将数据输出到了标准输出中，每个数据占一行。输出的数据格式与`fmt.Println`函数类似，但是可以指定输出流。
