from flask import render_template, request, redirect, url_for, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route('/')
def base():
    all_posts = Entry.query.filter_by(is_published = True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts = all_posts)

@app.route("/new_post/", methods = ["GET", "POST"])
@app.route("/edit_post/<int:entry_id>", methods = ["GET", "POST"])
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
            flash("Post saved !")
            return redirect(url_for('base'))
        else:
            errors = form.errors
    return render_template("entry_form.html", form = form, errors = errors)
