from . import db
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from .models import User
from .models import Patient_Details

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/new')
@login_required
def new_patient():
    return render_template('create_patient.html')

@main.route('/new', methods=['POST'])
@login_required
def new_patient_post():
    age = request.form.get('age')
    p_name = request.form.get('p_name')
    email1 = request.form.get('email1')

    detail = Patient_Details(age=age, p_name=p_name, email1=email1, author=current_user)
    db.session.add(detail)
    db.session.commit()

    flash('Patient Detail has been added!')

    return redirect(url_for('main.all_details'))

@main.route('/all')
@login_required
def all_details():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    details = user.details

    return render_template('all_details.html', details=details, user=user)

@main.route('/detail/<int:detail_id>/update', methods=['GET', 'POST'])
@login_required
def update_detail(detail_id):
    detail = Patient_Details.query.get_or_404(detail_id)
    if request.method == 'POST':
        detail.age = request.form['age']
        detail.p_name = request.form['p_name']
        detail.email1 = request.form['email1']
        db.session.commit()
        flash('your detail has been updated!!')

        return redirect(url_for('main.all_details'))
    return render_template('update_detail.html', detail=detail)

@main.route('/detail/<int:detail_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_detail(detail_id):
    detail = Patient_Details.query.get_or_404(detail_id)
    db.session.delete(detail)
    db.session.commit()
    return redirect(url_for('main.all_details'))