from flask import render_template, request, redirect, url_for, flash, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get("logged_in"):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next = request.path))
    return check_permissions

@app.route("/")
def base():
    all_posts = Entry.query.filter_by(is_published = True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts = all_posts)

@app.route("/drafts/", methods = ["GET"])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published = False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts = drafts)

@app.route("/new_post/", methods = ["GET", "POST"])
@app.route("/edit_post/<int:entry_id>", methods = ["GET", "POST"])
@login_required
def create_or_edit_entry(entry_id = None):
    if entry_id:
        entry = Entry.query.filter_by(id = entry_id).first_or_404()
        form = EntryForm(obj = entry)
    else:
        entry = None
        form = EntryForm()
    errors = None
    if request.method == "POST":
        if form.validate_on_submit():
            if entry:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title = form.title.data,
                    body = form.body.data,
                    is_published = form.is_published.data
                )
                db.session.add(entry)
            db.session.commit()
            flash("Post saved.")
            return redirect(url_for('base'))
        else:
            errors = form.errors
    return render_template("entry_form.html", form = form, errors = errors)

@app.route("/delete_entry/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Post deleted")
    return redirect(url_for('base'))

@app.route("/login/", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == "POST":
        if form.validate_on_submit():
            session["logged_in"] = True
            session.permanent = True
            flash("You are logged in.")
            return redirect(next_url or url_for('base'))
        else:
            errors = form.errors
    return render_template("login_form.html", form = form, errors = errors)

@app.route("/logout/", methods = ["GET", "POST"])
def logout():
    if request.method == "POST":
        session.clear()
        flash("You are logged out.")
    return redirect(url_for('base'))
