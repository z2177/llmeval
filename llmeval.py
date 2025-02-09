import jsonlines
import requests
import pandas as pd

# 读取同目录下的datasets.jsonl文件
with jsonlines.open('datasets.jsonl', 'r') as reader:
    dataset = [obj for obj in reader]

# url以及鉴权token
url = "https://api.siliconflow.cn/v1/chat/completions"
# 从mydata目录下的token文件读取token
with open('mydata/token', 'r') as f:
    token = f.read().strip()

# 待评估模型列表
models = [
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
]

# 创建用于存储结果的字典
results = {model.split('/')[-1]: [] for model in models}
questions = []

# Process each question in the dataset
total_questions = len(dataset)
for idx, item in enumerate(dataset, 1):
    print(f"\n处理问题 {idx}/{total_questions}: {item['question']}")
    questions.append(item['question'])
    
    # 对每个模型进行评测
    for model in models:
        print(f"正在调用模型: {model}")
        # 基础 payload
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": item['question']
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }
        
        # 只为 V3 模型添加 tools 参数
        if model == "deepseek-ai/DeepSeek-V3":
            payload["tools"] = [
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
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            print(f"Status Code: {response.status_code}")
            
            # 解析响应 JSON，保留完整响应
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                # 直接使用完整的响应文本
                answer = response.text
                print("成功获取响应")
            else:
                answer = f"错误: 无法获取有效响应 - {response.text}"
                print("响应格式错误")
            
            results[model.split('/')[-1]].append(answer)
            
        except Exception as e:
            error_msg = f"错误: {str(e)}"
            print(error_msg)
            results[model.split('/')[-1]].append(error_msg)

# 创建基础 DataFrame
df = pd.DataFrame(results, index=questions)

# 使用 DeepSeek-R1 Pro 进行评估
print("\n开始使用 DeepSeek-R1 评估结果...")
evaluation_results = []
for i, question in enumerate(questions):
    print(f"正在评估第 {i+1}/{len(questions)} 个问题")
    eval_prompt = f"""请评估以下四个模型对同一个问题的回答质量，给出评分（1-10分）和简要分析。

问题：{question}

模型回答：
1. DeepSeek-V3: {results['DeepSeek-V3'][i]}
2. DeepSeek-R1-Distill-Llama-70B: {results['DeepSeek-R1-Distill-Llama-70B'][i]}
3. DeepSeek-R1-Distill-Qwen-32B: {results['DeepSeek-R1-Distill-Qwen-32B'][i]}
4. DeepSeek-R1-Distill-Qwen-14B: {results['DeepSeek-R1-Distill-Qwen-14B'][i]}
"""

    eval_payload = {
        "model": "Pro/deepseek-ai/DeepSeek-R1",
        "messages": [{"role": "user", "content": eval_prompt}],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        eval_response = requests.request("POST", url, json=eval_payload, headers=headers)
        eval_json = eval_response.json()
        if 'choices' in eval_json and len(eval_json['choices']) > 0:
            # 使用完整响应而不是只取 content
            result = eval_response.text
            # 只保留content部分，不包含reasoning内容
            # result = eval_json['choices'][0]['message']['content']
            print("评估完成")
        else:
            result = "评估失败：无法获取有效响应"
            print("评估响应格式错误")
        evaluation_results.append(result)
    except Exception as e:
        error_msg = f"评估错误: {str(e)}"
        print(error_msg)
        evaluation_results.append(error_msg)

# 添加评估结果并保存
df['DeepSeek-R1评估'] = evaluation_results
df.to_excel('mydata/model_responses.xlsx')
print("\n所有结果（包括评估）已保存到 mydata/model_responses.xlsx")
