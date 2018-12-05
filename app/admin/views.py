from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
from functools import wraps
from app import db
import math


# 用于检查用户是否登录的装饰器
def admin_login_req(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if "admin" not in session:
			return redirect(url_for("admin.login", next=request.url))
		return func(*args, **kwargs)
	return decorated_function

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
		print('haha:', data["pwd"])
		if not admin.check_pwd(data["pwd"]):
			flash("密码错误!")
			return redirect(url_for("admin.login"))
		# 将账户账号存入session
		session["admin"] = data["account"]
		return redirect(request.args.get("next") or url_for("admin.index"))
	return render_template("admin/login.html",form=form)


@admin.route("/logout/")
@admin_login_req
def logout():
	# 删除session中的账户信息
	session.pop("admin", None)
	return redirect(url_for("admin.login"))

@admin.route("/pwd/")
@admin_login_req
def pwd():
	return render_template("admin/pwd.html")

# 添加标签
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_req
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
		flash("添加成功", "ok")
		redirect(url_for('admin.tag_add'))
	return render_template("admin/tag_add.html", form=form)

# 标签删除
@admin.route("/tag/del/<int:id>/<int:page>/", methods=["GET"])
@admin_login_req
def tag_del(id=None, page=None):
	# 通过标签id查询出需要删除的标签字段, first_or_404: 查询到无条目时会返回一个404错误, 而不是返回None
	tag = Tag.query.filter_by(id=id).first_or_404()
	# 删除标签并提交
	db.session.delete(tag)
	db.session.commit()
	# 查询出所有标签的总数
	count = Tag.query.all()
	# 向上取整, 如果总共有三个标签, 则页码数应为2
	page_num = math.ceil(len(count)/ 2)
	# 如果当前的页码数大于删除之后的标签总数, 则跳转到删除之后的最大页码数
	if page_num < page and page_num != 0:
		page = page_num
	flash("删除成功", "ok")
	# 重定向到tag_list页面, 并传入当前页码数
	return redirect(url_for('admin.tag_list', page=page))

# 标签列表
@admin.route("/tag/list/<int:page>/", methods=['GET'])
@admin_login_req
def tag_list(page=None):
	if page is None:
		page = 1
	page_data = Tag.query.order_by(
		Tag.addtime.desc()
	).paginate(page=page, per_page=2) # per_page: 一页显示的条数
	return render_template("admin/tag_list.html", page_data=page_data)

@admin.route("/movie/add/")
@admin_login_req
def movie_add():
	return render_template("admin/movie_add.html")

@admin.route("/movie/list/")
@admin_login_req
def movie_list():
	return render_template("admin/movie_list.html")

@admin.route("/preview/add/")
@admin_login_req
def preview_add():
	return render_template("admin/preview_add.html")

@admin.route("/preview/list/")
@admin_login_req
def preview_list():
	return render_template("admin/preview_list.html")

@admin.route("/user/list/")
@admin_login_req
def user_list():
	return render_template("admin/user_list.html")

@admin.route("/user/view/")
@admin_login_req
def user_view():
	return render_template("admin/user_view.html")

@admin.route("/comment/list/")
@admin_login_req
def comment_list():
	return render_template("admin/comment_list.html")

@admin.route("/moviecol/list/")
@admin_login_req
def moviecol_list():
	return render_template("admin/moviecol_list.html")

@admin.route("/oplog/list/")
@admin_login_req
def oplog_list():
	return render_template("admin/oplog_list.html")

@admin.route("/adminloginlog/list/")
@admin_login_req
def adminloginlog_list():
	return render_template("admin/adminloginlog_list.html")

@admin.route("/userloginlog/list/")
@admin_login_req
def userloginlog_list():
	return render_template("admin/userloginlog_list.html")

@admin.route("/role/add/")
@admin_login_req
def role_add():
	return render_template("admin/role_add.html")

@admin.route("/role/list/")
@admin_login_req
def role_list():
	return render_template("admin/role_list.html")

@admin.route("/auth/add/")
@admin_login_req
def auth_add():
	return render_template("admin/auth_add.html")

@admin.route("/auth/list/")
@admin_login_req
def auth_list():
	return render_template("admin/auth_list.html")

@admin.route("/admin/add/")
@admin_login_req
def admin_add():
	return render_template("admin/admin_add.html")

@admin.route("/admin/list/")
@admin_login_req
def admin_list():
	return render_template("admin/admin_list.html")