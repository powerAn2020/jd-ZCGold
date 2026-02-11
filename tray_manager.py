"""系统托盘管理 - 负责系统托盘图标和菜单"""

import pystray
from PIL import Image, ImageDraw
from typing import Callable
from config import TRAY_ICON_SIZE, APP_NAME


class TrayManager:
    """系统托盘管理器"""
    
    def __init__(self, on_show: Callable, on_hide: Callable, on_quit: Callable, on_toggle_click_through: Callable = None):
        """
        初始化托盘管理器
        
        Args:
            on_show: 显示窗口的回调函数
            on_hide: 隐藏窗口的回调函数
            on_quit: 退出程序的回调函数
            on_toggle_click_through: 切换鼠标穿透的回调函数
        """
        self.on_show = on_show
        self.on_hide = on_hide
        self.on_quit = on_quit
        self.on_toggle_click_through = on_toggle_click_through
        self.icon = None
        self.window_visible = True
        self.click_through_enabled = False
    
    def _create_icon_image(self) -> Image.Image:
        """
        创建托盘图标
        
        Returns:
            PIL Image对象
        """
        # 创建一个金色的圆形图标
        image = Image.new('RGB', TRAY_ICON_SIZE, (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # 绘制金色圆形
        margin = 8
        draw.ellipse(
            [margin, margin, TRAY_ICON_SIZE[0] - margin, TRAY_ICON_SIZE[1] - margin],
            fill='#FFD700',  # 金色
            outline='#FFA500'  # 橙色边框
        )
        
        # 绘制"金"字（简化版，用圆点表示）
        center_x, center_y = TRAY_ICON_SIZE[0] // 2, TRAY_ICON_SIZE[1] // 2
        draw.ellipse(
            [center_x - 6, center_y - 6, center_x + 6, center_y + 6],
            fill='#8B4513'  # 棕色
        )
        
        return image
    
    def _toggle_window(self, icon, item):
        """切换窗口显示/隐藏"""
        if self.window_visible:
            self.on_hide()
            self.window_visible = False
        else:
            self.on_show()
            self.window_visible = True
    
    def _quit_app(self, icon, item):
        """退出应用"""
        icon.stop()
        self.on_quit()
    
    def _toggle_click_through(self, icon, item):
        """切换鼠标穿透"""
        if self.on_toggle_click_through:
            self.on_toggle_click_through()
            # 直接从窗口获取最新状态，不要反转
            # 状态已经在 toggle_click_through 中更新了
    
    def _check_click_through(self, item):
        """检查鼠标穿透是否启用（用于菜单显示勾选）"""
        return self.click_through_enabled
    
    def _create_menu(self):
        """创建托盘菜单"""
        return pystray.Menu(
            pystray.MenuItem(
                "显示/隐藏",
                self._toggle_window,
                default=True
            ),
            pystray.MenuItem(
                "鼠标穿透",
                self._toggle_click_through,
                checked=self._check_click_through
            ),
            pystray.MenuItem(
                "退出",
                self._quit_app
            )
        )
    
    def run(self):
        """运行托盘图标（阻塞）"""
        icon_image = self._create_icon_image()
        menu = self._create_menu()
        
        self.icon = pystray.Icon(
            APP_NAME,
            icon_image,
            APP_NAME,
            menu
        )
        
        # 双击托盘图标切换窗口
        self.icon.run()
    
    def stop(self):
        """停止托盘图标"""
        if self.icon:
            self.icon.stop()
