"""浮窗UI - 负责显示黄金价格的置顶透明窗口"""

import tkinter as tk
from datetime import datetime
from typing import Optional, Dict, Callable
from config import *
import win32gui
import win32con


class FloatingWindow:
    """黄金价格浮窗"""
    
    def __init__(self, on_close_callback: Optional[Callable] = None):
        self.root = tk.Tk()
        self.on_close_callback = on_close_callback
        
        # 窗口配置
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=WINDOW_BG_COLOR)
        
        # 置顶和透明度
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', WINDOW_ALPHA)
        
        # 无边框
        self.root.overrideredirect(True)
        
        # 拖动相关变量
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        # 鼠标穿透状态（默认不启用）
        self.click_through_enabled = False
        
        # 创建UI元素
        self._create_widgets()
        
        # 绑定拖动事件
        self._bind_drag_events()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """创建UI组件"""
        # 主容器
        container = tk.Frame(self.root, bg=WINDOW_BG_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # 第一行：当前价格
        price_frame = tk.Frame(container, bg=WINDOW_BG_COLOR)
        price_frame.pack(fill=tk.X)
        
        tk.Label(
            price_frame,
            text="当前金价:",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        ).pack(side=tk.LEFT)
        
        self.price_label = tk.Label(
            price_frame,
            text="--",
            font=(FONT_FAMILY, FONT_SIZE_LARGE, "bold"),
            fg=COLOR_TEXT,
            bg=WINDOW_BG_COLOR
        )
        self.price_label.pack(side=tk.LEFT, padx=(3, 0))
        
        # 第二行：涨跌额
        change_frame = tk.Frame(container, bg=WINDOW_BG_COLOR)
        change_frame.pack(fill=tk.X, pady=(1, 0))
        
        tk.Label(
            change_frame,
            text="涨跌额:",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        ).pack(side=tk.LEFT)
        
        self.change_amt_label = tk.Label(
            change_frame,
            text="--",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        )
        self.change_amt_label.pack(side=tk.LEFT, padx=(3, 0))
        
        # 第三行：涨跌幅
        rate_frame = tk.Frame(container, bg=WINDOW_BG_COLOR)
        rate_frame.pack(fill=tk.X, pady=(1, 0))
        
        tk.Label(
            rate_frame,
            text="涨跌幅:",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        ).pack(side=tk.LEFT)
        
        self.change_rate_label = tk.Label(
            rate_frame,
            text="--",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        )
        self.change_rate_label.pack(side=tk.LEFT, padx=(3, 0))
        
        # 第四行：昨收
        yesterday_frame = tk.Frame(container, bg=WINDOW_BG_COLOR)
        yesterday_frame.pack(fill=tk.X, pady=(1, 0))
        
        tk.Label(
            yesterday_frame,
            text="昨收:",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        ).pack(side=tk.LEFT)
        
        self.yesterday_label = tk.Label(
            yesterday_frame,
            text="--",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        )
        self.yesterday_label.pack(side=tk.LEFT, padx=(3, 0))
        
        # 第五行：更新时间
        time_frame = tk.Frame(container, bg=WINDOW_BG_COLOR)
        time_frame.pack(fill=tk.X, pady=(1, 0))
        
        self.time_label = tk.Label(
            time_frame,
            text="更新: --",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=COLOR_NEUTRAL,
            bg=WINDOW_BG_COLOR
        )
        self.time_label.pack(side=tk.LEFT)
    
    def _enable_click_through(self):
        """启用鼠标穿透功能"""
        try:
            # 获取窗口句柄
            hwnd = win32gui.FindWindow(None, APP_NAME)
            if hwnd:
                # 获取当前窗口扩展样式
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                # 添加 WS_EX_TRANSPARENT 和 WS_EX_LAYERED 样式
                ex_style |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
                # 设置新的扩展样式
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
                self.click_through_enabled = True
        except Exception as e:
            # 如果失败，静默处理（可能是窗口还未完全创建）
            pass
    
    def _disable_click_through(self):
        """禁用鼠标穿透功能"""
        try:
            # 获取窗口句柄
            hwnd = win32gui.FindWindow(None, APP_NAME)
            if hwnd:
                # 获取当前窗口扩展样式
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                # 移除 WS_EX_TRANSPARENT 样式
                ex_style &= ~win32con.WS_EX_TRANSPARENT
                # 设置新的扩展样式
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
                self.click_through_enabled = False
        except Exception as e:
            pass
    
    def toggle_click_through(self):
        """切换鼠标穿透状态"""
        if self.click_through_enabled:
            self._disable_click_through()
        else:
            self._enable_click_through()
    
    def _bind_drag_events(self):
        """绑定窗口拖动事件"""
        self.root.bind("<Button-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._on_drag)
        
        # 为所有子组件也绑定拖动
        for widget in self.root.winfo_children():
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._on_drag)
            for child in widget.winfo_children():
                child.bind("<Button-1>", self._start_drag)
                child.bind("<B1-Motion>", self._on_drag)
    
    def _start_drag(self, event):
        """开始拖动"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _on_drag(self, event):
        """拖动中"""
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")
    
    def update_data(self, data: Dict):
        """
        更新显示数据
        
        Args:
            data: 包含价格信息的字典
        """
        if not data:
            return
        
        # 更新价格
        price = data.get('price', '--')
        self.price_label.config(text=price)
        
        # 更新涨跌额和涨跌幅（带颜色）
        change_amt = data.get('change_amt', '0')
        change_rate = data.get('change_rate', '0%')
        
        # 判断涨跌
        try:
            amt_value = float(change_amt)
            if amt_value > 0:
                color = COLOR_UP
                amt_text = change_amt if change_amt.startswith('+') else f"+{change_amt}"
            elif amt_value < 0:
                color = COLOR_DOWN
                amt_text = change_amt
            else:
                color = COLOR_NEUTRAL
                amt_text = change_amt
        except ValueError:
            color = COLOR_NEUTRAL
            amt_text = change_amt
        
        self.change_amt_label.config(text=amt_text, fg=color)
        self.change_rate_label.config(text=change_rate, fg=color)
        
        # 更新昨日价格
        yesterday = data.get('yesterday_price', '--')
        self.yesterday_label.config(text=yesterday)
        
        # 更新时间
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"更新: {now}")
    
    def show(self):
        """显示窗口"""
        self.root.deiconify()
    
    def hide(self):
        """隐藏窗口"""
        self.root.withdraw()
    
    def _on_closing(self):
        """窗口关闭事件"""
        if self.on_close_callback:
            self.on_close_callback()
    
    def destroy(self):
        """销毁窗口"""
        self.root.quit()
        self.root.destroy()
