import fileinput

from flask import render_template, url_for, redirect, flash,request,session
from flask_bootstrap import Bootstrap4
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user
import pandas as pd

import os

from forms import *
from models import *

#UPLOAD_FOLDER =
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.'in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

bootstrap = Bootstrap4(app)
csrf = CSRFProtect(app)



@app.route('/')
# @app.route('')
def index():
    pizzas = Pizza.query.order_by(Pizza.name.desc()).all()

    return render_template('user/index.html',pizzas=pizzas)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = User_RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, register successed!')
        return redirect((url_for('user_login')))
    return render_template('user/user_register.html', form=form)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = User_LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        flash('User not exists or password not match!', 'err')
    return render_template('user/user_login.html', form=form)

@app.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/cart_add/<int:pizza_id>')
@login_required
def cart_add(pizza_id):

    cart= Cart.query.filter_by(pizza_id=pizza_id,user_id=current_user.id ).first()
    if cart:

        cart.number =cart.number+1

        #cart.update({'number': addnumber})
        #Pizza.query.filter(Pizza.id == cart.pizza_id).update({'sold': Pizza.sold + cart.number})
        db.session.commit()
    else:

        cart_new = Cart(pizza_id=pizza_id, number =1, user_id = current_user.id)
        db.session.add(cart_new)
        db.session.commit()
    return  redirect(url_for('shopping_cart'))

@app.route('/shopping_cart')
@login_required
def shopping_cart():
    user_id = current_user.id
    # page = request.args.get('page', 1, type=int)
    # pagination = Cart.query.filter_by(user_id=user_id).order_by(Cart.addtime.desc()).paginate(page=page, per_page=10)
    # carts = pagination.items
    carts = Cart.query.filter_by(user_id = user_id).order_by(Cart.addtime.desc()).all()

    if not carts:
        return redirect(url_for('empty_cart'))

    return render_template('user/shopping_cart.html', carts=carts)  # , titles=titles, Model=Cart, data=data)
    # data =[]
    # for msg in carts:
    #     data.append({'picture':msg.pizza.picture, 'name': msg.pizza.name,'number':msg.number,'price': msg.pizza.price,
    #     'total_price':msg.pizza.price*msg.number})
    # titles = [ ('picture', 'Picture'), ('name', 'Name'), ('number', 'Number'), ('price', 'Unit price'),('total_price','Total price')]

@app.route('/empty_cart')
@login_required
def empty_cart():
    return render_template('user/empty_cart.html')

@app.route('/new_cart')
@login_required
def new_cart():
    return redirect(url_for('index'))

'''@app.route('/shopping_cart/<int:pizza_id>/delete', methods=['POST'])
def delete_cart(card_id):
    cart = Cart.query.get(card_id)
    if cart:
        db.session.delete(cart)
        db.session.commit()
        return flash('The items has been deleted!','info')
    return redirect(url_for('shopping_cart'))'''

'''    user_id = current_user.id
    cart = Cart.query.filter_by(user_id=int(user_id)).order_by(Cart.addtime.desc()).all()
    if cart:
        return  render_template('user/shopping_cart.html',cart = cart)
    else:
        return  render_template('user/empty_cart')
'''
@app.route('/check_out', methods=['GET', 'POST'])
@login_required
def check_out():
    form = User_PayForm()
    if form.validate_on_submit():
        ###add order
        user_id = current_user.id
        receive_name = form.firstname.data+' ' +form.lastname.data
        receive_address = form.address.data+','+form.city.data+' '+form.zip.data
        receive_tel = form.phone.data
        order_status= 'Placed'
        order = Orders(user_id=user_id,receive_tel=receive_tel,receive_address=receive_address,receive_name=receive_name,
                       order_status=order_status)
        db.session.add(order)
        db.session.commit()


        ####add order detail
        carts = Cart.query.filter_by(user_id=user_id ).all()
        object=[]
        for cart in carts:
            object.append(
                OrdersDetail(order_id=order.id,pizzas_id = cart.pizza_id,number = cart.number) )
            db.session.add_all(object)
            db.session.commit()
            #pizza= Pizza.query.filter_by(id=cart.pizza_id).all().first()
           # pizza.inventory=pizza.inventory-cart.number
            Pizza.query.filter(Pizza.id==cart.pizza_id).update({'inventory': Pizza.inventory - cart.number})
            Pizza.query.filter(Pizza.id==cart.pizza_id).update({'sold':Pizza.sold+cart.number})
            db.session.commit()
           # OrdersDetail.query.join(Orders).filter(Orders.user_id == user_id).order_by(Orders.addtime.desc()).all()

       # pizza = OrdersDetail.query.join(Pizza).filter(Pizza.id ==)

            Cart.query.filter_by(user_id=user_id).update({'user_id':0})
            db.session.commit()

        return redirect((url_for('order_done')))

    return render_template('/user/check_out.html',form=form)

@app.route("/clear_cart/")
@login_required
def clear_cart():
    user_id = current_user.id
    Cart.query.filter_by(user_id=user_id).update({'user_id': 0})
    db.session.commit()
    return redirect(url_for('shopping_cart'))

@app.route("/delete_cart/")
@login_required
def delete_cart():
    cart_id = request.args.get('cartid')

    cart = Cart.query.filter_by(id=cart_id).first()

    if cart:
        db.session.delete(cart)
        db.session.commit()
    return redirect(url_for('shopping_cart'))

