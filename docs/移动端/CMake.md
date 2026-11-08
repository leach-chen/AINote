
# 一、CMake和MK区别

| 特性维度 | CMakeLists.txt (CMake) | Android.mk (NDK Build) |
| :--- | :--- | :--- |
| **构建系统** | **跨平台的CMake** | **Android NDK的旧式构建系统** |
| **语法风格** | 相对抽象，**跨平台**，**功能丰富** | 接近传统Makefile，**语法直接** |
| **依赖管理** | **自动或半自动**。提供`find_package`等命令。 | **手动配置**。需直接指定库路径和名称。 |
| **跨平台性** | **优秀**。一份配置可在多个平台生成对应的构建文件。 | **仅限于Android平台**使用。 |
| **适用场景** | **跨平台项目**；**复杂或大型项目**；OpenCV 4.x后的**推荐方式**。 | **遗留的Android NDK项目**；需要**精细控制**的简单模块。 |



# 二、CMake

## 2.1：语法
```
1、指定 CMake 的最低版本要求（cmake_minimum_required(VERSION <version>)）：
cmake_minimum_required(VERSION 3.10)

2、定义项目的名称和使用的编程语言（project(<project_name> [<language>...])）：
project(MyProject CXX)

3、指定要生成的可执行文件和其源文件，将main.cpp编译为MyExecutable（add_executable(<target> <source_files>...)）：
add_executable(MyExecutable main.cpp other_file.cpp)

4、创建一个库（静态库或动态库）及其源文件（add_library(<target> <source_files>...)）：
add_library(MyLibrary STATIC library.cpp)

5、将库链接到可执行文件，PUBLIC意味着MyExecutable使用了库的接口（target_link_libraries(<target> <libraries>...)）：
target_link_libraries(MyExecutable MyLibrary)

6、添加头文件搜索路径（include_directories(<dirs>...)）：
include_directories(${PROJECT_SOURCE_DIR}/include)

7、设置变量的值（set(<variable> <value>...)）：
set(CMAKE_CXX_STANDARD 11)

8、添加头文件搜索路径，PRIVATE表示仅MyExecutable需要这些头文件：
target_include_directories(TARGET target_name
                          [BEFORE | AFTER]
                          [SYSTEM] [PUBLIC | PRIVATE | INTERFACE]
                          [items1...])

target_include_directories(MyExecutable PRIVATE ${PROJECT_SOURCE_DIR}/include)

9、安装规则：
install(TARGETS target1 [target2 ...]
        [RUNTIME DESTINATION dir]
        [LIBRARY DESTINATION dir]
        [ARCHIVE DESTINATION dir]
        [INCLUDES DESTINATION [dir ...]]
        [PRIVATE_HEADER DESTINATION dir]
        [PUBLIC_HEADER DESTINATION dir])

install(TARGETS MyExecutable RUNTIME DESTINATION bin)

10、条件语句 (if, elseif, else, endif 命令)
if(expression)
  # Commands
elseif(expression)
  # Commands
else()
  # Commands
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  message("Debug build")
endif()


11、自定义命令 (add_custom_command 命令)：
add_custom_command(
   TARGET target
   PRE_BUILD | PRE_LINK | POST_BUILD
   COMMAND command1 [ARGS] [WORKING_DIRECTORY dir]
   [COMMAND command2 [ARGS]]
   [DEPENDS [depend1 [depend2 ...]]]
   [COMMENT comment]
   [VERBATIM]
)

add_custom_command(
   TARGET MyExecutable POST_BUILD
   COMMAND ${CMAKE_COMMAND} -E echo "Build completed."
)


12、设置库文件的输出目录
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)
```

### find_package

是用于查找和加载外部依赖库的核心工具，能够自动定位库文件并设置相关变量。

