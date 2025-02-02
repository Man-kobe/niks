from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='public')
CORS(app)

API_KEY = os.getenv('DEEPSEEK_API_KEY')
API_URL = 'https://api.deepseek.com/chat/completions'

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# 添加环境变量检查
if not API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        
        # 添加请求数据验证
        if not data or 'messages' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        # 添加请求超时设置
        response = requests.post(
            API_URL,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json={
                'model': 'deepseek-chat',
                'messages': data['messages'],
                'stream': False
            },
            timeout=10  # 添加10秒超时
        )
        
        response.raise_for_status()
        return jsonify(response.json())
        
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {str(e)}")
        return jsonify({'error': 'Failed to communicate with DeepSeek API'}), 502
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000) 