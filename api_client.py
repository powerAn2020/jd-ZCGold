"""API客户端 - 负责从京东API获取黄金价格数据"""

import requests
import logging
from typing import Optional, Dict
from config import API_URL, REQUEST_TIMEOUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoldPriceAPI:
    """黄金价格API客户端"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_price(self) -> Optional[Dict]:
        """
        获取最新金价数据
        
        Returns:
            包含价格信息的字典，失败返回None
            {
                'price': str,           # 当前价格
                'yesterday_price': str, # 昨日价格
                'change_amt': str,      # 涨跌额
                'change_rate': str,     # 涨跌幅
                'update_time': str      # 更新时间
            }
        """
        try:
            response = self.session.get(API_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # 检查返回状态
            if not data.get('success'):
                logger.error(f"API返回失败: {data.get('resultMsg')}")
                return None
            
            # 提取数据
            result_data = data.get('resultData', {}).get('datas', {})
            
            return {
                'price': result_data.get('price', 'N/A'),
                'yesterday_price': result_data.get('yesterdayPrice', 'N/A'),
                'change_amt': result_data.get('upAndDownAmt', '0'),
                'change_rate': result_data.get('upAndDownRate', '0%'),
                'update_time': result_data.get('time', '')
            }
            
        except requests.exceptions.Timeout:
            logger.error("请求超时")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"解析数据失败: {e}")
            return None
    
    def close(self):
        """关闭会话"""
        self.session.close()
