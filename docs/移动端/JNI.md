

# 一、常用方法

## 1、基础操作类方法

### 1.1 类操作
```c
// 查找类
jclass FindClass(JNIEnv *env, const char *name);
// 示例：
jclass stringClass = env->FindClass("java/lang/String");
jclass myClass = env->FindClass("com/example/MyClass");

// 获取对象类
jclass GetObjectClass(JNIEnv *env, jobject obj);
// 示例：
jclass objClass = env->GetObjectClass(myObject);

// 获取父类
jclass GetSuperclass(JNIEnv *env, jclass sub);
// 示例：
jclass superClass = env->GetSuperclass(subClass);
```

### 1.2 方法操作
```c
// 获取方法ID
jmethodID GetMethodID(JNIEnv *env, jclass clazz, 
                     const char *name, const char *sig);
// 示例：
jmethodID methodId = env->GetMethodID(clazz, "add", "(II)I");

// 获取静态方法ID
jmethodID GetStaticMethodID(JNIEnv *env, jclass clazz,
                           const char *name, const char *sig);
// 示例：
jmethodID staticMethodId = env->GetStaticMethodID(clazz, "getInstance", "()Lcom/example/MyClass;");

// 调用方法（根据返回类型选择）
void CallVoidMethod(JNIEnv *env, jobject obj, jmethodID methodID, ...);
jint CallIntMethod(JNIEnv *env, jobject obj, jmethodID methodID, ...);
jobject CallObjectMethod(JNIEnv *env, jobject obj, jmethodID methodID, ...);
// 示例：
env->CallVoidMethod(obj, methodId, arg1, arg2);
jint result = env->CallIntMethod(obj, methodId, 10, 20);
jstring strResult = (jstring)env->CallObjectMethod(obj, methodId, arg1);

// 调用静态方法
void CallStaticVoidMethod(JNIEnv *env, jclass clazz, 
                         jmethodID methodID, ...);
jint CallStaticIntMethod(JNIEnv *env, jclass clazz, 
                        jmethodID methodID, ...);
// 示例：
env->CallStaticVoidMethod(clazz, staticMethodId);
jint value = env->CallStaticIntMethod(clazz, staticMethodId);
```

## 2、字段操作类方法

### 2.1 字段访问
```c
// 获取字段ID
jfieldID GetFieldID(JNIEnv *env, jclass clazz, 
                   const char *name, const char *sig);
// 示例：
jfieldID nameField = env->GetFieldID(clazz, "name", "Ljava/lang/String;");
jfieldID ageField = env->GetFieldID(clazz, "age", "I");

// 获取静态字段ID
jfieldID GetStaticFieldID(JNIEnv *env, jclass clazz,
                         const char *name, const char *sig);

// 获取/设置字段值
jobject GetObjectField(JNIEnv *env, jobject obj, jfieldID fieldID);
jint GetIntField(JNIEnv *env, jobject obj, jfieldID fieldID);
void SetObjectField(JNIEnv *env, jobject obj, jfieldID fieldID, jobject value);
void SetIntField(JNIEnv *env, jobject obj, jfieldID fieldID, jint value);
// 示例：
jstring name = (jstring)env->GetObjectField(obj, nameField);
jint age = env->GetIntField(obj, ageField);
env->SetIntField(obj, ageField, 30);
```

## 3、字符串操作方法

### 3.1 字符串转换
```c
// UTF-8 字符串操作
const char* GetStringUTFChars(JNIEnv *env, jstring str, jboolean *isCopy);
void ReleaseStringUTFChars(JNIEnv *env, jstring str, const char* chars);
// 示例：
const char* cstr = env->GetStringUTFChars(jstr, NULL);
// 使用 cstr...
env->ReleaseStringUTFChars(jstr, cstr);

// 创建新字符串
jstring NewStringUTF(JNIEnv *env, const char* bytes);
// 示例：
jstring newStr = env->NewStringUTF("Hello World");

// 获取字符串长度
jsize GetStringLength(JNIEnv *env, jstring str);  // Unicode字符数
jsize GetStringUTFLength(JNIEnv *env, jstring str); // UTF-8字节数

// Unicode 字符串操作（用于处理非ASCII字符）
const jchar* GetStringChars(JNIEnv *env, jstring str, jboolean *isCopy);
void ReleaseStringChars(JNIEnv *env, jstring str, const jchar* chars);
jstring NewString(JNIEnv *env, const jchar* unicodeChars, jsize len);
```

