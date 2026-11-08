



## 数据类型

### 1.1 整型（Integer Types）

| 类型 | 大小（通常） | 范围（通常） | 说明 |
|------|------------|------------|------|
| `bool` | 1 字节 | `true` 或 `false` | 布尔类型 |
| `char` | 1 字节 | -128 到 127 或 0 到 255 | 字符类型 |
| `signed char` | 1 字节 | -128 到 127 | 有符号字符 |
| `unsigned char` | 1 字节 | 0 到 255 | 无符号字符 |
| `short` | 2 字节 | -32,768 到 32,767 | 短整型 |
| `unsigned short` | 2 字节 | 0 到 65,535 | 无符号短整型 |
| `int` | 4 字节 | -2,147,483,648 到 2,147,483,647 | 整型 |
| `unsigned int` | 4 字节 | 0 到 4,294,967,295 | 无符号整型 |
| `long` | 4 或 8 字节 | 取决于平台 | 长整型 |
| `unsigned long` | 4 或 8 字节 | 0 到 2³²-1 或 2⁶⁴-1 | 无符号长整型 |
| `long long` | 8 字节 | -9.22×10¹⁸ 到 9.22×10¹⁸ | 长长整型（C++11） |
| `unsigned long long` | 8 字节 | 0 到 1.84×10¹⁹ | 无符号长长整型 |

### 1.2 浮点型（Floating-point Types）

| 类型 | 大小 | 范围（近似） | 精度 | 说明 |
|------|------|-------------|------|------|
| `float` | 4 字节 | ±3.4×10⁻³⁸ 到 ±3.4×10³⁸ | 6-9 位小数 | 单精度浮点数 |
| `double` | 8 字节 | ±1.7×10⁻³⁰⁸ 到 ±1.7×10³⁰⁸ | 15-17 位小数 | 双精度浮点数 |
| `long double` | 8-16 字节 | 取决于平台 | 更高精度 | 扩展精度浮点数 |

### 1.3 **数据类型总结表**
| 类别 | 类型 | 说明 |
|------|------|------|
| **基本类型** | `bool` | 布尔值 |
| | `char`, `wchar_t`, `char16_t`, `char32_t` | 字符类型 |
| | `short`, `int`, `long`, `long long` | 有符号整型 |
| | `unsigned short`, `unsigned int`, ... | 无符号整型 |
| | `float`, `double`, `long double` | 浮点型 |
| | `void` | 无类型 |
| | `nullptr_t` | 空指针类型 |
| **复合类型** | 数组 | 相同类型元素的集合 |
| | 指针 | 存储内存地址 |
| | 引用 | 变量的别名 |
| | 枚举 | 命名常量集合 |
| **用户定义** | 结构体 | 数据成员的集合 |
| | 类 | 数据和方法的封装 |
| | 联合体 | 共享内存的不同类型 |
| **标准库** | `std::string` | 字符串类 |
| | `std::vector`, `std::list`, ... | 容器类 |
| | `std::unique_ptr`, `std::shared_ptr` | 智能指针 |
| | `std::function` | 函数包装器 |
| | `std::tuple`, `std::pair` | 元组类型 |
| **C++11/14/17** | `auto` | 自动类型推导 |
| | `decltype` | 获取表达式类型 |
| | `std::variant` | 类型安全联合 |
| | `std::optional` | 可选值 |
| | `std::any` | 任意类型 |




## 用法

```
// 初始化静态成员
const std::string Constants::KEY_DEGREE = "degree";

//extern 是一个关键字，主要用于声明变量或函数的外部链接属性，允许跨文件访问其他模块定义的全局变量或函数，常用于多文件编程中实现代码模块化。
extern int configValue;


//for (const auto& score : scores)
const：防止修改 scores 中的元素（只读访问）。
auto：自动推导元素类型（如 int、double 等）。
&：引用传递，避免拷贝（高效处理大对象）。

//std::vector<Constants::LineData>{data[0]}
std::vector<LineData>{data[0]}使用列表初始化语法（C++11+）创建一个包含data第一个元素的单元素vector。列表初始化{...}会调用LineData的拷贝构造函数，将data[0]复制到新vector中

```