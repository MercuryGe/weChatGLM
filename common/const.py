# bot_type
OPEN_AI = "openAI"
CHATGPT = "chatGPT"
BAIDU = "baidu"
CHATGPTONAZURE = "chatGPTOnAzure"
CHATGML = "chatGML"
PAUSE = False # 项目启动(False)，暂停（True）
MODEL_PATH = "./model/chatglm-6b" # 模型路径
GPU = True # 是否使用显卡
GPU_LEVEL = "int8" # choices=["fp16", "int4", "int8"] 默认int8 可在8G显存上运行，int 4可在6G显存上运行， fp16 需要13G以上显存

