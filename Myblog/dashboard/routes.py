from flask import render_template,url_for, flash , redirect ,request
from Myblog.dashboard import dashboard
from Myblog.dashboard.forms import PostForm
from Myblog.models import Post
from Myblog import db
from flask_login import login_user , logout_user, current_user ,login_required


@dashboard.before_request
def restrict_dashboard_to_admins():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

@dashboard.route("/")
def index():
    return render_template("dashboard/index.html")


@dashboard.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("dashboard/posts.html",posts=posts)

@dashboard.route("/new-post/",methods=['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,slug=form.slug.data,content=form.content.data,catogary=form.catogary.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post have been saved ','success')
        return redirect(url_for('dashboard.edit_post', post_id=post.id))
    return render_template("dashboard/post-editor.html", form=form)

@dashboard.route("/edit-post/<int:post_id>",methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data,slug=form.slug.data,content=form.content.data,catogary=form.catogary.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post have been edited','success')
        return redirect(url_for('dashboard.edit_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.slug.data = post.slug
        form.catogary.data = post.catogary
        form.content.data = post.content

    return render_template("dashboard/post-editor.html", form=form)

@dashboard.route("/delete-post/<int:post_id>",methods=['GET','DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return render_template(redirect(url_for('dashboard.posts')))