# coding=utf-8
import os
import qianfan

def gpt(question):
    with open('QIANFAN_ACCESS_KEY', 'r', encoding='utf-8') as f:
        QIANFAN_ACCESS_KEY = f.read()
    os.environ['QIANFAN_AK'] = QIANFAN_ACCESS_KEY
    
    with open('QIANFAN_SECRET_KEY', 'r', encoding='utf-8') as f:
        QIANFAN_SECRET_KEY = f.read()
    os.environ['QIANFAN_SK'] = QIANFAN_SECRET_KEY
    chat_robt = qianfan.ChatCompletion()
    resp = chat_robt.do(
        messages=[{
            'role': 'user',
            'content': question
        }]
    )
    return resp.body['result']

if __name__ == '__main__':
    result = gpt("Python是什么？")
    print(result)