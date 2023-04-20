# encoding:utf-8

import requests

from bot.bot import Bot
from bridge.reply import Reply, ReplyType

# 本地部署的chatGML模型（与app.py系统启动在同一个环境下）
class ChatGML(Bot):
    def __init__(self):
        print("初始化chatGML完成")



    def reply(self, query, context = None):
        print("执行进入了chatGML模型")
        reply = None
        reply = Reply(ReplyType.TEXT, "这里可以填写字符串吗？")
        return reply