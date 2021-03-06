from flask import flash, render_template, abort
from flask_login import login_required, current_user

from .import main
from .. import db
from app.models import User, Blogsection


@main.route('/')
def index():
    '''
    render homepage template on the /route
    '''
    return render_template('index.html', title='Welcome to Gypsy Blogs')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', title='Dashboard')

# admin dashboard view


@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the admin dashboard
    if not current_user.is_admin:
        abort(403)
    title = "Gypsy admin dashboard"
    return render_template('main/admin_dashboard.html', title=title)


@main.route('/blogsections')
def display_blogsections():
    blogsections = Blogsection.get_blogsections()

    # title = 'Blog Sections'
    return render_template('main/blogsections.html', blogsections=blogsections)


@main.route('/blogsections/<int:id>')
def single_blogsection(id):
    blogsection = Blogsection.query.get(id)
    return render_template('main/blogsections.html', blogsection=blogsection)
