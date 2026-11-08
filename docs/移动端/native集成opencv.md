在Android Studio的C++项目中引入OpenCV，主要有三种方式：通过Maven Central引入、使用OpenCV Android SDK，或者从源码编译。我将以最常用的**OpenCV Android SDK**方式为例，为你说明具体步骤，并补充其他方式的选择建议。

### 🔧 使用 OpenCV Android SDK

这是目前较为通用和灵活的方法，适合大多数需要C++ Native (JNI) 开发的场景。

1.  **获取 SDK 并导入模块**
    *   从OpenCV官网下载对应版本的**OpenCV Android SDK**。
    *   在Android Studio中，点击 `File -> New -> Import Module`，选择SDK解压路径下的 `sdk/java` 文件夹。
    *   导入后，建议将模块名统一改为简洁的 `:opencv`（在导入第二步可修改）。

2.  **添加模块依赖**
    *   点击 `File -> Project Structure`。
    *   在 `Dependencies` 选项卡下，选择你的 **app module**，点击 `+` 号，添加 `Module Dependency`，选择刚才导入的OpenCV模块（如 `:opencv`）。

3.  **配置 NDK 和 CMake**
    确保你的项目已配置NDK和CMake。在 `app/build.gradle` 文件的 `defaultConfig` 块中检查：
    ```groovy
    android {
        ...
        defaultConfig {
            ...
            externalNativeBuild {
                cmake {
                    cppFlags "-std=c++11 -frtti -fexceptions" // 推荐添加的编译选项
                    // 指定ABI，根据需要筛选，有助于减小APK体积
                    abiFilters 'arm64-v8a', 'armeabi-v7a'
                }
            }
        }
    }
    ```
    关于ABI过滤，你可以根据项目需求选择适用的架构。

4.  **准备 native libs 并配置 CMakeLists.txt**
    *   将SDK包中 `OpenCV-android-sdk/sdk/native/libs` 目录下的所有子文件夹（每个对应一种ABI架构）复制到你的项目 `app/src/main` 目录下，并将该文件夹重命名为 **`jniLibs`**。这样Gradle在构建时就会自动将这些本地库打包进APK。
    *   配置你项目 `app` 目录下的 `CMakeLists.txt` 文件，关键配置如下：
    ```cmake
    cmake_minimum_required(VERSION 3.6.0)
    
    # 设置OpenCV的路径，请根据你的实际下载和解压路径修改
    set(OPENCV_ROOT_DIR ${CMAKE_SOURCE_DIR}/../../../OpenCV-android-sdk) # 示例路径
    set(OPENCV_ANDROID_DIR ${OPENCV_ROOT_DIR}/sdk/native)
    
    # 添加头文件包含目录
    include_directories(${OPENCV_ANDROID_DIR}/jni/include)
    
    # 动态方式加载OpenCV本地库
    add_library(lib_opencv SHARED IMPORTED)
    # 设置目标属性，链接到.so文件
    set_target_properties(lib_opencv PROPERTIES
        IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/src/main/jniLibs/${ANDROID_ABI}/libopencv_java4.so) # 注意.so文件名可能随版本变化
    
    # 你的本地库
    add_library(native-lib SHARED native-lib.cpp)
    
    # 链接OpenCV库到你的目标库
    target_link_libraries(native-lib
        lib_opencv
        # 其他需要的库...
        ${log-lib})
    ```
    注意：`libopencv_java4.so` 的文件名可能因OpenCV版本而异（如可能是`libopencv_java3.so`），请以 `jniLibs` 目录下实际文件名为准。

5.  **在代码中加载 OpenCV 库**
    在你的Java代码（例如`MainActivity`）中，需要显式加载OpenCV库：
    ```java
    public class MainActivity extends AppCompatActivity {
        static {
            // 加载OpenCV本地库，库名可能随版本变化，通常是"opencv_java4"
            System.loadLibrary("opencv_java4");
        }
        // ... 其他代码
    }
    ```
    如果一切配置正确，你就可以在C++源文件（如`native-lib.cpp`）中包含OpenCV头文件并使用其功能了。
    ```cpp
    #include <jni.h>
    #include <string>
    #include <opencv2/opencv.hpp>
    // ... 其他代码
    ```

### 💡 其他集成方式与选择建议

*   **通过 Maven Central 引入**
    这是**最简单**的方式。只需在`app/build.gradle`的`dependencies`中添加一行依赖：
    ```groovy
    dependencies {
        implementation 'org.opencv:opencv:4.9.0' // 检查并使用最新版本
    }
    ```
    这种方式由OpenCV官方维护，Android Studio和Gradle原生支持，适合**初学者**或主要使用Java接口、不需要高级构建选项的项目。但对于复杂的C++ JNI开发，灵活性可能不如SDK方式。

*   **从源代码编译**
    这种方式可以获取最新功能并进行深度定制，但过程复杂，**不推荐大多数开发者**使用。

### 🚨 注意事项

*   **ABI 兼容性**：配置`abiFilters`时，需确保与你准备的`jniLibs`架构目录以及设备架构兼容。
*   **版本匹配**：尽量保证OpenCV库版本、NDK版本以及CMake版本的兼容性。使用较新的OpenCV版本时，推荐使用NDK r18或更新版本。
*   **权限与特性**：如果使用相机等硬件功能，别忘了在`AndroidManifest.xml`中添加相应权限声明（如`<uses-permission android:name="android.permission.CAMERA" />`）和硬件特性声明。
*   **APK 体积**：OpenCV库会显著增加APK体积（通常增加10MB以上）。可通过只引入所需模块（从源码编译时）或使用ABI过滤来缓解。

### 💎 总结

总的来说，在Android Studio C++项目中引入OpenCV，**对于大多数JNI C++开发，推荐使用 OpenCV Android SDK 的方式**。若你追求快速简便且主要使用Java接口，可以尝试 **Maven Central** 方式。

希望这些步骤能帮助你顺利完成配置。如果在实际操作中遇到问题，比如具体的错误提示，欢迎随时提出。