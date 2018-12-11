# coding:utf-8
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegisterForm, LoginForm
from app.models import User, Userlog
from app import db
from werkzeug.security import generate_password_hash
import uuid
from functools import wraps


# 用于检查用户是否登录的装饰器
def admin_login_req(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if "user" not in session:
			return redirect(url_for("home.login", next=request.url))
		return func(*args, **kwargs)
	return decorated_function


# 会员注册
@home.route("/regist/", methods=['GET', 'POST'])
def regist():
	form = RegisterForm()
	if form.validate_on_submit():
		data = form.data
		user = User(
			name = data['name'],
			pwd = generate_password_hash( data['pwd']),
			email = data['email'],
			phone = data['phone'],
			uuid = uuid.uuid4().hex
		)
		db.session.add(user)
		db.session.commit()
		flash("注册成功", "ok")
	return render_template("home/regist.html", form=form)

@home.route("/login/", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=data['name']).first()
		if not user.check_pwd(data['pwd']):
			flash('密码错误', 'err')
			return render_template("home/login.html", form=form)
		session['user'] = data['name']
		session['user_id'] = user.id
		userlog = Userlog(
			user_id = user.id,
			ip = request.remote_addr
		)
		db.session.add(userlog)
		db.session.commit()
		return redirect(url_for('home.user'))
	return render_template("home/login.html", form=form)

@home.route("/logout/")
def logout():
	session.pop("user", None)
	session.pop("user_id", None)
	return redirect(url_for("home.login"))

@home.route("/user/")
@admin_login_req
def user():
	return render_template("/home/user.html")

@home.route("/pwd/")
@admin_login_req
def pwd():
	return render_template("/home/pwd.html")

@home.route("/comments/")
@admin_login_req
def comments():
	return render_template("/home/comments.html")

@home.route("/loginlog/")
@admin_login_req
def loginlog():
	return render_template("/home/loginlog.html")

@home.route("/moviecol/")
@admin_login_req
def moviecol():
	return render_template("/home/moviecol.html")

@home.route("/")
def index():
	return render_template("home/index.html")

@home.route("/animation")
def animation():
	return render_template("home/animation.html")

@home.route("/search/")
def search():
	return render_template("home/search.html")

@home.route("/play/")
def play():
	return render_template("home/play.html")