## 4、数组操作方法

### 4.1 基本类型数组
```c
// 获取数组长度
jsize GetArrayLength(JNIEnv *env, jarray array);

// 创建新数组
jintArray NewIntArray(JNIEnv *env, jsize length);
jfloatArray NewFloatArray(JNIEnv *env, jsize length);
jobjectArray NewObjectArray(JNIEnv *env, jsize length, 
                           jclass elementClass, jobject initialElement);

// 获取数组元素指针（用于高效操作）
jint* GetIntArrayElements(JNIEnv *env, jintArray array, jboolean *isCopy);
jfloat* GetFloatArrayElements(JNIEnv *env, jfloatArray array, jboolean *isCopy);
// 示例：
jint* elements = env->GetIntArrayElements(intArray, NULL);
for (int i = 0; i < length; i++) {
    elements[i] *= 2;
}
env->ReleaseIntArrayElements(intArray, elements, 0);

// 释放数组元素
void ReleaseIntArrayElements(JNIEnv *env, jintArray array, 
                            jint* elems, jint mode);
// mode参数：
// 0: 复制回内容并释放elems缓冲区
// JNI_COMMIT: 复制回内容但不释放缓冲区
// JNI_ABORT: 不复制回内容但释放缓冲区

// 区域操作（用于部分数组操作）
void SetIntArrayRegion(JNIEnv *env, jintArray array, jsize start, 
                      jsize len, const jint* buf);
void GetIntArrayRegion(JNIEnv *env, jintArray array, jsize start,
                      jsize len, jint* buf);
// 示例：
jint buffer[10];
env->GetIntArrayRegion(array, 0, 10, buffer);
```

### 4.2 对象数组
```c
// 获取/设置对象数组元素
jobject GetObjectArrayElement(JNIEnv *env, jobjectArray array, jsize index);
void SetObjectArrayElement(JNIEnv *env, jobjectArray array, 
                          jsize index, jobject value);
// 示例：
for (int i = 0; i < length; i++) {
    jstring element = (jstring)env->GetObjectArrayElement(strArray, i);
    // 处理element...
}
```

## 5、引用操作方法

### 5.1 引用管理
```c
// 创建全局引用
jobject NewGlobalRef(JNIEnv *env, jobject obj);
void DeleteGlobalRef(JNIEnv *env, jobject globalRef);
// 示例：
jobject globalObj = env->NewGlobalRef(localObj);
// 在多线程中使用...
env->DeleteGlobalRef(globalObj);

// 创建弱全局引用
jobject NewWeakGlobalRef(JNIEnv *env, jobject obj);
void DeleteWeakGlobalRef(JNIEnv *env, jobject obj);

// 检查弱引用是否有效
jboolean IsSameObject(JNIEnv *env, jobject ref1, jobject ref2);
// 示例：
if (env->IsSameObject(weakRef, NULL)) {
    // 弱引用已被垃圾回收
}

// 创建局部引用
jobject NewLocalRef(JNIEnv *env, jobject ref);
void DeleteLocalRef(JNIEnv *env, jobject localRef);
// 示例：
jobject localCopy = env->NewLocalRef(globalRef);
// 使用...
env->DeleteLocalRef(localCopy);

// 确保局部引用容量
jint EnsureLocalCapacity(JNIEnv *env, jint capacity);
// 示例：
if (env->EnsureLocalCapacity(100) == 0) {
    // 可以安全创建100个局部引用
}
```

## 6、异常处理方法

### 6.1 异常检测和处理
```c
// 检查异常
jthrowable ExceptionOccurred(JNIEnv *env);
// 示例：
if (env->ExceptionCheck()) {
    // 有异常发生
}

// 更简洁的检查
jboolean ExceptionCheck(JNIEnv *env);
// 示例：
if (env->ExceptionCheck()) {
    env->ExceptionClear();
    return;
}

// 获取异常描述
void ExceptionDescribe(JNIEnv *env);

// 清除异常
void ExceptionClear(JNIEnv *env);

// 抛出异常
jint Throw(JNIEnv *env, jthrowable obj);
jint ThrowNew(JNIEnv *env, jclass clazz, const char* message);
// 示例：
jclass excClass = env->FindClass("java/lang/IllegalArgumentException");
env->ThrowNew(excClass, "Invalid argument");

// 创建异常对象
jthrowable ExceptionOccurred(JNIEnv *env);
// 示例：
jthrowable exc = env->ExceptionOccurred();
if (exc) {
    env->ExceptionDescribe();
    env->ExceptionClear();
}
```