@app.route('/order_done')
@login_required
def order_done():
    return render_template('/user/order_done.html')

@app.route('/order_list',methods=['GET', 'POST'])
@login_required
def order_list():
    user_id = current_user.id
    orders = OrdersDetail.query.join(Orders).filter(Orders.user_id==user_id).order_by(Orders.addtime.desc()).all()
    return render_template('user/order_list.html',orders=orders)


'''================================================='''


@app.route('/admin_login',methods=['GET', 'POST'])
def admin_login():
    form = Admin_LoginForm()
    if form.validate_on_submit():
        admin_id =1
        manager = form.manager.data
        password = form.password.data
        #admin= Admin.query.filer_by(manger=manager)
        if manager =='admin' and password =='123':
       # if admin  and password==admin.password:
            session["admin"] = manager
            session["admin_id"] = admin_id
            return redirect(url_for('admin_index'))
    return render_template('admin/admin_login.html', form=form)

@app.route('/admin_logout')
def admin_logout():

    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("index"))

@app.route('/admin_orderlist',methods=['GET', 'POST'])
def admin_orderlist():
    orders = Orders.query.order_by(Orders.addtime.desc()).all()
    #orders = OrdersDetail.query.join(Orders).filter(Orders.user_id == user_id).order_by(Orders.addtime.desc()).all()
    return  render_template('admin/admin_order_list.html',orders=orders)

@app.route('/admin_pizzalist',methods=['GET', 'POST'])
def admin_pizzalist():
    pizzas = Pizza.query.order_by(Pizza.addtime.desc()).all()
    return render_template('admin/admin_pizzalist.html',pizzas=pizzas)

@app.route('/admin_delete_pizza/',methods=['GET'])
def admin_delete_pizza():
    pizza_id = request.args.get('pizzaid')
    pizza = Pizza.query.filter_by(id = pizza_id).first()
    if pizza:
        db.session.delete(pizza)
        db.session.commit()
        #return redirect(url_for('admin_pizzalist'))
    return redirect(url_for('admin_pizzalist'))

@app.route('/admin_edit_pizza/',methods=['GET','POST'])
def admin_edit_pizza():
    form = Action_PizzaForm()
    pizza_id = request.args.get('pizzaid')
    pizza = Pizza.query.filter_by(id = pizza_id).first()
    if pizza:
        original_pf = pizza.picture
        if request.method=='GET':

            form.pizzaname.data = pizza.name
            form.pizzaprice.data = pizza.price
            form.pizzasize.data = pizza.size
            form.pizzatoppings.data = pizza.toppings
            form.pizzainventory.data = pizza.inventory
        elif form.validate_on_submit():
            pf = form.pizzapicture.data
            if pf and  allowed_file(pf.filename):
                pizza.picture = pf
                filename = secure_filename(pf.filename)
                pf.save(os.path.join('static','images',filename))
            else:
                pizza.picture = original_pf
            pizza.name = form.pizzaname.data
            pizza.price = form.pizzaprice.data
            pizza.size = form.pizzasize.data
            pizza.toppings = form.pizzatoppings.data
            pizza.inventory = form.pizzainventory.data
            db.session.add(pizza)
            db.session.commit()
            return redirect(url_for('admin_pizzalist'))
    return render_template('admin/admin_edit_pizza.html',form=form)

@app.route('/admin_add_pizza/',methods=['GET','POST'])
def admin_add_pizza():
    form= Action_PizzaForm()
    if form.validate_on_submit():
        pf = form.pizzapicture.data
        if pf and allowed_file(pf.filename):
            filename = secure_filename(pf.filename)
            pf.save(os.path.join('static', 'images', filename))
            picture = '/static/images/'+ filename
            name = form.pizzaname.data
            price = form.pizzaprice.data
            size = form.pizzasize.data
            toppings = form.pizzatoppings.data
            inventory = form.pizzainventory.data
            pizza = Pizza(name=name,price=price,picture=picture,size=size,toppings=toppings,inventory=inventory)
            db.session.add(pizza)
            db.session.commit()
            return redirect(url_for('admin_pizzalist'))
    return render_template('admin/admin_add_pizza.html', form=form)

@app.route('/admin_change_orderstatus')
def admin_change_orderstatus():
    order_id = request.args.get('order_id')
    orderstatus = request.args.get('orderstatus')
    order = Orders.query.filter_by(id =order_id).first()
    if order:
        order.order_status = orderstatus
        db.session.commit()
    return redirect(url_for('admin_orderlist'))

@app.route('/admin_orderdetail',methods=['GET'])
def admin_order_detail():
    order_id = request.args.get('order_id')
    order_details = OrdersDetail.query.join(Orders).filter(OrdersDetail.order_id==order_id)
    return  render_template('admin/admin_order_detail.html',order_details=order_details,)

@app.route('/admin_userlist',methods=['GET'])
def admin_userlist():
    pass

@app.route('/admin_index')
def admin_index():
    return render_template('admin/admin_index.html')




if __name__ == '__main__':
    df = pd.read_csv('pizzeria.csv')

    with app.app_context():
        if not os.path.exists('app.db'):
            db.create_all()
            for index, row in df.iterrows():
                pizza_data = Pizza(name=row['Name'], price=row['Price'], size=row['Size'], \
                             toppings=row['Toppings'],picture='/static/images/'+row['Name']+'.jpeg')
                db.session.add(pizza_data)
                db.session.commit()

    app.run(debug=True, host='127.0.0.1', port=3000)
