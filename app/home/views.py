# coding:utf-8
from . import home
import os
import datetime
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegisterForm, LoginForm, UserdetailForm, PwdForm
from app.models import User, Userlog
from app import db, app
from werkzeug.utils import secure_filename
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

# 用于修改表单提交中的文件名
def change_filename(filename):
	fileinfo = os.path.splitext(filename)
	filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinfo[-1]
	return filename

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

# 会员登录
@home.route("/login/", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=data['name']).first()
		print('aaaa', user.name)
		print('aaaa', user.pwd)
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

@home.route("/user/", methods=['GET', 'POST'])
@admin_login_req
def user():
	form = UserdetailForm()
	user = User.query.get(int(session['user_id']))
	if request.method == 'GET':
		form.name.data = user.name
		form.email.data = user.email
		form.phone.data = user.phone
		form.info.data = user.info
		form.face.data = user.face
	if form.validate_on_submit():
		data = form.data
		file_face = secure_filename(form.face.data.filename)
		if not os.path.exists(app.config["FC_DIR"]):
			os.makedirs(app.config["FC_DIR"])
			os.chmod(app.config["FC_DIR"], "rw")
		user.face = change_filename(file_face)
		form.face.data.save(app.config["FC_DIR"] + user.face)
		name_count = User.query.filter_by(name=data["name"]).count()
		if data["name"] != user.name and name_count == 1:
			flash("昵称已经存在！", "err")
			return redirect(url_for("home.user"))
		email_count = User.query.filter_by(email=data["email"]).count()
		if data["email"] != user.email and email_count == 1:
			flash("邮箱已经存在！", "err")
			return redirect(url_for("home.user"))
		phone_count = User.query.filter_by(phone=data["phone"]).count()
		if data["phone"] != user.phone and phone_count == 1:
			flash("手机号码已经存在！", "err")
			return redirect(url_for("home.user"))
		user.name = data["name"]
		user.email = data["email"]
		user.phone = data["phone"]
		user.info = data["info"]
		db.session.add(user)
		db.session.commit()
		flash("修改成功！", "ok")
		return redirect(url_for("home.user"))
	return render_template("/home/user.html", form=form, user=user)

@home.route("/pwd/", methods=['GET', 'POST'])
@admin_login_req
def pwd():
	form = PwdForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=session['user']).first()
		if not user.check_pwd(data['old_pwd']):
			flash('旧密码错误', 'err')
			return redirect(url_for('home.pwd'))
		user.pwd = generate_password_hash(data['new_pwd'])
		db.session.add(user)
		db.session.commit()
		flash("修改密码成功, 请重新登录", "ok")
		return redirect(url_for('home.logout'))
	return render_template("/home/pwd.html", form=form)

@home.route("/comments/")
@admin_login_req
def comments():
	return render_template("/home/comments.html")

# 会员登录日志
@home.route("/loginlog/<int:page>/", methods=['GET'])
@admin_login_req
def loginlog(page=None):
	page_data = Userlog.query.filter_by(
		user_id = int(session['user_id'])
	).order_by(
		Userlog.addtime.desc()
	).paginate(page=page, per_page=1)
	return render_template("/home/loginlog.html", page_data=page_data)

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

