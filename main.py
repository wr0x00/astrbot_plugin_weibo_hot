from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import httpx
import json
from bs4 import BeautifulSoup


@register("weibo_hot", "weibo_hot", "一个简单的抓取微博热榜插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    
    # 将 weibohot 方法改为异步调用
    @filter.command("wbhot")
    async def weibohot(self, event: AstrMessageEvent):
        result = await self.fetch_weibo_hot_simple()
        if result:
            yield event.plain_result(result)
        else:
            yield event.plain_result("❌ 未能获取到微博热榜数据")

    # 将 fetch_weibo_hot_simple 方法改为异步方法
    async def fetch_weibo_hot_simple(self):
        with open('data/plugins/astrbot_plugin_weibo_hot/config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        url = "https://s.weibo.com/top/summary"
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://weibo.com/',
                "Cookie": data["Cookie"]
            }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status() # 检查请求是否成功
        except httpx.RequestError as e:
            logger.error(f"获取微博热榜失败: {e}")
            return ""
        soup = BeautifulSoup(response.text, 'html.parser')
        lines = [] # 使用列表存储每一行
        pinned = soup.select_one('#pl_top_realtimehot table tr td.td-02 a')
        if pinned:
            lines.append(f"置顶.{pinned.text.strip()}(🔥置顶)")
        
        for i, item in enumerate(soup.select('#pl_top_realtimehot tbody tr')[1:], 1):
            title = item.select_one('.td-02 a').text.strip()
            hot = item.select_one('.td-02 span').text.strip() if item.select_one('.td-02 span') else "0"
            lines.append(f"{i}.{title}(🔥{hot})")
            
        return "\n".join(lines) # 最后统一拼接



            