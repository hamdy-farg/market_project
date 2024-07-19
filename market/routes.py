from market import app
from flask import  render_template, redirect, url_for, flash,request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm,SellItemForm
from market import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about/<user_name>')
def about_page(user_name):
    return f'<h1>{user_name}</h1>'

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    sell_form = SellItemForm()
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        #
        sell_item  = request.form.get("owned_item")
        purchase_item = request.form.get('purchase_item')
        #
        if purchase_item:
            p_item_object = Item.query.filter_by(name = purchase_item[:-1]).first()
            #
            print(p_item_object)
            if p_item_object:
                if current_user.can_purchase(p_item_object):
                    p_item_object.buy(current_user)
                    flash(f'Congratulations! You purchased {p_item_object} for {p_item_object.price}$',category='success')
                else :
                    flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}")
            return redirect(url_for('market_page'))
        else:
            if sell_item:
                p_item_object = Item.query.filter_by(name = sell_item).first()
                #
                if p_item_object:                
                    p_item_object.sell(current_user)
                    flash(f'Congratulations! You cell {p_item_object.name} for {p_item_object.price}$',category='success')
                   
                    return redirect(url_for('market_page'))
            return redirect(url_for('market_page'))
            #   
            #   
            #
    if request.method == "GET":   

        items = Item.query.filter_by(owner=None)
        owned_itemes = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_itemes, Sell_Item_Form=sell_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if(form.validate_on_submit()):
        db.session.rollback()
        user_to_create = User(
            user_name = form.user_name.data,
            email_address = form.email_address.data,
            password = form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        #
        flash(f'Account created successfully! You are now logged in as : {user_to_create.user_name}', category='success')
        
    #?
        return redirect(url_for('market_page'))
    if form.errors != {}: # if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user{err_msg}', category='danger')

    #?
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if(form.validate_on_submit()):
        print(f'{form.email_address.data} eeeeeeeeeeee')
        #
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        #
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
        #
            login_user(attempted_user)
        #
            flash('Success! Your are logged in as: {attempted_user.user_name}', category='success')
        #
            return redirect(url_for('market_page'))
        #
        else:
            flash('Email and password not match ! please try again', category='danger')

        #
    #     return redirect(url_for('market_page'))
    # if form.errors != {}:
    #     for err_msg in form.errors.values():
    #         flash(f'There was an error with creating a user{err_msg}', category='danger')
    return render_template('login.html',form=form)

@app.route('/logoute_page')
@app.route('/logoute')
def logoute_page():
    logout_user()
    flash('you have been logged out!',category='info')
    return redirect(url_for('home_page'))