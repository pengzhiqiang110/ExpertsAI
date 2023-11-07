# 文本切片，提取问题或问答对
# 1. 文本切合适长度[100左右，重叠20?]，设计prompt,提取问题
# 2. 文本切合适长度[1000左右，重叠200],设计prompt,提取知识点[问答对]

import requests
import json
import time
import hashlib
import os


def calculate_md5(input_string):
    md5 = hashlib.md5()
    md5.update(input_string.encode('utf-8'))
    encrypted = md5.hexdigest()
    return encrypted

def do_request(prompt):
    url = "https://api.baichuan-ai.com/v1/chat"
    api_key = "bdeba0caffdf6bdaa2c0014100568a59"
    secret_key = "3dX74NvSwHusGNlel9+wdUEa+sI="

    data = {
        "model": "Baichuan2-53B",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    json_data = json.dumps(data)
    time_stamp = int(time.time())
    signature = calculate_md5(secret_key + json_data + str(time_stamp))

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
        "X-BC-Request-Id": "your requestId",
        "X-BC-Timestamp": str(time_stamp),
        "X-BC-Signature": signature,
        "X-BC-Sign-Algo": "MD5",
    }

    response = requests.post(url, data=json_data, headers=headers)
    
    res={}
    if response.status_code == 200:
        res={}
        print("请求成功！")
        print("响应header:", response.headers)
        print("响应内容:",response.text)
        text=json.loads(response.text)
        if text['code']==0:
            res=text['data']['messages'][0]['content']
            #print("响应body:", res)
        else:
            print("请求失败，状态码:", text['code'])
    
    else:
        print("请求失败，状态码:", response.status_code)
    return res


def list_files_in_folder_recursive(folder_path):  
    file_list = []
    def traverse_folder(folder_path):  
        for entry in os.listdir(folder_path):  
            entry_path = os.path.join(folder_path, entry)  
            if os.path.isfile(entry_path):  
                file_list.append(entry_path)  
            elif os.path.isdir(entry_path):  
                traverse_folder(entry_path)
    traverse_folder(folder_path)  
    return file_list

    
def opentxt(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content
    #print(content)
    
def split_text(text, max_length=1000, overlap=200):
    # 如果文本长度超过max_length，使用滑动窗口进行分片
    slices = []
    start = 0
    while start < len(text):
        end = start + max_length
        slices.append(text[start:end])
        start += max_length - overlap

    return slices

import re

def format_text(s):
    # 去除多余的空格和换行
    s = s.strip().strip()
    
    # 将连续的空行合并为一个
    s = re.sub(r'\n\s*\n', '', s)
    
    # 删除特定的字符，这里假设是页码或页眉，可以根据需要调整
    s = re.sub(r'\[\*\d+\]', '', s)
    
    return s

def prompt_product2(context):
    prompt=f"""目标：
    1.请仔细阅读以下文本。您的任务是识别与恋爱或感情话题相关的核心知识点。对于识别到的知识点，请构思用户会口语化表达的问题，该问题应该能够引导理解和思考这一知识点。
    2.请根据文本内容为问题提供一个准确，丰富，适当解释，更加易于理解的高质量答案。确保您的问题对与恋爱话题紧密相关。确保您的问题对来自文本内容。
    3.请以JSON格式返回问题和答案对。不要返回其他内容。


    提供的文本：{context}
    输出：
    """
    return prompt


    

if __name__ == "__main__":
    list_file=list_files_in_folder_recursive('初筛数据')
    for file in list_file:
        print(file)
        paragraphs=opentxt(file)
        print(type(paragraphs))
        result=split_text(paragraphs, 1000, 200)
        for slice in result:
            #print('-' * 50)  # 分隔线
            print(type(slice))
            context = format_text(slice)
            prompt_self_qa=prompt_product2(context)

            print(prompt_self_qa)
            print('-' * 50)  # 分隔线
            res=do_request(prompt_self_qa)
            print(res)
            print('-' * 50)  # 分隔线
            break
