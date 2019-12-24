from flask import Flask, request, render_template
from models import t_students
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_paginate import Pagination

engine = create_engine("mysql+pymysql://root:qwer1234@127.0.0.1/flask")
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)


@app.route('/index')
def index(limit=10):
    sess = DBSession()
    data = sess.query(t_students).all()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    paginate = Pagination(page=page, total=len(data))
    ret = sess.query(t_students).slice(start, end)
    return render_template("index.html", data=ret, paginate=paginate)


@app.route('/main', methods=['GET'])
def main():
    return render_template("main.html")


@app.route('/get_data', methods=['POST'])
def get_data():
    sess = DBSession()
    data = sess.query(t_students).all()
    limit = int(request.form.get("pageSize"))
    page = int(request.form.get("currentPage"))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    ret = [{"id": data[i].stu_id, "name": data[i].stu_name} for i in range(start, end)]
    return {"data": ret, "count": len(data)}


if __name__ == '__main__':
    app.run()
