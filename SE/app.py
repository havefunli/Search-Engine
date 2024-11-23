from flask import Flask, request, render_template, session, jsonify, redirect, url_for
from flask_session import Session
import pandas as pd
from MyCode.Query import QueryWebPages

app = Flask(__name__)

# 配置 Flask-Session
app.config['SECRET_KEY'] = 'your_very_secret_key_here'  # 设置 SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'  # 存储在本地文件系统
app.config['SESSION_FILE_DIR'] = './flask_session/'  # 存储路径
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# 每页显示的条数
ITEMS_PER_PAGE = 20

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form.get('user_input')
    if user_input:
        # 获取查询结果（假设返回一个 DataFrame）
        result_df = QueryWebPages(user_input)
        results = result_df.to_dict(orient='records')

        # 存储结果到服务器端 session
        session['search_results'] = results

        # 总页数计算
        total_pages = -(-len(results) // ITEMS_PER_PAGE)

        # 渲染结果页面
        return render_template(
            'result.html',
            total_pages=total_pages,
            current_page=1
        )

    return redirect(url_for('index'))


@app.route('/get_page/<int:page>')
def get_page(page):
    results = session.get('search_results', [])
    if not results:
        return jsonify({'error': 'No cached results'}), 400

    # 分页逻辑
    total_pages = -(-len(results) // ITEMS_PER_PAGE)
    if page < 1 or page > total_pages:
        return jsonify({'error': 'Invalid page number'}), 400

    page_data = paginate_results(results, page)
    return jsonify({
        "results": page_data,
        "current_page": page,
        "total_pages": total_pages
    })


def paginate_results(results, page):
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return results[start:end]


if __name__ == '__main__':
    app.run(debug=True)
