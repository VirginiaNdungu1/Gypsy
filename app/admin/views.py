from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from . forms import BlogSectionForm
from .. import db
from app.models import Blogsection


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
