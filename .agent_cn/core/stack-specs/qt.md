# Qt/C++/QML 开发规约

> 适用于 Qt 5.15+ / Qt 6 项目的开发规范。

---

## 1. 项目结构

```
project/
├── src/
│   ├── main.cpp
│   ├── app/
│   │   ├── Application.h
│   │   └── Application.cpp
│   ├── models/
│   ├── services/
│   └── ui/
│       └── qml/
│           ├── main.qml
│           └── components/
├── resources/
│   ├── qml.qrc
│   └── assets.qrc
├── tests/
├── .agent/
├── CMakeLists.txt
└── README.md
```

---

## 2. C++ 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类 | PascalCase | `UserManager` |
| 方法 | camelCase | `getUserById()` |
| 成员变量 | m_ + camelCase | `m_userName` |
| 局部变量 | camelCase | `userName` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 枚举 | PascalCase | `Status::Active` |
| 命名空间 | lowercase | `myapp::core` |

---

## 3. QML 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件名 | PascalCase | `UserCard.qml` |
| 属性 | camelCase | `userName` |
| 信号 | camelCase | `userClicked` |
| 函数 | camelCase | `handleClick()` |
| id | camelCase | `userCard` |

---

## 4. Qt 最佳实践

### 4.1 信号槽连接

```cpp
// ✅ 推荐 - 新式连接（编译时检查）
connect(button, &QPushButton::clicked, 
        this, &MyClass::handleClick);

// ✅ Lambda 连接
connect(button, &QPushButton::clicked, this, [this]() {
    handleClick();
});

// ⚠️ 旧式连接（运行时检查）
connect(button, SIGNAL(clicked()), this, SLOT(handleClick()));
```

### 4.2 对象生命周期

```cpp
// ✅ 正确 - 使用父对象管理生命周期
auto* widget = new QWidget(this); // this 是父对象

// ✅ 正确 - 智能指针管理
auto widget = std::make_unique<QWidget>();

// ❌ 错误 - 内存泄漏风险
auto* widget = new QWidget(); // 无父对象，需手动删除
```

### 4.3 线程安全

```cpp
// 跨线程信号槽
connect(worker, &Worker::resultReady,
        this, &MainWindow::handleResult,
        Qt::QueuedConnection); // 明确指定连接类型

// 使用 QMutex 保护共享数据
class ThreadSafeCounter {
public:
    void increment() {
        QMutexLocker locker(&m_mutex);
        ++m_count;
    }
private:
    QMutex m_mutex;
    int m_count = 0;
};
```

---

## 5. QML 最佳实践

### 5.1 属性绑定

```qml
// ✅ 正确 - 声明式绑定
Rectangle {
    width: parent.width * 0.8
    height: contentColumn.height + 20
    color: mouseArea.pressed ? "lightblue" : "white"
}

// ❌ 避免 - 命令式赋值破坏绑定
Component.onCompleted: {
    width = parent.width * 0.8 // 破坏了绑定
}
```

### 5.2 组件化

```qml
// UserCard.qml - 可复用组件
import QtQuick 2.15

Rectangle {
    id: root
    
    // 公开属性
    property string userName: ""
    property string avatarUrl: ""
    
    // 公开信号
    signal clicked()
    signal deleteRequested()
    
    // 内部实现
    width: 200
    height: 80
    
    MouseArea {
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
```

### 5.3 动画规范

```qml
// ✅ 正确 - 平滑过渡
Rectangle {
    id: panel
    width: expanded ? 300 : 100
    
    Behavior on width {
        NumberAnimation {
            duration: 250
            easing.type: Easing.OutQuad
        }
    }
}

// ❌ 禁止 - 硬跳变
Rectangle {
    width: expanded ? 300 : 100 // 无动画！
}
```

---

## 6. C++ 与 QML 交互

### 6.1 注册类型

```cpp
// main.cpp
#include <QQmlContext>
#include "UserModel.h"

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);
    
    // 注册类型
    qmlRegisterType<UserModel>("MyApp", 1, 0, "UserModel");
    
    // 注册单例
    qmlRegisterSingletonType<AppSettings>(
        "MyApp", 1, 0, "AppSettings",
        [](QQmlEngine*, QJSEngine*) -> QObject* {
            return new AppSettings();
        }
    );
    
    QQmlApplicationEngine engine;
    engine.load(QUrl("qrc:/main.qml"));
    
    return app.exec();
}
```

### 6.2 暴露属性和方法

```cpp
class UserModel : public QObject {
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(int count READ count NOTIFY countChanged)
    
public:
    QString name() const { return m_name; }
    void setName(const QString& name);
    
    int count() const { return m_count; }
    
    Q_INVOKABLE void refresh();
    
signals:
    void nameChanged();
    void countChanged();
    void dataLoaded(const QVariantList& data);
    
private:
    QString m_name;
    int m_count = 0;
};
```

---

## 7. 资源管理

### 7.1 QRC 文件

```xml
<!-- qml.qrc -->
<RCC>
    <qresource prefix="/qml">
        <file>main.qml</file>
        <file>components/UserCard.qml</file>
    </qresource>
</RCC>

<!-- assets.qrc -->
<RCC>
    <qresource prefix="/assets">
        <file>icons/user.svg</file>
        <file>fonts/Roboto-Regular.ttf</file>
    </qresource>
</RCC>
```

### 7.2 加载资源

```qml
Image {
    source: "qrc:/assets/icons/user.svg"
}

FontLoader {
    source: "qrc:/assets/fonts/Roboto-Regular.ttf"
}
```

---

## 8. CMake 配置

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)

qt_add_executable(${PROJECT_NAME}
    src/main.cpp
    src/app/Application.cpp
)

qt_add_qml_module(${PROJECT_NAME}
    URI MyApp
    VERSION 1.0
    QML_FILES
        src/ui/qml/main.qml
        src/ui/qml/components/UserCard.qml
    RESOURCES
        resources/icons/user.svg
)

target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
)
```

---

## 9. 测试规范

### 9.1 Qt Test

```cpp
#include <QtTest>
#include "UserModel.h"

class TestUserModel : public QObject {
    Q_OBJECT
    
private slots:
    void initTestCase() {
        // 全局初始化
    }
    
    void cleanupTestCase() {
        // 全局清理
    }
    
    void testSetName() {
        UserModel model;
        QSignalSpy spy(&model, &UserModel::nameChanged);
        
        model.setName("Alice");
        
        QCOMPARE(model.name(), QString("Alice"));
        QCOMPARE(spy.count(), 1);
    }
};

QTEST_MAIN(TestUserModel)
#include "test_user_model.moc"
```

### 9.2 QML 测试

```qml
import QtQuick 2.15
import QtTest 1.15
import MyApp 1.0

TestCase {
    name: "UserCardTest"
    
    UserCard {
        id: userCard
    }
    
    function test_initialState() {
        compare(userCard.userName, "")
    }
    
    function test_clickEmitsSignal() {
        var clicked = false
        userCard.clicked.connect(function() { clicked = true })
        mouseClick(userCard)
        verify(clicked)
    }
}
```

---

## 10. 代码检查

```bash
# 格式化（需要 clang-format）
find src -name '*.cpp' -o -name '*.h' | xargs clang-format -i

# 静态分析
clang-tidy src/**/*.cpp

# 构建
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# 测试
cd build && ctest --output-on-failure

# QML Lint（Qt 6）
qmllint src/ui/qml/**/*.qml
```

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
