from flask import Flask, render_template
from chatgpt_example import chat_with_chatgpt
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test/<int:post_id>/")
def hello_post(post_id):
    return f"<p>User-{escape(post_id)}, </p>"

@app.route("/test/<path:subpath>/")
def hello_path(subpath):
    return f"<p>Post{escape(subpath)} </p>"

@app.route("/text/<user_message>")
def hello_home(user_message):
    response = chat_with_chatgpt(
        user_message=user_message,
        system_prompt="你是一位中式廚師，有人向你請教煮菜"

    )
    return response

@app.route("/sample/")
def show_html_sample():
    return render_template("sample.html", 
                            name='koko',
                            numbers = [1,2,3,4,5],
                            paris = [('A',1), ('B',2)],
                            dict = {
                                'apple':6,
                                'banana':4,
                            }
    )



# 如果要使用 python .\xxx.py 執行
if __name__ == '__main__':
    app.run(debug=True)