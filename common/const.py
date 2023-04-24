# bot_type
OPEN_AI = "openAI"
CHATGPT = "chatGPT"
BAIDU = "baidu"
CHATGPTONAZURE = "chatGPTOnAzure"
CHATGML = "chatGML"
PAUSE = True # 项目启动(False)，暂停（True）
MODEL_PATH = "./model/chatglm-6b" # 模型路径
GPU = True # 是否使用显卡
GPU_LEVEL = "int8" # choices=["fp16", "int4", "int8"] 默认int8 可在8G显存上运行，int 4可在6G显存上运行， fp16 需要13G以上显存
SAY = "say" # 调用对话模型
DRAW = "draw" # 调用绘图模型
SEARCH = "search" # 调用搜索模型
# chatGLM入参
max_length = 2048
top_p = 0.7       
temperature = 0.95