## 7、类型转换方法

### 7.1 基本类型转换
```c
// 字符串与基本类型转换
jint GetStringUTFLength(JNIEnv *env, jstring str);
const char* GetStringUTFChars(JNIEnv *env, jstring str, jboolean* isCopy);
void ReleaseStringUTFChars(JNIEnv *env, jstring str, const char* chars);

// 获取方法签名
const char* GetStringUTFChars(JNIEnv *env, jstring str, jboolean* isCopy);
```

## 8、JVM操作方法

### 8.1 JVM交互
```c
// 获取JavaVM实例（通常在JNI_OnLoad中保存）
jint GetJavaVM(JNIEnv *env, JavaVM** vm);
// 示例：
JavaVM* g_vm;
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved) {
    g_vm = vm;
    // 保存到全局变量
    return JNI_VERSION_1_8;
}

// 获取JNIEnv（用于非JNI线程）
jint AttachCurrentThread(JavaVM* vm, void** penv, void* args);
jint DetachCurrentThread(JavaVM* vm);

// 获取JNI版本
jint GetVersion(JNIEnv *env);
// 示例：
jint version = env->GetVersion();
```

## 9、监控操作方法

### 9.1 同步操作
```c
// 进入监视器（类似synchronized）
jint MonitorEnter(JNIEnv *env, jobject obj);
// 示例：
if (env->MonitorEnter(obj) == JNI_OK) {
    // 同步代码块
    env->MonitorExit(obj);
}

// 退出监视器
jint MonitorExit(JNIEnv *env, jobject obj);
```

## 10、直接缓冲区方法

### 10.1 NIO直接缓冲区操作
```c
// 获取直接缓冲区地址
void* GetDirectBufferAddress(JNIEnv *env, jobject buf);
// 示例：
void* buffer = env->GetDirectBufferAddress(directBuffer);
if (buffer != NULL) {
    // 直接操作内存
}

// 获取直接缓冲区容量
jlong GetDirectBufferCapacity(JNIEnv *env, jobject buf);
```

## 11、反射操作方法

### 11.1 反射支持
```c
// 从类获取名称
jstring GetClassName(JNIEnv *env, jclass clazz);
// 或通过反射API：
jclass classClass = env->FindClass("java/lang/Class");
jmethodID getNameMethod = env->GetMethodID(classClass, "getName", "()Ljava/lang/String;");
jstring className = (jstring)env->CallObjectMethod(clazz, getNameMethod);

// 判断实例类型
jboolean IsInstanceOf(JNIEnv *env, jobject obj, jclass clazz);
// 示例：
jclass stringClass = env->FindClass("java/lang/String");
if (env->IsInstanceOf(obj, stringClass)) {
    // obj是String类型
}

// 判断赋值兼容性
jboolean IsAssignableFrom(JNIEnv *env, jclass sub, jclass sup);
// 示例：
if (env->IsAssignableFrom(subClass, superClass)) {
    // subClass可以赋值给superClass
}
```

## 12、常用实用模式

### 12.1 字符串处理模板
```c
jstring JNICALL nativeProcessString(JNIEnv* env, jobject obj, jstring input) {
    const char* cstr = NULL;
    jstring result = NULL;
    
    cstr = env->GetStringUTFChars(input, NULL);
    if (cstr == NULL) {
        // 内存不足
        return NULL;
    }
    
    try {
        // 处理字符串
        char buffer[256];
        snprintf(buffer, sizeof(buffer), "Processed: %s", cstr);
        result = env->NewStringUTF(buffer);
    } catch (...) {
        // 异常处理
    }
    
    // 确保释放资源
    if (cstr != NULL) {
        env->ReleaseStringUTFChars(input, cstr);
    }
    
    return result;
}
```

