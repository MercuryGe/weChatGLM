import requests, re, json, io, base64, os
from urllib.parse import quote
from bs4 import BeautifulSoup
from PIL import Image, PngImagePlugin

class Util():

    def test_if_zhcn(string):
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def translate(word):
        if Util.test_if_zhcn(word):
            url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
            key = {
                'type': "AUTO",
                'i': word,
                "doctype": "json",
                "version": "2.1",
                "keyfrom": "fanyi.web",
                "ue": "UTF-8",
                "action": "FY_BY_CLICKBUTTON",
                "typoResult": "true"
            }
            response = requests.post(url, data=key)
            if response.status_code == 200:
                list_trans = response.text
                result = json.loads(list_trans)
                return result['translateResult'][0][0]['tgt']
        else:
            return word
        

    def stable_diffusion(Pprompt,Nprompt):
        url = "http://127.0.0.1:7861"
        payload = {
            "prompt": Pprompt,
            "steps": 20,
            "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
            "sampler_index": "DPM++ 2M Karras", #采样方法选择
            "restore_faces": True, # 是否开启面部重绘
            "enable_hr": True, # 是否开启高清修复
            "denoising_strength": 0.7, #重绘幅度
            "hr_scale": 2, #放大倍率
            "hr_upscaler": "Latent", # 放大算法
            "hr_second_pass_steps": 0, # 高清修复采样次数
        }
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        r = response.json()
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save('stable_diffusion.png', pnginfo=pnginfo)

    def stable_diffusion_get_sd_models():
        url = "http://127.0.0.1:7861" 
        response = requests.get(url=f'{url}/sdapi/v1/sd-models')
        models = response.json()

        for model in models:
            model_name = model['model_name']
            model_hash = model['hash']
            print(f"Model name: {model_name}, Hash: {model_hash}")
        return model_name, model_hash

    def reloadCheckpoint():
        url = "http://127.0.0.1:7861"
        payload = {
            
        }
        response = requests.post(url=f'{url}/sdapi/v1/reload-checkpoint', json=payload)