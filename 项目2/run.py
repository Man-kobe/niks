

import os
from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()

# 从环境变量中获取API密钥


from openai import OpenAI

client = OpenAI(
    api_key = "sk-oPEyNK4Iqr0Tta4jkhpsG91HgPLm0SRr62mLwxQKPfCZ3sZC",
    base_url = "https://api.moonshot.cn/v1",
)


# ... 其余代码保持不变 ...

history = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。：请遵守以下规则1、一次回答中，在五十个汉字以内更好地回答，如果提问者说“详细一点”，则没有字数限制。2、一般情况下用中文回答，如果提问者说“用英文回答”，则用英文回答。3、如果不知道答案，请回答“对不起，我还不知道。”4、如果提问者提相同问题，则以第一次的回答为答案回答。"}
]

# 定义提示词和相应回答
prompts_and_responses = [
    ("你好", "你好！很高兴认识你。我是Kimi，由 Moonshot AI 提供的人工智能助手。有什么我可以帮助你的吗？"),
    ("我不开心", "我理解你的感受，但是请记住，无论遇到什么困难，都有解决的办法。保持积极的心态，相信自己，你会找到解决问题的方法的。"),
    ("Moonshot AI", "Moonshot AI 是一家专注于人工智能技术的公司，他们开发了我这个AI助手。"),
    ("你能做什么", "作为一个AI助手，我可以回答问题、提供信息、协助解决问题等。但请记住，我不能替代人类的判断和专业建议。"),
    ("再见", "再见！如果还有任何问题，随时欢迎再来询问。祝你有个愉快的一天！")
]

# 函数用于匹配用户输入和预定义的提示词
def match_prompt(user_input):
    for prompt, response in prompts_and_responses:
        if prompt.lower() in user_input.lower():
            return response
    return None

# ... (前面的代码保持不变)

def chat(query, history):
    # 先检查是否匹配预定义的提示词
    matched_response = match_prompt(query)
    if matched_response:
        print("Kimi:", matched_response)
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": matched_response})
        return

    history.append({
        "role": "user", 
        "content": query
    })
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,  # 这里使用整个对话历史
        temperature=0.3,
        stream=True
    )
    
    result = ""
    print("Kimi:", end=" ", flush=True)
    for chunk in completion:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            result += content
    
    print()  # 添加最后的换行
    
    history.append({
        "role": "assistant",
        "content": result
    })

# ... (后面的代码保持不变)
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
        stream=True
    )
    
    result = ""
    print("Kimi:", end=" ", flush=True)
    for chunk in completion:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            result += content
    
    print()  # 添加最后的换行
    
    history.append({
        "role": "assistant",
        "content": result
    })

# 主循环
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', '退出']:
        print("感谢使用，再见！")
        break
    chat(user_input, history)
    import time
# ... 其他导入保持不变 ...

def chat(query, history):
    # ... 前面的代码保持不变 ...
    
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=history,
                temperature=0.3,
                stream=True
            )
            # ... 处理响应的代码 ...
            break  # 如果成功，跳出循环
        except Exception as e:
            if "rate limit" in str(e).lower():
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    print(f"遇到速率限制，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                else:
                    print("达到最大重试次数，请稍后再试。")
                    return
            else:
                print(f"发生错误: {e}")
                return