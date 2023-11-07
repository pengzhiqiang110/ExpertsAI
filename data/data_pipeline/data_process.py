# 该脚本不要直接跑，需根据数据状况，调整参考
# 原始数据中包含需清洗数据
# 1. 最初ASR转为json，需进一步提取text
# 2. 部分音频切割转为文本，需进一步合并
# 3. 部分短文本中，标题可做问题，将标题写入内容开头
# 待解决：核心自信课 数据大量缺失
import os
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

folder_path = '初筛数据/阮琦/课程与视频'  # 替换为你的文件夹路径  
all_files = list_files_in_folder_recursive(folder_path)


# 解决json提取text
import json
def json2txt(all_files):
    for file in all_files:
        if file.endswith(".json"):
            print(file)
            base_filename = os.path.splitext(file)[0]
            base_filename = base_filename + '.txt'

            # 读取 JSON 文件  
            with open(file, 'r') as json_file:  
                data = json.load(json_file)['text']
            # 将数据写入 TXT 文件  
            with open(base_filename, 'w') as txt_file:  
                #print(data['text'])
                txt_file.write(data) 
            os.remove(file)


# 解决 长期关系课、阮琦视频号_转文本、表达训练课 内容切片的合并
# 解决 30步脱单秘笈 短文本类型，标题补充进内容
    dic={}
    for file in all_files:
        file_name=os.path.split(file)[-1]
        path = os.path.dirname(file)
        if os.path.split(file)[-1].startswith('.') or 'checkpoint' in file: continue
#         if '长期关系课' in file or '阮琦视频号_转文本' in file or '表达训练课' in file:
#             #print(file)
#             file_name=os.path.split(file)[-1]
#             path = os.path.dirname(file)
#             if '表达训练课' in file:
#                 file_new = path + '/' + file.split('-')[1].strip()
#                 num = int(file_name.split('-')[0])
#             # if '阮琦视频号_转文本' in file and 'segment' in file:
#             #     file_new = file.split('.')[0]+'.txt'
#             #     num = int(file_name.split('.')[1].split('_')[1])
                
        
#             with open(file, 'r') as f:
#                 context = f.read()
#             if file_new not in dic:
#                 dic[file_new]={num:context}
#             else:
#                 dic[file_new][num]=context
                
        if '课程概述' in file:
            os.remove(file)
            
        if '30步脱单秘笈' in file:
            # 文件名 写入 文件中
            file_new = path + '/new_' + file_name
            with open(file, 'r') as f:
                context = f.read()
            with open(file_new, 'w') as txt_file:  
                #print(data['text'])
                txt_file.write(file_name.split('.')[0]+context)
            
    
    for file_new in dic:
        # 使用 sorted() 函数对字典进行排序，注意这里使用了 lambda 表达式来定义排序规则  
        sorted_dict = dict(sorted(dic[file_new].items(), key=lambda item: item[0], reverse=False))
        # 接下来，我们可以按需要拼接字符串值  
        result = ''.join(sorted_dict.values())
        print(file_new)
        with open(file_new, 'w') as txt_file:  
            #print(data['text'])
            txt_file.write(result)
            