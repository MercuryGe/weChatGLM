# 简介
本项目结合[chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)微信聊天机器人与[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)开源双语对话语言模型，在聊天机器人的项目中添加了chatGLM-6B模型的选项，这样可以定制一个自己的聊天机器人，可以当作我的微信助手。
准备再结合[ChatGLM-6B-Engineering](https://github.com/LemonQu-GIT/ChatGLM-6B-Engineering)，将Stable Diffusion也引进来

# 运行
模型可以从[hunggingface](https://huggingface.co/THUDM/chatglm-6b)上下载，根据上面连个项目的流程配好Python310的环境后，修改一下common.const里面的模型路径和显卡的类型，就可以执行app.py启动了