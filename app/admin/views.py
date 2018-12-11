from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Oplog, Adminlog, Userlog, Auth, Role
from functools import wraps
from app import db, app
import math
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import datetime
import uuid


# 上下文处理器
@admin.context_processor
def tpl_extra():
	data = dict(
		online_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
	)
	return data

# 用于检查用户是否登录的装饰器
def admin_login_req(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if "admin" not in session:
			return redirect(url_for("admin.login", next=request.url))
		return func(*args, **kwargs)
	return decorated_function

# 权限控制装饰器
def admin_auth(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		# 首先查出当前登录的管理员用户
		admin = Admin.query.join(
			Role
		).filter(
			Admin.role_id == Role.id,
			Admin.id == session['admin_id']
		).first()
		# 得到当前管理员用户所支持的所有权限
		auths = admin.role.auths
		# 将当前管理员用户所支持的所有权限转换为一个list, 该list中的数据为int类型
		auths = list(map(lambda x : int(x), auths.split(',')))
		auth_list = Auth.query.all()
		# 通过所支持的权限得到对应所支持的url
		urls = [ auth.url for auth_id in auths for auth in auth_list if auth_id == auth.id ]
		print('urls:',urls)
		# 当前访问的页面url
		rule = request.url_rule
		print('rule:',rule)
		if str(rule) not in urls:
			abort(404)
		return f(*args, **kwargs)
	return decorated_function

# 用于修改表单提交中的文件名
def change_filename(filename):
	fileinfo = os.path.splitext(filename)
	filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinfo[-1]
	return filename


@admin.route("/")
@admin_login_req
def index():
	return render_template("admin/index.html")

@admin.route("/login/", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# 获取用户提交的表单数据
		data = form.data
		# 根据用户输入的账号查询数据库获取一条账户信息
		admin = Admin.query.filter_by(name=data["account"]).first()
		# 调用在models中定义的check_pwd方法查询密码
		if not admin.check_pwd(data["pwd"]):
			flash("密码错误!", 'err')
			return render_template("admin/login.html",form=form)
		# 将账户账号存入session
		session["admin"] = data["account"]
		session["admin_id"] = admin.id

		adminlog = Adminlog(
			admin_id = session['admin_id'],
			ip = request.remote_addr
		)
		db.session.add(adminlog)
		db.session.commit()
		return redirect(request.args.get("next") or url_for("admin.index"))
	return render_template("admin/login.html",form=form)

# 管理员退出登录
@admin.route("/logout/")
@admin_login_req
def logout():
	# 删除session中的账户信息
	session.pop("admin", None)
	session.pop("admin_id", None)
	return redirect(url_for("admin.login"))

# 修改密码
@admin.route("/pwd/", methods=['GET', 'POST'])
@admin_login_req
def pwd():
	form = PwdForm()
	if form.validate_on_submit():
		data = form.data
		admin = Admin.query.filter_by(name=session['admin']).first()
		admin.pwd = generate_password_hash(data['new_pwd'])
		db.session.add(admin)
		db.session.commit()
		flash('修改密码成功, 请重新登录', 'ok')
		return redirect(url_for('admin.logout'))
	return render_template("admin/pwd.html", form=form)

# 添加标签
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_add():
	form = TagForm()
	if form.validate_on_submit():
		data = form.data
		# 通过标签名字段查询数据库中的tag表获取一条查询集
		tag = Tag.query.filter_by(name=data["name"]).count()
		if tag == 1:
			flash("名称已经存在", "err")
			return redirect(url_for('admin.tag_add'))
		tag = Tag(
			name = data["name"]
		)
		db.session.add(tag)
		db.session.commit()
		# 将此次添加标签的操作数据记录在操作日志数据库中
		oplog = Oplog(
			admin_id = session["admin_id"],
			ip=request.remote_addr,
			reason="添加标签%s" % data["name"]
		)
		db.session.add(oplog)
		db.session.commit()
		flash("添加成功", "ok")
		redirect(url_for('admin.tag_add'))
	return render_template("admin/tag_add.html", form=form)

# 编辑标签
@admin.route("/tag/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_edit(id=None):
	form = TagForm()
	tag = Tag.query.get_or_404(id)
	if form.validate_on_submit():
		data = form.data
		# 如果用户输入的标签名与编辑标签时拿到的标签一样则不用对数据库进行修改
		if tag.name == data['name']:
			flash("未作任何修改", "ok")
		else:
			# 查询用户输入表单中的标签名在数据库中的个数
			tag_count = Tag.query.filter_by(name=data["name"]).count()
			# 如果用户输入的标签名在数据库中已经存在也就是 tag_count == 1
			if tag_count == 1:
				flash("名称已经存在", "err")
				return redirect(url_for('admin.tag_edit', id=id))
			# 修改
			tag.name = data['name']
			db.session.add(tag)
			db.session.commit()
			flash("修改成功", "ok")
		redirect(url_for('admin.tag_edit', id=id))
	return render_template("admin/tag_edit.html", form=form, tag=tag)

# 删除标签
@admin.route("/tag/del/<int:id>/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def tag_del(id=None, page=None):
	# 通过标签id查询出需要删除的标签字段, first_or_404: 查询到无条目时会返回一个404错误, 而不是返回None
	tag = Tag.query.filter_by(id=id).first_or_404()
	# 删除标签并提交
	db.session.delete(tag)
	db.session.commit()
	# 查询出所有标签的总数
	alltag = Tag.query.all()
	# 向上取整, 如果总共有三个标签, 则页码数应为2
	page_num = math.ceil(len(alltag)/ 2)
	# 如果当前的页码数大于删除之后的标签总数, 则跳转到删除之后的最大页码数
	if page_num < page and page_num != 0:
		page = page_num
	flash("删除成功", "ok")
	# 重定向到tag_list页面, 并传入当前页码数
	return redirect(url_for('admin.tag_list', page=page))

# 标签列表
@admin.route("/tag/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def tag_list(page=None):
	if page is None:
		page = 1
	page_data = Tag.query.order_by(
		Tag.addtime.desc()
	).paginate(page=page, per_page=2) # per_page: 一页显示的条数
	return render_template("admin/tag_list.html", page_data=page_data)

# 添加电影
@admin.route("/movie/add/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def movie_add():
	form = MovieForm()
	if form.validate_on_submit():
		data = form.data
		file_url = secure_filename(form.url.data.filename)
		file_logo = secure_filename(form.logo.data.filename)
		if not os.path.exists(app.config['UP_DIR']):
			os.makedirs(app.config['UP_DIR'])
			os.chmod(app.config['UP_DIR'], 'rw')
		url = change_filename(file_url)
		logo = change_filename(file_logo)
		form.url.data.save(app.config['UP_DIR'] + url)
		form.logo.data.save(app.config['UP_DIR'] + logo)
		movie = Movie(
			title = data['title'],
			url = url,
			info = data['info'],
			logo = logo,
			star = int(data['star']),
			playnum = 0,
			commentnum = 0,
			tag_id = data['tag_id'],
			area = data['area'],
			length = data['length'],
			release_time = data['release_time'],
		)
		db.session.add(movie)
		db.session.commit()
		flash("添加电影成功", "ok")
		return redirect(url_for('admin.movie_add'))
	return render_template("admin/movie_add.html", form=form)

# 编辑电影
@admin.route("/movie/edit/<int:id>/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def movie_edit(id):
	form = MovieForm()
	form.url.validators = []
	form.logo.validators = []
	movie = Movie.query.get_or_404(id)
	if request.method == "GET":
		form.info.data = movie.info
		form.tag_id.data = movie.tag_id
		form.star.data = movie.star 
	if form.validate_on_submit():
		data = form.data
		movie_count = Movie.query.filter_by(title=data['title']).count()
		if movie_count == 1 and movie.title != data['title']:
			flash('片名已经存在', 'err')
			return redirect(url_for('admin.movie_edit', id=id))

		if not os.path.exists(app.config['UP_DIR']):
			os.makedirs(app.config['UP_DIR'])
			os.chmod(app.config['UP_DIR'], 'rw')
		
		# 将用户输入的电影文件下载到本地
		if form.url.data.filename != "":
			file_url = secure_filename(form.url.data.filename)
			movie.url = change_filename(file_url)
			form.url.data.save(app.config['UP_DIR'] + movie.url)

		if form.logo.data.filename != "":
			file_logo = secure_filename(form.logo.data.filename)
			movie.logo = change_filename(file_logo)
			form.logo.data.save(app.config['UP_DIR'] + movie.logo)

		movie.star = data['star']
		movie.tag_id = data['tag_id']
		movie.info = data['info']
		movie.area = data['area']
		movie.title = data['title']
		movie.length = data['length']
		movie.release_time = data['release_time']
		db.session.add(movie)
		db.session.commit()

		flash("修改电影成功", "ok")
		return redirect(url_for('admin.movie_edit', id=id))
	return render_template("admin/movie_edit.html", form=form, movie=movie)

# 删除电影
@admin.route("/movie/del/<int:id>/<int:page>/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def movie_del(id=None, page=None):
	movie = Movie.query.filter_by(id=id).first_or_404()
	db.session.delete(movie)
	db.session.commit()
	allmovie = Movie.query.all()
	page_num = math.ceil(len(allmovie)/2)
	if page_num < page and page_num != 0:
		page = page_num
	flash('删除成功', 'ok')
	return redirect(url_for("admin.movie_list", page=page))

# 电影列表
@admin.route("/movie/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def movie_list(page):
	if page is None:
		page = 1
	page_data = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id
	).order_by(
		Movie.addtime.desc()
	).paginate(page=page, per_page=2) # per_page: 一页显示的条数
	return render_template("admin/movie_list.html", page_data=page_data)

# 添加预告
@admin.route("/preview/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_add():
	form = PreviewForm()
	if form.validate_on_submit():
		data = form.data
		file_logo = secure_filename(form.logo.data.filename)
		if not os.path.exists(app.config["UP_DIR"]):
			os.makedirs(app.config['UP_DIR'])
			os.chmod(app.config['UP_DIR'], 'rw')
		logo = change_filename(file_logo)
		form.logo.data.save(app.config["UP_DIR"] + logo)
		preview = Preview(
			title = data['title'],
			logo = logo
		)
		db.session.add(preview)
		db.session.commit()
		flash("添加预告成功", "ok")
		return redirect(url_for("admin.preview_add"))
	return render_template("admin/preview_add.html", form=form)

# 编辑预告
@admin.route("/preview/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_edit(id=None):
	form = PreviewForm()
	form.logo.validators = []
	preview = Preview.query.get_or_404(id)
	if request.method == 'GET':
		form.title.data = preview.title
	if form.validate_on_submit():
		data = form.data
		preview_count = Preview.query.filter_by(title=data['title']).count()
		if preview_count == 1 and data['title'] != preview.title:
			flash('预告名已经存在', 'err')

		if not os.path.exists(app.config['UP_DIR']):
			os.makedirs(app.config['UP_DIR'])
			os.chmod(app.config['UP_DIR'], 'rw')
		
		if form.logo.data.filename != "":
			file_logo = secure_filename(form.logo.data.filename)
			preview.logo = change_filename(file_logo)
			form.logo.data.save(app.config['UP_DIR'] + preview.logo)

		preview.title = data['title']
		# preview.logo = logo
		db.session.add(preview)
		db.session.commit()

		flash('修改预告成功', 'ok')
		return redirect(url_for('admin.preview_edit', id=id))
	return render_template('admin/preview_edit.html', form=form, preview=preview)

# 删除预告
@admin.route("/preview/del/<int:id>/<int:page>/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def preview_del(id=None, page=None):
	preview = Preview.query.filter_by(id=id).first_or_404()
	db.session.delete(preview)
	db.session.commit()
	allpreview = Preview.query.all()
	page_num = math.ceil(len(allpreview)/2)
	if page_num < page and page_num != 0:
		page = page_num
	flash('删除成功', 'ok')
	return redirect(url_for('admin.preview_list', page=page))

# 预告列表
@admin.route("/preview/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def preview_list(page=None):
	if page is None:
		page = 1
	page_data = Preview.query.order_by(
		Preview.addtime.desc()
	).paginate(page=page, per_page=2) # per_page: 一页显示的条数
	return render_template("admin/preview_list.html", page_data=page_data)

# 会员查看
@admin.route("/user/view/<int:id>/", methods=['GET'])
@admin_login_req
@admin_auth
def user_view(id):
	user = User.query.get_or_404(id)
	return render_template("admin/user_view.html", user=user)

# 会员删除
@admin.route("/user/del/<int:id>/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def user_del(id=None, page=None):
	user = User.query.filter_by(id=id).first_or_404()
	db.session.delete(user)
	db.session.commit()
	alluser = User.query.all()
	page_num = math.ceil(len(alluser) / 10)
	if page_num < page and page_num != 0:
		page = page_num
	flash('删除会员成功', 'ok')
	return redirect(url_for('admin.user_list', page=page))

# 会员列表
@admin.route("/user/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def user_list(page=None):
	if page is None:
		page = 1
	page_data = User.query.order_by(
		User.addtime.desc()
	).paginate(page=page, per_page=10) # per_page: 一页显示的条数
	return render_template("admin/user_list.html", page_data=page_data)

# 评论删除
@admin.route("/comment/del/<int:id>/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def comment_del(id=None, page=None):
	comment = Comment.query.filter_by(id=id).first_or_404()
	db.session.delete(comment)
	db.session.commit()
	allcomment = Comment.query.all()
	page_num = math.ceil(len(allcomment) / 5)
	if page_num < page and page_num != 0:
		page = page_num
	flash('删除评论成功', 'ok')
	return redirect(url_for("admin.comment_list", page=page))

# 评论列表
@admin.route("/comment/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def comment_list(page=None):
	if page is None:
		page = 1
	page_data = Comment.query.join(
		User
	).join(
		Movie
	).filter(
		User.id == Comment.user_id,
		Movie.id == Comment.movie_id
	).order_by(
		User.addtime.desc()
	).paginate(page=page, per_page=5) # per_page: 一页显示的条数
	return render_template("admin/comment_list.html", page_data=page_data)

# 电影收藏删除
@admin.route("/moviecol/del/<int:id>/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_del(id=None, page=None):
	moviecol = Moviecol.query.filter_by(id=id).first_or_404()
	db.session.delete(moviecol)
	db.session.commit()
	allmoviecol = Moviecol.query.all()
	page_num = math.ceil(len(allmoviecol) / 5)
	if page_num < page and page_num != 0:
		page = page_num
	flash('删除收藏成功', 'ok')
	return redirect(url_for("admin.moviecol_list", page=page))

# 电影收藏列表
@admin.route("/moviecol/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_list(page=None):
	if page is None:
		page = 1
	page_data = Moviecol.query.join(
		User
	).join(
		Movie
	).filter(
		User.id == Moviecol.user_id,
		Movie.id == Moviecol.movie_id
	).order_by(
		Moviecol.addtime.desc()
	).paginate(page=page, per_page=5)

	return render_template("admin/moviecol_list.html", page_data=page_data)

# 操作日志列表
@admin.route("/oplog/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def oplog_list(page=None):
	if page is None:
		page = 1
	page_data = Oplog.query.join(
		Admin
	).filter(
		Admin.id == Oplog.admin_id
	).order_by(
		Oplog.addtime.desc()
	).paginate(page=page, per_page=10) # per_page: 一页显示的条数

	return render_template("admin/oplog_list.html", page_data=page_data)

# 管理员登录日志列表
@admin.route("/adminloginlog/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
	if page is None:
		page = 1
	page_data = Adminlog.query.join(
		Admin
	).filter(
		Admin.id == Adminlog.admin_id
	).order_by(
		Adminlog.addtime.desc()
	).paginate(page=page, per_page=10) # per_page: 一页显示的条数
	return render_template("admin/adminloginlog_list.html", page_data=page_data)

# 用户登录日志列表
@admin.route("/userloginlog/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
	if page is None:
		page = 1
	page_data = Userlog.query.join(
		User
	).filter(
		User.id == Userlog.user_id
	).order_by(
		Userlog.addtime.desc()
	).paginate(page=page, per_page=10) # per_page: 一页显示的条数
	return render_template("admin/userloginlog_list.html", page_data=page_data)

# 角色添加
@admin.route("/role/add/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def role_add():
	form = RoleForm()
	data = form.data
	if form.validate_on_submit():
		data = form.data
		role = Role(
			name = data['name'],
			auths = ",".join(map(lambda x : str(x), data['auths']))
		)
		db.session.add(role)
		db.session.commit()
		flash('添加角色成功', 'ok')
	return render_template("admin/role_add.html", form=form)

# 角色删除
@admin.route("/role/del/<int:id>/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def role_del(id=None, page=None):
	role = Role.query.filter_by(id=id).first_or_404()
	db.session.delete(role)
	db.session.commit()
	allrole = Role.query.all()
	page_num = math.ceil(len(allrole)/2)
	if page_num < page and page_num != 0:
		page = page_num
	flash ('删除角色成功', 'ok')
	return redirect(url_for("admin.role_list", page=page))

# 角色编辑
@admin.route("/role/edit/<int:id>/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def role_edit(id=None):
	form = RoleForm()
	role = Role.query.get_or_404(id)
	if request.method == "GET":
		auths = role.auths
		form.auths.data = list(map(lambda v: int(v), auths.split(",")))
	if form.validate_on_submit():
		data = form.data
		if role.name == data['name'] and role.auths == data['auths']:
			flash("未作任何修改", "ok")
		else:
			# 修改
			
			role.name = data['name']
			role.auths =  ",".join(map(lambda v: str(v), data["auths"]))
			db.session.add(role)
			db.session.commit()
			flash("修改成功", "ok")
		redirect(url_for('admin.auth_edit', id=id))
	return render_template('admin/role_edit.html',form=form, role=role)

# 角色列表
@admin.route("/role/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def role_list(page=None):
	if page is None:
		page = 1
	page_data = Role.query.order_by(
		Role.addtime.desc()
	).paginate(page=page, per_page=2) # per_page: 一页显示的条数
	return render_template("admin/role_list.html", page_data=page_data)

# 权限添加
@admin.route("/auth/add/", methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def auth_add():
	form = AuthForm()
	if form.validate_on_submit():
		data = form.data
		auth = Auth(
			name=data['name'],
			url=data['url']
		)
		db.session.add(auth)
		db.session.commit()
		flash('添加权限成功', 'ok')
	return render_template("admin/auth_add.html", form=form)

# 权限编辑
@admin.route('/auth/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def auth_edit(id):
	form = AuthForm()
	auth = Auth.query.get_or_404(id)
	if form.validate_on_submit():
		data = form.data
		# 如果用户输入的权限名与编辑权限时拿到的权限一样则不用对数据库进行修改
		if auth.name == data['name'] and auth.url == data['url']:
			flash("未作任何修改", "ok")
		else:
			# 修改 
			auth.name = data['name']
			auth.url = data['url']
			db.session.add(auth)
			db.session.commit()
			flash("修改成功", "ok")
		redirect(url_for('admin.auth_edit', id=id))
	return render_template("admin/auth_edit.html", form=form, auth=auth)

# 权限删除
@admin.route("/auth/del/<int:id>/<int:page>/", methods=['GET'])
@admin_login_req
# @admin_auth
def auth_del(id=None, page=None):
	auth = Auth.query.get_or_404(id)
	db.session.delete(auth)
	db.session.commit()
	alluser = User.query.all()
	page_num = math.ceil(len(alluser) / 10)
	if page_num < page and page_num != 0:
		page = page_num
	flash('删除权限成功', 'ok')
	return redirect(url_for("admin.auth_list", page=page))

# 权限列表
@admin.route("/auth/list/<int:page>/",methods=["GET"])
@admin_login_req
# @admin_auth
def auth_list(page=None):
	if page is None:
		page = 1
	page_data = Auth.query.order_by(
		Auth.addtime.desc()
	).paginate(page=page, per_page=10) # per_page: 一页显示的条数
	return render_template("admin/auth_list.html", page_data=page_data)

# 管理员添加
@admin.route("/admin/add/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def admin_add():
	form = AdminForm()
	if form.validate_on_submit():
		data = form.data
		admin_count = Admin.query.filter_by(name=data['name']).count()
		if admin_count == 1:
			flash("名称已经存在", 'err')
			return redirect(url_for('admin.admin_add'))
		admin = Admin(
			name = data['name'],
			pwd = generate_password_hash(data['pwd']),
			role_id = data['role_id'],
			is_super = 1
		)
		db.session.add(admin)
		db.session.commit()
		flash("添加管理员成功", 'ok')
	return render_template("admin/admin_add.html", form=form)

# 管理员列表
@admin.route("/admin/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def admin_list(page=None):
	if page is None:
		page=1
	page_data = Admin.query.join(
			Role
		).filter(
			Role.id == Admin.role_id
		).order_by(
		Admin.addtime.desc()
	).paginate(page=page, per_page=5) # 一页显示5条
	return render_template("admin/admin_list.html", page_data=page_data)