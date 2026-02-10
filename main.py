"""主程序入口 - 整合所有模块并启动应用"""

import threading
import time
import logging
from api_client import GoldPriceAPI
from floating_window import FloatingWindow
from tray_manager import TrayManager
from config import REFRESH_INTERVAL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GoldPriceApp:
    """浙商积存金价格监控应用主类"""
    
    def __init__(self):
        self.api_client = GoldPriceAPI()
        self.window = FloatingWindow(on_close_callback=self.quit)
        self.tray = TrayManager(
            on_show=self.show_window,
            on_hide=self.hide_window,
            on_quit=self.quit,
            on_toggle_click_through=self.toggle_click_through
        )
        
        self.running = True
        self.update_thread = None
    
    def show_window(self):
        """显示窗口"""
        self.window.show()
    
    def hide_window(self):
        """隐藏窗口"""
        self.window.hide()
    
    def toggle_click_through(self):
        """切换鼠标穿透"""
        self.window.toggle_click_through()
        # 同步状态到托盘管理器
        self.tray.click_through_enabled = self.window.click_through_enabled
    
    def quit(self):
        """退出应用"""
        logger.info("正在退出应用...")
        self.running = False
        
        # 停止托盘
        self.tray.stop()
        
        # 关闭API客户端
        self.api_client.close()
        
        # 销毁窗口
        try:
            self.window.destroy()
        except:
            pass
    
    def _update_price_loop(self):
        """价格更新循环（在后台线程运行）"""
        logger.info("价格更新线程已启动")
        
        while self.running:
            try:
                # 获取最新价格
                data = self.api_client.fetch_price()
                
                if data:
                    # 在主线程更新UI
                    self.window.root.after(0, self.window.update_data, data)
                    logger.debug(f"价格已更新: {data.get('price')}")
                else:
                    logger.warning("获取价格失败")
                
            except Exception as e:
                logger.error(f"更新价格时出错: {e}")
            
            # 等待下一次更新
            time.sleep(REFRESH_INTERVAL)
        
        logger.info("价格更新线程已停止")
    
    def run(self):
        """启动应用"""
        logger.info("启动浙商积存金价格监控应用")
        
        # 启动价格更新线程
        self.update_thread = threading.Thread(
            target=self._update_price_loop,
            daemon=True
        )
        self.update_thread.start()
        
        # 在单独线程中运行托盘（避免阻塞tkinter主循环）
        tray_thread = threading.Thread(
            target=self.tray.run,
            daemon=True
        )
        tray_thread.start()
        
        # 运行tkinter主循环
        try:
            self.window.root.mainloop()
        except KeyboardInterrupt:
            logger.info("收到中断信号")
        finally:
            self.quit()


def main():
    """程序入口"""
    app = GoldPriceApp()
    app.run()


if __name__ == "__main__":
    main()