### 12.2 数组处理模板
```c
jintArray JNICALL nativeProcessArray(JNIEnv* env, jobject obj, jintArray input) {
    jint* elements = NULL;
    jintArray result = NULL;
    
    jsize length = env->GetArrayLength(input);
    elements = env->GetIntArrayElements(input, NULL);
    if (elements == NULL) {
        return NULL;
    }
    
    try {
        // 创建结果数组
        result = env->NewIntArray(length);
        if (result == NULL) {
            throw std::bad_alloc();
        }
        
        // 处理数据
        jint* temp = new jint[length];
        for (int i = 0; i < length; i++) {
            temp[i] = elements[i] * 2;
        }
        
        // 设置结果
        env->SetIntArrayRegion(result, 0, length, temp);
        delete[] temp;
    } catch (...) {
        // 清理
        if (result != NULL) {
            env->DeleteLocalRef(result);
            result = NULL;
        }
    }
    
    // 释放输入数组
    if (elements != NULL) {
        env->ReleaseIntArrayElements(input, elements, JNI_ABORT);
    }
    
    return result;
}
```

### 12.3 对象操作模板
```c
void JNICALL nativeProcessObject(JNIEnv* env, jobject obj, jobject dataObj) {
    // 获取类
    jclass dataClass = env->GetObjectClass(dataObj);
    if (dataClass == NULL) {
        return;
    }
    
    // 获取字段ID（缓存这些ID以提高性能）
    static jfieldID valueField = NULL;
    static jmethodID processMethod = NULL;
    
    if (valueField == NULL) {
        valueField = env->GetFieldID(dataClass, "value", "I");
        processMethod = env->GetMethodID(dataClass, "process", "()V");
        
        // 检查是否成功获取
        if (valueField == NULL || processMethod == NULL) {
            env->ExceptionClear();  // 清除NoSuchField/MethodError
            return;
        }
    }
    
    // 获取和设置字段
    jint value = env->GetIntField(dataObj, valueField);
    env->SetIntField(dataObj, valueField, value + 1);
    
    // 调用方法
    env->CallVoidMethod(dataObj, processMethod);
    
    // 检查异常
    if (env->ExceptionCheck()) {
        env->ExceptionDescribe();
        env->ExceptionClear();
    }
}
```

## 13、性能优化方法

### 13.1 ID缓存模式
```c
class JNICache {
private:
    JavaVM* jvm;
    jclass targetClass;
    jmethodID processMethod;
    jfieldID dataField;
    
public:
    JNICache() : targetClass(NULL), processMethod(NULL), dataField(NULL) {}
    
    bool init(JNIEnv* env) {
        targetClass = env->FindClass("com/example/TargetClass");
        if (targetClass == NULL) return false;
        
        // 转换为全局引用以便重用
        targetClass = (jclass)env->NewGlobalRef(targetClass);
        
        processMethod = env->GetMethodID(targetClass, "process", "()V");
        dataField = env->GetFieldID(targetClass, "data", "Ljava/lang/String;");
        
        return (processMethod != NULL && dataField != NULL);
    }
    
    void cleanup(JNIEnv* env) {
        if (targetClass != NULL) {
            env->DeleteGlobalRef(targetClass);
            targetClass = NULL;
        }
    }
    
    void process(JNIEnv* env, jobject obj) {
        if (processMethod != NULL) {
            env->CallVoidMethod(obj, processMethod);
        }
    }
};

// 全局缓存实例
static JNICache g_cache;

JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved) {
    JNIEnv* env;
    if (vm->GetEnv((void**)&env, JNI_VERSION_1_8) != JNI_OK) {
        return JNI_ERR;
    }
    
    if (!g_cache.init(env)) {
        return JNI_ERR;
    }
    
    return JNI_VERSION_1_8;
}
```

## 14、线程安全方法

### 14.1 多线程JNI操作
```c
JavaVM* g_jvm;

class JNIThreadSafe {
private:
    JNIEnv* env;
    bool attached;
    
public:
    JNIThreadSafe() : env(NULL), attached(false) {
        // 获取JNIEnv，如果需要则附加线程
        jint result = g_jvm->GetEnv((void**)&env, JNI_VERSION_1_8);
        if (result == JNI_EDETACHED) {
            // 线程未附加，附加它
            JavaVMAttachArgs args = {JNI_VERSION_1_8, NULL, NULL};
            result = g_jvm->AttachCurrentThread((void**)&env, &args);
            if (result == JNI_OK) {
                attached = true;
            }
        }
    }
    
    ~JNIThreadSafe() {
        if (attached) {
            g_jvm->DetachCurrentThread();
        }
    }
    
    JNIEnv* getEnv() { return env; }
    bool isValid() { return env != NULL; }
};

void nativeThreadFunction() {
    JNIThreadSafe jni;
    if (!jni.isValid()) {
        return;
    }
    
    JNIEnv* env = jni.getEnv();
    // 执行JNI操作...
}
```

