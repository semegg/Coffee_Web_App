import os

from flask import Flask, render_template, redirect, request, send_file
from flask_login import login_required

from auth import login_manager, login, logout
from models import db, Tables, Admin, add_product_to_database, save_uploaded_image, export_successful_purchases_to_csv

app = Flask(__name__)
app.secret_key = '77656220636F6666656520617070'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../menu.db'

login_manager.init_app(app)
db.init_app(app)


# Default users part ↓
@app.route('/')
def index():
    categories = Tables.categories
    return render_template('user_templates/index.html', categories=categories)


@app.route('/menu/<item>')
def menu_show(item):
    table = Tables.table_classes[item]
    data = db.session.query(table).all()
    return render_template('user_templates/menu.html', data=data)


# Admin part ↓


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            return redirect('/admin')
    return render_template('admin_templates/login.html')


@app.route('/logout')
@login_required
def logout_route():
    logout()
    return redirect('/login')


@app.route('/admin/')
@login_required
def main_panel_route():
    return render_template('admin_templates/main_panel.html')


@app.route('/admin/admin_list')
@login_required
def admins_route():
    data = db.session.query(Admin).all()
    return render_template('admin_templates/admins.html', data=data)


@app.route('/admin/admin_list/delete/<username>')
@login_required
def delete_admin_route(username):
    admin = Admin.query.filter_by(username=username).first()
    db.session.delete(admin)
    db.session.commit()
    return redirect('/admin/admin_list')


@app.route('/admin/admin_list/add', methods=['POST', 'GET'])
def add_admin_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Admin.register_admin(username, password)
        return redirect('/admin/admin_list')
    return render_template('admin_templates/add_admin.html')


@app.route('/admin/edit_menu', methods=['GET'])
@login_required
def edit_categories_route():
    return render_template('admin_templates/edit_categories.html')


@app.route('/admin/edit_menu/<category>', methods=['GET'])
@login_required
def edit_menu_route(category):
    table = Tables.table_classes.get(category)
    data = db.session.query(table).all()
    return render_template('admin_templates/edit_menu.html', category=category, items=data)


@app.route('/admin/edit_menu/<category>/add', methods=['GET', 'POST'])
@login_required
def add_product_route(category):
    table = Tables.table_classes.get(category)

    if request.method == 'POST':
        uploaded_file = request.files['image']

        if uploaded_file.filename == '':
            return '<h1>Add a photo, please</h1>'

        id = f'{category}_{request.form["id"]}'
        name = request.form['name']
        price = request.form['price']

        add_product_to_database(table, id, name, price)
        save_uploaded_image(uploaded_file, id)

        return redirect(f'/admin/edit_menu/{category}')

    return render_template('admin_templates/add_product.html', category=category)


@app.route('/admin/edit_menu/<category>/<product>', methods=['GET', 'POST'])
@login_required
def edit_product(category, product):
    table = Tables.table_classes.get(category)
    product = db.session.get(table, product)
    if request.method == 'POST':

        if 'action' in request.form:
            if request.form['action'] == 'save':
                product.name = request.form['name']
                product.price = request.form['price']
                db.session.commit()

                if 'image' in request.files:
                    uploaded_file = request.files['image']
                    if uploaded_file.filename != '':
                        save_uploaded_image(uploaded_file, product.id)

            elif request.form['action'] == 'delete':
                db.session.delete(product)
                db.session.commit()

        return redirect(f'/admin/edit_menu/{category}')
    return render_template('admin_templates/edit_product.html', product=product)


@app.route('/admin/sales/')
@login_required
def sales_history_route():
    return render_template('admin_templates/sales.html')


@app.route('/admin/sales/<period>')
@login_required
def get_csv_sales_history_route(period):
    file = export_successful_purchases_to_csv(period)
    try:
        return send_file(file, as_attachment=True)
    finally:
        if os.path.exists(file):
            os.remove(file)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
