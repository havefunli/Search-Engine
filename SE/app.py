from MyCode.Query import QueryWebPages
from flask import Flask, request, render_template

# 创建 Flask 应用实例
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  # 返回包含表单的 HTML 页面


@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form.get('user_input')

    if user_input:
        processed_input = user_input.upper()  # 示例：将输入转换为大写
        return f"处理后的内容是: {QueryWebPages(user_input)}"
    else:
        return "没有输入内容，请重新提交。"


if __name__ == '__main__':
    app.run(debug=True)  # 启动 Flask 应用

