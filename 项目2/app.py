from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'b9f8e9f1e0d9c8a7b6f5e4d3c2b1a0'  # 这里使用生成的密钥

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Flask-Session配置

users = {}

# 加载 .env 文件
load_dotenv()

# 从环境变量中获取API密钥
client = OpenAI(
    api_key= "sk-oPEyNK4Iqr0Tta4jkhpsG91HgPLm0SRr62mLwxQKPfCZ3sZC",
    base_url="https://api.moonshot.cn/v1",
)

history = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全、有帮助、准确的回答。"},
]

# 定义提示词和相应回答
prompts_and_responses = [
    ("你好", "你好！很高兴认识你。我是Kimi，由 Moonshot AI 提供的人工智能助手。有什麽我可以帮助你的吗？"),
    ("我不开心", "我理解你的感受，但是请记住，无论遇到什麽困难，都有解决的办法。保持积极的心态，相信自己，你会找到解决问题的办法的。"),
    ("Moonshot AI", "Moonshot AI 是一家专注于人工智能技术的公司，他们开发了我这个AI助手。"),
    ("你能做什麽", "作为一个AI助手，我可以回答问题、提供信息、协助解决问题等。但是请记住，我不能替代人类的判断和专业建议。"),
    ("再见", "再见！如果还有任何问题，随时欢迎再来咨询。祝你有个愉快的一天！")
]

# 定义匹配提示词的函数
def match_prompt(user_input):
    for prompt, response in prompts_and_responses:
        if prompt.lower() in user_input.lower():
            return response
    return None

# 定义 chat 函数
def chat(query, history):
    matched_response = match_prompt(query)
    if matched_response:
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": matched_response})
        return matched_response

    history.append({"role": "user", "content": query})
    
    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=history,
                temperature=0.3,
                stream=True,
                timeout=60  # 增加超时时间为60秒
            )
            break
        except RateLimitError as e:
            if attempt < retry_attempts - 1:
                time.sleep(2)  # 等待2秒后重试
            else:
                return "请求超时，请稍后再试。"

    result = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            result += content

    history.append({"role": "assistant", "content": result})
    return result

db = SQLAlchemy(app)
Session(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return 'User already exists'
        if len(password) != 6:
            return 'Password must be 6 characters long'

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['messages'] = []  # 初始化会话中的消息列表
            session.permanent = True  # 使用永久会话
            return redirect(url_for('home'))
        return 'Invalid username or password'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/qa', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        question = request.form['question']
        answer = chat(question, history)
        user_message = Message(sender='user', text=question)
        ai_message = Message(sender='ai', text=answer)
        db.session.add(user_message)
        db.session.add(ai_message)
        db.session.commit()
        return redirect(url_for('qa'))

    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('qa.html', messages=messages)

@app.route('/clear-chat-history', methods=['POST'])
def clear_chat_history():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            Message.query.delete()  # 删除所有消息记录
            db.session.commit()
            return {'success': True}
    return {'success': False}

if __name__ == '__main__':
    app.run(debug=True)