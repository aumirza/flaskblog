from flask import render_template,url_for, flash , redirect ,request
from Myblog.main import main
from Myblog import db 
from Myblog.models import User , Post
from Myblog.main.forms import RegisterationForm , LoginForm
from flask_login import login_user , logout_user, current_user ,login_required


# @main.route('/<string:page>', defaults={'page': 'index'})
# def show(page):
#     try:
#         return render_template('main/%s.html' % page)
#     except TemplateNotFound:
#         abort(404)

@main.route("/")
@main.route("/home")
def home(): 
    posts = Post.query.all()
    return render_template("main/home.html",posts=posts)

@main.route("/<string:slug>")
def post(slug): 
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("main/post.html",post=post)

@main.route("/<int:post_id>")
def post_by_id(post_id):
    post = Post.query.get_or_404(post_id)
    return redirect(url_for('main.post',slug=post.slug))

@main.route("/contact")
def contact():
    return render_template("main/contact.html")

@main.route("/about")
def about():
    return render_template("main/about.html")

@main.route("/login", methods=['GET','Post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user , remember=form.remember.data)
            next_page = request.args.get('next')
            flash("login successful",'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash("login successful",'success')
    return render_template("/auth/login.html" , form=form)

@main.route("/register", methods=['GET','Post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully",'success')
        return redirect(url_for('main.login'))
    return render_template("/auth/register.html",form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))