# coding:utf-8
from . import home
import os
import datetime
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegisterForm, LoginForm, UserdetailForm, PwdForm, CommentForm
from app.models import User, Userlog, Preview, Tag, Movie, Comment
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

@home.route("/comments/<int:page>/", methods=['GET'])
@admin_login_req
def comments(page=None):
	if page == None:
		page= 1
	page_data = Comment.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == Comment.movie_id,
		User.id == session['user_id']
	).order_by(
		Comment.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template("/home/comments.html", page_data=page_data)

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

# 首页
@home.route("/<int:page>/", methods=['GET', 'POST'])
def index(page=None):
	tags = Tag.query.all()
	page_data = Movie.query
	# 标签
	tid = request.args.get('tid', 0)
	if int(tid) !=0:
		page_data = page_data.filter_by(tag_id=int(tid))
	# 星级
	star = request.args.get('star', 0)
	if int(star) != 0:
		page_data = page_data.filter_by(star=int(star))
	# 上映时间
	time = request.args.get('time', 0)
	if int(time) != 0:
		if int(time) == 1:
			page_data = page_data.order_by(
				Movie.addtime.desc()
			)
		else:
			page_data = page_data.order_by(
				Movie.addtime.asc()
			)
	# 播放量
	pm = request.args.get('pm', 0)
	if int(pm) != 0:
		page_data = page_data.order_by(
			Movie.playnum.desc()
		)
	else:
		page_data = page_data.order_by(
			Movie.playnum.asc()
		)
	# 评论量
	cm = request.args.get('cm', 0)
	if int(cm) != 0:
		page_data = page_data.order_by(
			Movie.commentnum.desc()
		)
	else:
		page_data = page_data.order_by(
			Movie.commentnum.asc()
		)
	if page is None:
		page = 1
	page_data = page_data.paginate(page=page, per_page=8)
	p = dict(
		tid= tid,
		star= star, 
		time= time,
		pm= pm,
		cm= cm

	)
	return render_template("home/index.html", tags = tags, p=p, page_data=page_data)

@home.route("/animation")
def animation():
	data = Preview.query.all()
	return render_template("home/animation.html", data=data)

@home.route("/search/<int:page>/", methods=['GET'])
def search(page=None):
	if page is None:
		page = 1
	key = request.args.get("key", "")
	movie_count = Movie.query.filter(
		Movie.title.ilike("%" + key + "%")
	).count()
	page_data = Movie.query.filter(
		Movie.title.ilike("%" + key + "%")
	).order_by(
		Movie.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template("home/search.html",movie_count=movie_count, key=key, page_data=page_data)

@home.route("/play/<int:id>/<int:page>/", methods=['GET', 'POST'])
def play(id=None, page=None):
	movie = Movie.query.get_or_404(int(id))
	form = CommentForm()
	movie.playnum += 1
	if page == None:
		page= 1
	page_data = Comment.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == movie.id,
		User.id == Comment.user_id
	).order_by(
		Comment.addtime.desc()
	).paginate(page=page, per_page=10)
	if "user" in session and form.validate_on_submit():
		data = form.data
		comment = Comment(
			content = data['content'],
			movie_id = movie.id,
			user_id = session['user_id'],
		)
		movie.commentnum += 1
		db.session.add(comment)
		db.session.add(movie)
		db.session.commit()
		flash('追加评论成功', 'ok')
		return redirect(url_for('home.play', id=movie.id, page=1))
	db.session.add(movie)
	db.session.commit()
	return render_template("home/play.html", movie=movie, form=form, page_data=page_data)

