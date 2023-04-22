# encoding:utf-8

import requests

from bot.bot import Bot
from bridge.reply import Reply, ReplyType
from transformers import AutoModel, AutoTokenizer
from  common.const import PAUSE, MODEL_PATH, GPU, GPU_LEVEL

# 本地部署的chatGML模型（与app.py系统启动在同一个环境下）
class ChatGML(Bot):
    def __init__(self):
        if PAUSE == False:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH,trust_remote_code=True)
            self.model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True)
            if GPU == False:
                self.model = self.model.float()
            else:
                if GPU_LEVEL == "fp16":
                    self.model = self.model.half().cuda()
                    print("启动fp16")
                elif GPU_LEVEL == "int4":
                    self.model = self.model.half().quantize(4).cuda()
                    print("启动int4")
                elif GPU_LEVEL == "int8":
                    self.model = self.model.half().quantize(8).cuda()
                    print("启动int8")
            self.model = self.model.eval()
            self.history = []
            self.readable_history = []
            print("初始化chatGML完成")
        else:
            print("模型暂停启动，如需启动，请修改common.const.PAUSE为False")
        

    def predict(self, query, max_length, top_p, temperature):
        global history
        if(len(self.readable_history) > 5):
            self.readable_history=[]
        output, history = self.model.chat(
            self.tokenizer, query=query, history=self.readable_history,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature
        )
        self.readable_history.append((query, ChatGML.parse_codeblock(ChatGML, output)))
        print(output)
        return output, self.readable_history
    
    def parse_codeblock(cls, text):
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if "```" in line:
                if line != "```":
                    lines[i] = f'<pre><code class="{lines[i][3:]}">'
                else:
                    lines[i] = '</code></pre>'
            else:
                if i > 0:
                    lines[i] = "<br/>" + line.replace("<", "&lt;").replace(">", "&gt;")
        return "".join(lines)

    def reply(self, query, context = None):
        print("执行进入了chatGML模型")
        if PAUSE == True:
            reply = Reply(ReplyType.TEXT, "目前项目停止，小周同学正在快马加鞭DEBUG中...")
            return reply
        else:
            max_length = 2048
            top_p = 0.7
            temperature = 0.95
            reply = None
            reply = Reply(ReplyType.TEXT, self.predict(query,max_length, top_p, temperature)[0])
            return reply