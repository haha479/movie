from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
from functools import wraps
from app import db

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
			print('密码错误aaaa')
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
	
	return render_template("admin/tag_add.html", form=form)

@admin.route("/tag/list/")
@admin_login_req
def tag_list():
	return render_template("admin/tag_list.html")

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