# encoding:utf-8

import requests

from bot.bot import Bot
from bridge.reply import Reply, ReplyType
from transformers import AutoModel, AutoTokenizer
from  common.const import PAUSE, MODEL_PATH, GPU, GPU_LEVEL
from common import const
from common.util import Util
from PIL import Image

# 本地部署的chatGML模型（与app.py系统启动在同一个环境下）
#class ChatGML(Bot):
class ChatGML():
    def __init__(self):
        global sd_model_dict # sd模型的model_name与model_hash
        if PAUSE == False:
            print("初始化stable diffusion...")
            print("读取sd模型...")
            model_name, model_hash = Util.stable_diffusion_get_sd_models()
            sd_model_dict = dict(zip(model_name, model_hash))
            print("读取本地的sd_model成功...")

            print("初始化chatGML....")
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
        

    def predict(self, query, max_length, top_p, temperature, drawHistory):
        global history
        if(len(self.readable_history) > 10):
            self.readable_history=[]
        if self.isNotBlank(drawHistory):
            output, history = self.model.chat(
            self.tokenizer, query=query, history=drawHistory,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature)
            return output
        else:
            output, history = self.model.chat(
            self.tokenizer, query=query, history=self.readable_history,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature)
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


    # 删除请求字符中开头的多余空格和逗号
    def deleteInvalid(self, query):
        return query.lstrip(" ,，")

    # 判断空字符
    def isNotBlank(self, s):
        return s is not None and bool(s and isinstance(s, list))

    # 向模型发起聊天会话
    def reply(self, query, context = None):
        print("执行进入了chatGML模型")
        if PAUSE == True:
            reply = Reply(ReplyType.TEXT, "目前项目停止，小周同学正在快马加鞭DEBUG中...")
            return reply
        else:
            prompt_history = None
            if const.SAY in query[:3]:
                print("进入对话模型........")
                reply = None
                reply = Reply(ReplyType.TEXT, self.predict(query[3:],const.max_length, const.top_p, const.temperature, prompt_history)[0])
                return reply
            elif const.DRAW in query[:4]:
                print("进入绘图模型........")
                prompt_text = self.deleteInvalid(query[5:])
                Util.reloadCheckpoint()
                #/sdapi/v1/reload-checkpoint
                # 建筑

                # 动物

                # 动漫

                # 线稿
                Util.reloadCheckpoint()
                prompt_history = [["我接下来会给你一些作画的指令，你只要回复出作画内容及对象，不需要你作画，不需要给我参考，不需要你给我形容你的作画内容，请直接给出作画内容，你不要回复”好的，我会画一张“等不必要的内容，你只需回复作画内容。你听懂了吗","听懂了。请给我一些作画的指令。"]]
                query = str(f"不需要你作画，不需要给我参考，不需要你给我形容你的作画内容，请给出“{prompt_text}”中的作画内容，请直接给出作画内容和对象")
                draw_object = self.predict(query,const.max_length, const.top_p, const.temperature, prompt_history)
                print(draw_object)
                if draw_object[0] == "，" or draw_object[0] == "," or draw_object[0] == "。" or draw_object[0] == ".":
                    draw_object = draw_object[1:len(draw_object)]
                if draw_object[-1] == "，" or draw_object[-1] == "," or draw_object[-1] == "。" or draw_object[-1] == ".":
                    draw_object = draw_object[0:len(draw_object)-1]
                draw_object = draw_object.replace("好的", "")
                draw_object = draw_object.replace("我", "")
                draw_object = draw_object.replace("将", "")
                draw_object = draw_object.replace("会", "")
                draw_object = draw_object.replace("画", "")
                if draw_object[0] == "，" or draw_object[0] == "," or draw_object[0] == "。" or draw_object[0] == ".":
                    draw_object = draw_object[1:len(draw_object)]
                if draw_object[-1] == "，" or draw_object[-1] == "," or draw_object[-1] == "。" or draw_object[-1] == ".":
                    draw_object = draw_object[0:len(draw_object)-1]
                Util.stable_diffusion(str(Util.translate(draw_object)),"")
                reply = Reply(ReplyType.IMAGE, Image.open('stable_diffusion.png'))
                return reply
            elif const.SEARCH in query[:6]:
                print("进行网络信息搜索........")
                searchQuery = self.deleteInvalid(query[6:]) # 这里不知道对不对 todo

    def run():
        print("初始化chat_gml_bot...")
        ChatGML.reply(ChatGML,"testText")
        