## 15、错误处理辅助方法

### 15.1 安全检查宏
```c
#define CHECK_EXCEPTION(env) \
    if ((env)->ExceptionCheck()) { \
        (env)->ExceptionDescribe(); \
        (env)->ExceptionClear(); \
        return; \
    }

#define CHECK_EXCEPTION_RETURN(env, ret) \
    if ((env)->ExceptionCheck()) { \
        (env)->ExceptionDescribe(); \
        (env)->ExceptionClear(); \
        return ret; \
    }

#define CHECK_NULL(ptr, env, ret) \
    if ((ptr) == NULL) { \
        jclass exc = (env)->FindClass("java/lang/OutOfMemoryError"); \
        if (exc != NULL) { \
            (env)->ThrowNew(exc, "Memory allocation failed"); \
        } \
        return ret; \
    }
```

### 15.2 资源自动管理类
```c
class JNIStringGuard {
private:
    JNIEnv* env;
    jstring jstr;
    const char* cstr;
    
public:
    JNIStringGuard(JNIEnv* e, jstring s) : env(e), jstr(s), cstr(NULL) {
        if (jstr != NULL) {
            cstr = env->GetStringUTFChars(jstr, NULL);
        }
    }
    
    ~JNIStringGuard() {
        if (cstr != NULL && jstr != NULL) {
            env->ReleaseStringUTFChars(jstr, cstr);
        }
    }
    
    const char* get() const { return cstr; }
    operator bool() const { return cstr != NULL; }
};

// 使用示例：
void example(JNIEnv* env, jstring input) {
    JNIStringGuard guard(env, input);
    if (!guard) return;
    
    printf("String: %s\n", guard.get());
    // 自动释放，无需手动调用ReleaseStringUTFChars
}
```




# 二、参数说明

### 参数

> JNIEXPORT jstring JNICALL Java_com_leachchen_testjni_MainActivity_testMethod(JNIEnv *env, jobject instance, jstring name_)

```
Java是函数的前缀，com_leachchen_testjni_MainActivity是函数所在类路径，testMethod是方法名；

第一个参数：JNIEnv* 是定义任意native函数的第一个参数（包括调用JNI的RegisterNatives函数注册的函数），指向JVM函数表的指针，函数表中的每一个入口指向一个JNI函数，每个函数用于访问JVM中特定的数据结构。

第二个参数：调用java中native方法的实例或Class对象，如果这个native方法是实例方法，则该参数是jobject，如果是静态方法，则是jclass

第三个参数：Java对应JNI中的数据类型，Java中String类型对应JNI的jstring类型。

返回值：JNIEXPORT和JNICALL宏中间的jstring，表示函数的返回值类型，对应Java的String类型
```

## 参数理解

### **函数参数 (JNIEnv \*env, jobject instance )理解**

基本类型很容易理解，就是对C/C++中的基本类型用typedef重新定义了一个新的名字，在JNI中可以直接访问。
JNI把Java中的所有对象当作一个C指针传递到本地方法中，这个指针指向JVM中的内部数据结构，而内部的数据结构在内存中的存储方式是不可见的。只能从JNIEnv指针指向的函数表中选择合适的JNI函数来操作JVM中的数据结构。如访问java.lang.String对应的JNI类型jstring时，没有像访问基本数据类型一样直接使用，因为它在Java是一个引用类型，所以在本地代码中只能通过GetStringUTFChars这样的JNI函数来访问字符串的内容。如：

> testMethod(JNIEnv \*env, jobject instance, jstring name\_)

Java内部的数据结构（除基本数据类型外）对JNI来说是不可见的，如上面函数中，Java传递过来了一个字符串类型的name\_变量，name\_变量在JVM中的数据结构对JNI来说是不可见的，那JNI如何访问到这个变量呢？\*env指针指向的函数表中的GetStringUTFChars变能访问到JVM中的数据结构，调用GetStringUTFChars可以获取到该字符串的值，然后再赋值给JNI中的变量，这样便完成了JAVA-》JNI的一个传值过程。若JNI想返回一个字符串给JAVA，那么需要调用NewStringUTF，将JNI中的字符串，包装成符合JAVA字符串数据结构，的字符串，然后返回JVM便能够识别到了。

