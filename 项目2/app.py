from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'b9f8e9f1e0d9c8a7b6f5e4d3c2b1a0'  # 这里使用生成的密钥

users = {}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('inDex.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return 'User already exists'
        if len(password) != 6:
            return 'Password must be 6 characters long'

        users[username] = password
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.get(username) == password:
            session['username'] = username
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
        # 这里你可以添加调用AI模型的代码来回答问题
        answer = "这是一个示例答案。"
        return render_template('qa.html', question=question, answer=answer)
    return render_template('qa.html')

if __name__ == '__main__':
    app.run(debug=True)