import jsonlines
import requests
import pandas as pd

# 读取同目录下的datasets.jsonl文件
with jsonlines.open('datasets.jsonl', 'r') as reader:
    dataset = [obj for obj in reader]

url = "https://api.siliconflow.cn/v1/chat/completions"
token = "sk-odxkswagmgpwazmumdinbihxxioqzbyboceptmwytkdofmzr"

# 创建用于存储结果的字典
results = {
    'DeepSeek-V3': []  # 可以根据需要添加更多模型
}
questions = []

# Process each question in the dataset
for item in dataset:
    questions.append(item['question'])
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {
                "role": "user",
                "content": item['question']
            }
        ],
        "stream": False,
        "max_tokens": 512,
        "stop": ["null"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": [
            {
                "type": "function",
                "function": {
                    "description": "<string>",
                    "name": "<string>",
                    "parameters": {},
                    "strict": False
                }
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        print(f"Question: {item['question']}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}\n")
        
        # 存储响应结果
        results['DeepSeek-V3'].append(response.text)
        
    except requests.exceptions.ConnectionError:
        print("网络连接错误，请检查网络连接")
        results['DeepSeek-V3'].append("网络连接错误")
    except requests.exceptions.Timeout:
        print("请求超时")
        results['DeepSeek-V3'].append("请求超时")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {str(e)}")
        results['DeepSeek-V3'].append(f"请求错误: {str(e)}")

# 创建DataFrame并保存为Excel
df = pd.DataFrame(results, index=questions)
df.to_excel('model_responses.xlsx')
print("结果已保存到 model_responses.xlsx")