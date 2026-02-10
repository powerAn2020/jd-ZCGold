"""配置文件 - 存储应用程序的所有配置常量"""

# API配置
API_URL = "https://api.jdjygold.com/gw2/generic/jrm/h5/m/stdLatestPrice?productSku=1961543816"
REFRESH_INTERVAL = 1  # 刷新间隔（秒）
REQUEST_TIMEOUT = 5  # 请求超时时间（秒）

# 窗口配置
WINDOW_WIDTH = 140
WINDOW_HEIGHT = 140
WINDOW_ALPHA = 0.6  # 透明度 60%
WINDOW_BG_COLOR = "#2b2b2b"  # 背景颜色

# 颜色配置
COLOR_TEXT = "#ffffff"  # 文字颜色
COLOR_UP = "#ff4444"    # 上涨颜色（红色）
COLOR_DOWN = "#44ff44"  # 下跌颜色（绿色）
COLOR_NEUTRAL = "#cccccc"  # 中性颜色

# 字体配置
FONT_FAMILY = "微软雅黑"
FONT_SIZE_LARGE = 13
FONT_SIZE_MEDIUM = 9
FONT_SIZE_SMALL = 8

# 托盘配置
TRAY_ICON_SIZE = (64, 64)
APP_NAME = "浙商积存金价格监控"