jobject instance<br>
如果native方法不是static的话，这个obj就代表这个native方法的类实例
如果native方法是static的话，这个obj就代表这个native方法的类的class对象实例(static方法不需要类实例的，所以就代表这个类的class对象)

### **调用GetStringUTFChars后需要调用ReleaseStringUTFChars**

在调用GetStringUTFChars函数从JVM内部获取一个字符串之后，JVM内部会分配一块新的内存，用于存储源字符串的拷贝，以便本地代码访问和修改。即然有内存分配，用完之后马上释放是一个编程的好习惯。通过调用ReleaseStringUTFChars函数通知JVM这块内存已经不使用了，你可以清除了。注意：这两个函数是配对使用的，用了GetXXX就必须调用ReleaseXXX，而且这两个函数的命名也有规律，除了前面的Get和Release之外，后面的都一样。



<br>

# 三、数据类型

### **基本数据类型**

| Java Type | Native type |    Description   |
| :-------: | :---------: | :--------------: |
|  boolean  |   jboolean  |  unsigned 8 bits |
|    byte   |    jbyte    |   signed 8 bits  |
|    char   |    jchar    | unsigned 16 bits |
|   short   |    jshort   |  signed 16 bits  |
|    int    |     jint    |  signed 32 bits  |
|    long   |    jlong    |  signed 64 bits  |
|   float   |    jfloat   |      32 bits     |
|   double  |   jdouble   |      64 bits     |

### **引用类型**

|          Java Type          |  Native type  | Description |
| :-------------------------: | :-----------: | :---------: |
|          all object         |    jobject    |             |
|  java.lang.Class instances  |    jstring    |             |
|            arrays           |     jarray    |             |
|          Object\[]          |  jobjectArray |             |
|          boolean\[]         | jbooleanArray |             |
|           byte\[]           |   jbyteArray  |             |
|           char\[]           |   jcharArray  |             |
|            int\[]           |   jintArray   |             |
|           long\[]           |   jlongArray  |             |
|           float\[]          |  jfloatAyyay  |             |
|          double\[]          |  jdoubleArray |             |
| java.lang.Throwable Objects |   jthrowable  |             |

<br>

# 四、描述符

### **类描述符**

类描述符用来表示一个类或者接口的名字。把类或者接口在java中所定义的完整名称中的"."替换成"/"就是类描述符。<br>
比如java.lang.String的类描述符为：**java/lang/string**<br>
数组类的描述符：在"\["后面跟着数组元素的类型的字段描述符,如：<br>
**"int\[]"**的类描述符为：**"\[I"**<br>
**"double\[]\[]\[]"**的类描述符为：**"\[\[\[D"**<br>

#### **字段描述符:**

| Java Type | Native type |
| :-------: | :---------: |
|  boolean  |      Z      |
|    byte   |      B      |
|    char   |      C      |
|   short   |      S      |
|    int    |      I      |
|    long   |      J      |
|   float   |      F      |
|   double  |      D      |

引用类型的字段描述符的第一个字符是”L”，接着写类描述符，最后以”;”结尾。<br>
数组类型的字段描述符的定义规则和数组类描述符一致。 <br>
下面的例子是引用类型的字段描述符和他们相对应的java类型：<br>

| Java Type |       Native type      |
| :-------: | :--------------------: |
|   String  |  "Ljava/lang/String;"  |
|   int\[]  |          "\[I"         |
| Object\[] | "\[Ljava/lang/Object;" |

### **方法描述符**

*   方法描述符首先在”()”中写所有的参数类型的字段描述符，然后在”()”后面接着写返回类型的字段描述符。
*   并且在参数类型的字段描述符之间不能有空格或者其他分隔符。
*   "V"用来表示没有返回类型。
*   构造函数使用”V”做为返回类型，并且使用”< init>”做为函数名。

|        Java Type        |       Native type       |
| :---------------------: | :---------------------: |
|       String f();       |  "()Ljava/lang/String;" |
| long f(int i, Class c); | "(ILjava/lang/Class;)J" |
|  String(byte\[] bytes); |         "(\[B)V"        |



# 五、注册方式

### 静态动态注册

静态注册方式(函数名为JAVA_包名_类名_方法名组成):

