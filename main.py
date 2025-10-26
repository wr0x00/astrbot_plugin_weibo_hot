from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import requests
from bs4 import BeautifulSoup


@register("weibo_hot", "weibo_hot", "一个简单的抓取微博热榜插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    
    @filter.command("wbhot")
    async def weibohot(self, event: AstrMessageEvent):
        '''
        await event.send(event.plain_result("微博bot为您服务 ٩( 'ω' )و"))
        hot_list = self.fetch_weibo_hot_simple()
        print(hot_list)
        """美观地显示热搜列表"""
        if not hot_list:
            event.chain_result("❌ 未能获取到微博热榜数据")
            return
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        event.chain_result("\n" + "="*70)
        event.chain_result(f"🔥 微博实时热榜 (更新时间: {current_time})")
        event.chain_result("="*70)
        
        for item in hot_list:
            rank = item['排名']
            title = item['标题']
            hot_value = item['热度值']
            category = f"[{item['分类']}]" if item['分类'] else ""
            label = f"({item['标签']})" if item['标签'] else ""
            
            # 格式化输出，确保对齐
            event.chain_result(f"{rank:2d}. {title}")
            if hot_value != 'N/A' or category or label:
                info_parts = [part for part in [f"🔥 {hot_value}" if hot_value != 'N/A' else "", category, label] if part]
                if info_parts:
                    event.chain_result(f"    {' '.join(info_parts)}")
            #event.chain_result("-" * 70)
        '''
        yield event.plain_result(self.fetch_weibo_hot_simple())
        
        

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
    def fetch_weibo_hot_simple(self):
        url = "https://s.weibo.com/top/summary"
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://weibo.com/',
                    "Cookie": "SUB=_2AkMWJrkXf8NxqwJRmP8SxWjnaY12zwnEieKgekjMJRMxHRl-yj9jqmtbtRB6PaaX-IGp-AjmO6k5cS-OH2X9CayaTzVD"
                }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        result = ""
        # 处理置顶项
        pinned = soup.select_one('#pl_top_realtimehot table tr td.td-02 a')
        if pinned:
            result += f"置顶.{pinned.text.strip()}(🔥置顶)"
            
        for i, item in enumerate(soup.select('#pl_top_realtimehot tbody tr')[1:], 1):
            title = item.select_one('.td-02 a').text.strip()
            hot = item.select_one('.td-02 span').text.strip() if item.select_one('.td-02 span') else "0"
            result += f"{i}.{title}(🔥{hot})\n"
        return result.strip()



            