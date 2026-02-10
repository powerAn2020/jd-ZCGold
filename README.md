# 浙商积存金价格监控

Windows下的置顶透明浮窗应用，实时显示京东浙商积存金价格。

## 功能特性

✨ **置顶浮窗** - 窗口始终保持在最前端  
🎨 **透明度60%** - 半透明效果，不遮挡其他窗口  
🔄 **实时更新** - 每1秒自动刷新价格数据  
📊 **涨跌显示** - 红涨绿跌，直观显示价格变化  
🖲️ **鼠标穿透** - 窗口不阻挡鼠标点击，完全透明交互  
📌 **系统托盘** - 最小化到托盘，支持显示/隐藏切换  

## 快速开始

### 1. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
.\venv\Scripts\activate.bat
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行程序

```bash
python main.py
```

## 打包成可执行文件

使用PyInstaller打包成单文件exe：

```bash
# 确保在虚拟环境中
pyinstaller --onefile --windowed --name="浙商积存金价格监控" --icon=NONE main.py
```

打包后的exe文件位于 `dist` 目录下。

### 打包参数说明
- `--onefile`: 打包成单个exe文件
- `--windowed`: 不显示控制台窗口
- `--name`: 指定生成的exe文件名
- `--icon`: 指定图标（可选）

## 项目结构

```
gold/
├── main.py              # 程序入口
├── api_client.py        # API数据获取
├── floating_window.py   # 浮窗UI
├── tray_manager.py      # 系统托盘
├── config.py            # 配置文件
├── requirements.txt     # 依赖列表
├── build.bat            # Windows批处理打包脚本
├── build.ps1            # PowerShell打包脚本
└── README.md           # 本文件
```

## 配置说明

在 `config.py` 中可以修改以下配置：

- `REFRESH_INTERVAL`: 刷新间隔（秒），默认1秒
- `WINDOW_ALPHA`: 窗口透明度，默认0.6（60%）
- `WINDOW_WIDTH/HEIGHT`: 窗口大小（默认140x140）
- 颜色、字体等UI配置

## 使用说明

### 窗口操作
- **查看价格**: 窗口默认显示在屏幕上
- **关闭穿透**: 右键托盘图标 → 取消勾选"鼠标穿透"（关闭后可拖动窗口）

### 托盘菜单
- **显示/隐藏**: 切换窗口显示状态
- **鼠标穿透**: 切换鼠标穿透功能（打勾=开启，不打勾=关闭）
- **退出**: 关闭程序

## 数据来源

价格数据来自[京东浙商黄金API](https://api.jdjygold.com/gw2/generic/jrm/h5/m/stdLatestPrice?productSku=1961543816)

## 系统要求

- Windows 10/11
- Python 3.8+

## 依赖库

- `requests`: HTTP请求
- `pystray`: 系统托盘
- `Pillow`: 图像处理
- `pywin32`: Windows API（鼠标穿透功能）
- `pyinstaller`: 打包工具
- `pywin32`: windows API

## 常见问题

**Q: 程序无法启动？**  
A: 确保已安装所有依赖，运行 `pip install -r requirements.txt`

**Q: 数据不更新？**  
A: 检查网络连接，确保可以访问京东API

**Q: 如何修改刷新频率？**  
A: 编辑 `config.py` 中的 `REFRESH_INTERVAL` 参数

**Q: 打包后exe体积很大？**  
A: 这是正常的，PyInstaller会打包Python解释器和所有依赖

## 许可证

MIT License