```
find_package(<PackageName> [version] [EXACT] [QUIET] [MODULE] [REQUIRED] 
    [[COMPONENTS] [components...]] [OPTIONAL_COMPONENTS components...]

REQUIRED：如果找不到指定库，CMake将报错并停止配置
QUIET：即使找不到库也不输出错误信息
EXACT：要求版本必须完全匹配
COMPONENTS：指定需要查找的库组件    

find_package(OpenCV REQUIRED)  # 必需找到OpenCV库
find_package(GTest)             # 查找GTest，找不到也不报错
```




## 2.2：系统变量

```
### 预定义变量  

# 工程的根目录  
PROJECT_SOURCE_DIR

# 运行cmake命令的目录,通常是 ${PROJECT_SOURCE_DIR}/build
PROJECT_BINARY_DIR

# 返回通过 project 命令定义的项目名称  
PROJECT_NAME

# CMakeLists.txt 所在的路径
CMAKE_CURRENT_SOURCE_DIR

# 编译目录
CMAKE_CURRENT_BINARY_DIR

# CMakeLists.txt 的完整路径  
CMAKE_CURRENT_LIST_DIR

# 当前所在的行  
CMAKE_CURRENT_LIST_LINE

# 定义自己的 cmake 模块所在的路径，然后可以用INCLUDE命令来调用自己的模块
CMAKE_MODULE_PATH
SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

# 重新定义目标二进制可执行文件的存放位置  
EXECUTABLE_OUTPUT_PATH

# 重新定义目标链接库文件的存放位置   
LIBRARY_OUTPUT_PATH


# 使用环境变量
$ENV{Name}
#写入环境变量
set(ENV{Name} value) # 这里没有“$”符号

# 系统信息  
# cmake 主版本号，比如 3.4.1 中的 3  
CMAKE_MAJOR_VERSION
# cmake 次版本号，比如 3.4.1 中的 4
­CMAKE_MINOR_VERSION
# cmake 补丁等级，比如 3.4.1 中的 1
­CMAKE_PATCH_VERSION
# 系统名称，比如 Linux-­2.6.22  
­CMAKE_SYSTEM  
# 不包含版本的系统名，比如 Linux
­CMAKE_SYSTEM_NAME
# 系统版本，比如 2.6.22
­CMAKE_SYSTEM_VERSION
# 处理器名称，比如 i686
­CMAKE_SYSTEM_PROCESSOR

# 在所有的类 UNIX 平台下该值为 TRUE，包括 OS X 和 cygwin  
­UNIX
# 在所有的 win32 平台下该值为 TRUE，包括 cygwin  
­WIN32

```


## CMake示例