```
JNIEXPORT jstring JNICALL Java_com_leachchen_testjni_MainActivity_testMethod(JNIEnv *env, jobject instance, jstring name_) {
	const char *name = (*env)->GetStringUTFChars(env, name_, 0);
	char buff[128] = {0};
	sprintf(buff,"I am from C part String and get java part String:%s",name);
	(*env)->ReleaseStringUTFChars(env, name_, name);

	return (*env)->NewStringUTF(env, buff);
}
```

### 动态注册方式

指定包名路径，然后可以自定义函数名称与native名称映射

1: 指定java里面的native方法所在类的路径#define CLASS_PATH_NAME	 "com/leachchen/testjni/MainActivity";

2: 重写JNI_OnLoad方法:

3: 在JNINativeMethod里面将java里面的native方法及jni里面的方法映射;

4: 实现java要调用的方法jstring testJniMethod(JNIEnv *env, jobject instance, jstring name_)；

```
#include <stdio.h>
#include <jni.h>
#include <iostream>
using namespace std;

#define CLASS_PATH_NAME	 "com/leachchen/testjni/MainActivity"

/**
 * 静态注册方式
 */
/*extern "C" JNIEXPORT jstring JNICALL
Java_com_leachchen_testjni_MainActivity_testMethod(JNIEnv *env, jobject instance, jstring name_) {
	const char *name = env->GetStringUTFChars(name_, 0);
	char buff[128] = {0};
	sprintf(buff,"I am from C part String and get java part String:%s",name);
	env->ReleaseStringUTFChars(name_, name);

	return env->NewStringUTF(buff);
}*/

/**
 * 动态注册方式
 */
jstring testJniMethod(JNIEnv *env, jobject instance, jstring name_) {
	const char *name = env->GetStringUTFChars(name_, 0);
	char buff[128] = {0};
	sprintf(buff,"I am from C part String and get java part String:%s",name);
	env->ReleaseStringUTFChars(name_, name);

	return env->NewStringUTF(buff);
}


//注册Java端的方法以及本地相对应的方法
JNINativeMethod method[]={
	{
		  "testMethod", //Java中native函数的函数名
		  "(Ljava/lang/String;)Ljava/lang/String;", // Java中的native对应的native签名
		  (void *)testJniMethod //native 中的方法指针
	 }
};

//注册相应的类以及方法
jint registerNativeMeth(JNIEnv *env){
	jclass cl=env->FindClass(CLASS_PATH_NAME);
	if((env->RegisterNatives(cl,method,sizeof(method)/sizeof(method[0])))<0){
		return -1;
	}
	return 0;
}

//实现jni_onload 动态注册方法
jint JNI_OnLoad(JavaVM* vm, void* reserved) {
	JNIEnv* env = NULL;
	if (vm->GetEnv((void**) &env, JNI_VERSION_1_4) != JNI_OK) {
		return -1;
	}
	if(registerNativeMeth(env)!=JNI_OK){//注册方法
		return -1;
	}
	return JNI_VERSION_1_4;//必须返回这个值
}
```

六、示例

```

Android:
external fun processImageWithText(width: Int, height: Int, data: ByteArray, text: String): ByteArray

jni:
// 获取输入数据
jsize data_len = env->GetArrayLength(data);
jbyte* inputData = env->GetByteArrayElements(data, nullptr);
// 释放资源
env->ReleaseByteArrayElements(data, inputData, JNI_ABORT);


Android:
external fun predict(imageData: ImageData):ByteArray

jni:
// 获取Java类和字段ID
jclass cls = env->GetObjectClass(imageData);
jfieldID fidWidth = env->GetFieldID(cls, "width", "I");
jfieldID fidHeight = env->GetFieldID(cls, "height", "I");
jfieldID fidChannels = env->GetFieldID(cls, "channels", "I");
jfieldID fidData = env->GetFieldID(cls, "data", "[B");

// 提取字段值
int width = env->GetIntField(imageData, fidWidth);
int height = env->GetIntField(imageData, fidHeight);
int channels = env->GetIntField(imageData, fidChannels);
jbyteArray data = (jbyteArray)env->GetObjectField(imageData, fidData);
// 将Java字节数组转换为C++指针
jbyte* cData = env->GetByteArrayElements(data, nullptr);
// 释放资源
env->ReleaseByteArrayElements(data, cData, JNI_ABORT);

```


