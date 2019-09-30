import os
import random
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/get_captcha', methods=['GET'])
def get_captcha():
    img_list = os.listdir("static/captcha")
    img = img_list[random.randint(0, 1000)]
    return os.path.join("static/captcha", img)


if __name__ == '__main__':
    app.run()