```
MyProject/
├── CMakeLists.txt
├── src/
│   ├── main.cpp
│   ├── lib/
│   │   ├── module1.cpp
│   │   ├── module2.cpp
│   ├── include/
│       └── mylib.h
└── tests/
    ├── test_main.cpp
    └── CMakeLists.txt
1、创建 CMakeLists.txt 文件
1.1 根目录 CMakeLists.txt 文件
在 MyProject 根目录下创建一个 CMakeLists.txt 文件：

实例
cmake_minimum_required(VERSION 3.10)   # 指定最低 CMake 版本
project(MyProject VERSION 1.0)          # 定义项目名称和版本

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 包含头文件路径
include_directories(${PROJECT_SOURCE_DIR}/src/include)

# 添加子目录
add_subdirectory(src)
add_subdirectory(tests)
1.2 src 目录 CMakeLists.txt 文件
在 src 目录下创建一个 CMakeLists.txt 文件：

实例
# 创建库目标
add_library(MyLib STATIC
    lib/module1.cpp
    lib/module2.cpp
)

# 指定库的头文件
target_include_directories(MyLib PUBLIC ${CMAKE_SOURCE_DIR}/src/include)

# 创建可执行文件目标
add_executable(MyExecutable main.cpp)

# 链接库到可执行文件
target_link_libraries(MyExecutable PRIVATE MyLib)
1.3 tests 目录 CMakeLists.txt 文件
在 tests 目录下创建一个 CMakeLists.txt 文件：

实例
# 查找 GTest 包
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# 创建测试目标
add_executable(TestMyLib test_main.cpp)

# 链接库和 GTest 到测试目标
target_link_libraries(TestMyLib PRIVATE MyLib ${GTEST_LIBRARIES})
2、编写源代码和测试
以下是各个文件的代码：

2.1 src/main.cpp 文件代码
实例
#include <iostream>
#include "mylib.h"

int main() {
    std::cout << "Hello, CMake!" << std::endl;
    return 0;
}
2.2 src/lib/module1.cpp 文件代码
实例
#include "mylib.h"

// Implementation of module1
2.3 src/lib/module2.cpp 文件代码
实例
#include "mylib.h"

// Implementation of module2
2.4 src/include/mylib.h 文件代码
实例
#ifndef MYLIB_H
#define MYLIB_H

// Declarations of module functions

#endif // MYLIB_H
2.5 tests/test_main.cpp 文件代码
实例
#include <gtest/gtest.h>

// Test cases for MyLib
TEST(MyLibTest, BasicTest) {
    EXPECT_EQ(1, 1);
}
3、创建构建目录
在项目根目录下创建一个构建目录：

mkdir build
cd build
4、配置项目
在构建目录中运行 CMake 以配置项目：

cmake ..
5、编译项目
使用生成的构建系统文件进行编译，假设生成了 Makefile：

make
6、运行可执行文件
编译完成后，可以运行生成的可执行文件：

./MyExecutable
7、运行测试
使用生成的测试目标进行测试：

./TestMyLib
8、使用自定义命令和目标
8.1 自定义命令
在 src/CMakeLists.txt 文件中添加自定义命令：

add_custom_command(
    TARGET MyExecutable
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "Build complete!"
)
8.2 自定义目标
在 src/CMakeLists.txt 文件中添加自定义目标：

add_custom_target(run
    COMMAND ${CMAKE_BINARY_DIR}/MyExecutable
    DEPENDS MyExecutable
)
运行自定义目标：

make run
9、跨平台和交叉编译
9.1 指定平台
如果需要指定平台进行构建，可以在运行 CMake 时指定平台：

cmake -DCMAKE_SYSTEM_NAME=Linux ..
9.2 使用工具链文件
创建一个工具链文件 toolchain.cmake：

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
使用工具链文件进行构建：

cmake -DCMAKE_TOOLCHAIN_FILE=toolchain.cmake ..
```

```
MyProject/                      # 项目根目录
├── CMakeLists.txt              # 【根】全局设置，引入子目录
├── app/
│   ├── CMakeLists.txt          # 【应用】生成最终的可执行文件
│   └── main.cpp
├── libs/
│   ├── math/                   # 【数学库模块】
│   │   ├── CMakeLists.txt      # 定义 math 静态库/动态库
│   │   ├── include/math.h
│   │   └── src/*.cpp
│   └── logger/                 # 【日志库模块】
│       ├── CMakeLists.txt      # 定义 logger 库
│       ├── include/logger.h
│       └── src/*.cpp
└── tests/                      # 【测试模块】
    ├── CMakeLists.txt          # 定义测试可执行文件，链接 math 和 logger
    └── test_math.cpp


# 根 CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyAwesomeApp)

add_subdirectory(src)          # 主应用程序
add_subdirectory(libs/core)    # 核心库
add_subdirectory(libs/utils)   # 工具库
add_subdirectory(tests)        # 测试模块


# libs/math/CMakeLists.txt
add_library(math STATIC src/calculator.cpp) # 定义math库
target_include_directories(math PUBLIC include) # 头文件路径，PUBLIC属性会传递给使用者

# app/CMakeLists.txt
add_executable(MyApp main.cpp)
target_link_libraries(MyApp PRIVATE math) # 链接math库
# 链接后，MyApp会自动获得math的公共头文件路径，无需手动写 include_directories
```