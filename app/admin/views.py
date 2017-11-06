from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from . forms import BlogSectionForm, BlogPostForm, BlogpostAssignForm, CommentForm
from .. import db
from app.models import Blogsection, Post, Comment


def check_admin():
    '''
    function that prevents non admins from accessing admin dashboard
    '''
    if not current_user.is_admin:
        abort(403)

#  Blog Section Views


@admin.route('/blogsections/create', methods=['GET', 'POST'])
@login_required
def create_blogsection():
    '''
    add blog section to db
    '''
    check_admin()

    create_blogsection = True

    form = BlogSectionForm()

    if form.validate_on_submit():
        blogsection = Blogsection(name=form.name.data)

        try:
            # create new blog section
            blogsection.save_blogsection()
            flash('You have successdully created a new blog section')
        except:
            # avoid redundancy
            flash('Error: blog section already exists')
        return redirect(url_for('admin.view_blogsections'))
    # load blog section template
    title = 'New Blog Section'
    return render_template('admin/blogsections/new_blogsection.html', action="Add", create_blogsection=create_blogsection, form=form, title=title)


@admin.route('/blogsections', methods=['GET', 'POST'])
@login_required
def view_blogsections():
    '''
    View all blog sections
    '''
    check_admin()

    blogsections = Blogsection.get_blogsections()

    title = 'Blog Sections'
    return render_template('admin/blogsections/blogsections.html', blogsections=blogsections, title=title)


@admin.route('/blogsections/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blogsection(id):
    '''
    Edit blog section
    '''
    check_admin()

    create_blogsection = False

    blogsection = Blogsection.query.get(id)
    form = BlogSectionForm(obj=Blogsection)
    if form.validate_on_submit():
        blogsection.name = form.name.data
        db.session.commit()
        flash('Success Blog Section Edit')

        return redirect(url_for('admin.view_blogsections'))

    form.name.data = blogsection.name
    title = 'Edit Blog Section'
    return render_template('admin/blogsections/new_blogsection.html', action='Edit', create_blogsection=create_blogsection, form=form, blogsection=blogsection, title=title)


@admin.route('/blogsections/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blogsection(id):
    '''
    Delete blog section
    '''
    check_admin()

    blogsection = Blogsection.query.get(id)
    db.session.delete(blogsection)
    db.session.commit()
    flash('You have successully deleted blog section')

    return redirect(url_for('admin.view_blogsections'))
    title = "Delete blog section"
    return render_template(title=title)


@admin.route('/blogposts/create', methods=['GET', 'POST'])
@login_required
def create_blogpost():
    '''
    add blog section to db
    '''
    check_admin()

    create_blogpost = True
    # blogsection = Blogsection.query.filter_by(id=id).first()
    form = BlogPostForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        blogpost = Post(title=title,
                        description=description,
                        user=current_user)

        blogpost.save_blogpost()
        flash('You have successfully created a new blog post')

        return redirect(url_for('admin.view_blogposts'))
    # load blog section template
    title = 'New Blog Post'
    return render_template('admin/blogposts/new_blogpost.html', action="Add", create_blogpost=create_blogpost, form=form, title=title)


@admin.route('/blogposts')
@login_required
def view_blogposts():
    '''
    list all blog posts
    '''
    check_admin()

    blogposts = Post.query.all()
    title = "Blog Posts"
    return render_template('admin/blogposts/blogposts.html', blogposts=blogposts, title=title)


@admin.route('/blogposts/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_blogpost(id):
    check_admin()

    blogpost = Post.query.get(id)

    form = BlogpostAssignForm(obj=Post)

    if form.validate_on_submit():
        blogpost.blogsection = form.blogsection.data
        db.session.add(blogpost)
        db.session.commit()
        flash('Successfully assigned blog sections')

        return redirect(url_for('admin.view_blogposts'))
    title = "Assign Blog Post"
    return render_template('admin/blogposts/assign_blogpost.html', blogpost=blogpost, form=form, title=title)


@admin.route('/blogposts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blogposts(id):
    '''
    edit blog posts
    '''
    check_admin()

    create_blogpost = False
    blogpost = Post.query.get(id)
    form = BlogPostForm(obj=Post)
    if form.validate_on_submit():
        blogpost.title = form.title.data
        blogpost.description = form.description.data
        db.session.commit()
        flash('Successfull Blog Post Edit')
        return redirect(url_for('admin.view_blogposts'))

    form.title.data = blogpost.title
    form.description.data = blogpost.description
    title = "Edit Blog Post"
    return render_template('admin/blogposts/new_blogpost.html', action='Edit', create_blogpost=create_blogpost, blogpost=blogpost, form=form, title=title)


@admin.route('blogposts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blogpost(id):
    check_admin()

    blogpost = Post.query.get(id)
    db.session.delete(blogpost)
    db.session.commit()
    flash('You have successully deleted blog post')

    return redirect(url_for('admin.view_blogposts'))
    title = "Delete blog post"
    return render_template(title=title)


@admin.route('/blogcomments/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create_comment(id):
    '''
    add blog section to db
    '''
    check_admin()

    create_comment = True
    # blogsection = Blogsection.query.filter_by(id=id).first()
    form = CommentForm()

    post = Post.query.get(id)

    if form.validate_on_submit():
        description = form.description.data

        comment = Comment(description=description, post_id=post.id,
                          user=current_user)

        comment.save_comment()
        flash('You have successfully created a new blog post')

        return redirect(url_for('admin.view_comments', post=post, comment=comment))
    # load blog section template
    title = 'New Blog Post'
    return render_template('admin/blogcomments/new_blogcomment.html', create_comment=create_comment,  post=post, form=form, title=title)


@admin.route('/blogcomments', methods=['GET', 'POST'])
@login_required
def view_comments():
    '''
    list all comments
    '''
    check_admin()
    comments = Comment.query.all()
    title = "Blog Comments"
    return render_template('admin/blogcomments/blogcomments.html', comments=comments, title=title)


@admin.route('/blogcomments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    '''
    edit blog comments
    '''
    check_admin()

    create_comment = False
    comment = Comment.query.get(id)
    form = CommentForm(obj=Comment)
    if form.validate_on_submit():
        comment.description = form.description.data
        db.session.commit()
        flash('Successfull Blog Comment Edit')
        return redirect(url_for('admin.view_comments'))

    form.description.data = comment.description
    title = "Edit Blog Comment"
    return render_template('admin/blogcomments/new_blogcomment.html', action='Edit', create_comment=create_comment, comment=comment, form=form, title=title)


@admin.route('blogcomments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    check_admin()

    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    flash('You have successully deleted blog comment')

    return redirect(url_for('admin.view_comments'))
    title = "Delete blog comment"
    return render_template(title=title)
