from flask import Flask, render_template, session, redirect, request, url_for, abort
from cloudipsp import Api, Checkout
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate
import requests
import json
import telegram
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/lpage'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lisovakazka_user:4wRtMcCNFiCQH4lsZBuqIRkQGh3hqSDg@dpg-cgtjmtiut4mcfrm6h8p0-a/lisovakazkae"

#postgres://lisovakazka_user:4wRtMcCNFiCQH4lsZBuqIRkQGh3hqSDg@dpg-cgtjmtiut4mcfrm6h8p0-a/lisovakazkae
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lpage.db'
# print(os.environ.get('DATABASE_URL'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_secret_key'
bot_token = "6033946855:AAFWBgDFja05rhGs2kxCFJ1l282sGXBU708"
bot = telegram.Bot(token=bot_token)

db = SQLAlchemy(app)
# db.init_app(app)
migrate = Migrate(app, db)
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImI3N2ZiNWFhYWVjMmEyNWJjMjRiYjMxM2Y0ZDVjMjAxNjhjYzRjZGQxNTE3NmM5YmJmYTAyYmIzNDliN2MwMDJhYjM5NGZmZWVlNGRkNmMzIn0.eyJhdWQiOiIyY2RhZTNkZGIxNzk4MjRjZTZiNTQ0NWQxODk3OTI3YyIsImp0aSI6ImI3N2ZiNWFhYWVjMmEyNWJjMjRiYjMxM2Y0ZDVjMjAxNjhjYzRjZGQxNTE3NmM5YmJmYTAyYmIzNDliN2MwMDJhYjM5NGZmZWVlNGRkNmMzIiwiaWF0IjoxNjgxNDY2OTQ2LCJuYmYiOjE2ODE0NjY5NDYsImV4cCI6MTY4MTQ3MDU0Niwic3ViIjoiIiwic2NvcGVzIjpbXSwidXNlciI6eyJpZCI6ODI4MTU5MywiZ3JvdXBfaWQiOm51bGwsInBhcmVudF9pZCI6bnVsbCwiY29udGV4dCI6eyJhY2NsaW0iOiIwIn0sImFyZWEiOiJyZXN0In19.WEIpniqDFTm032lJ12cQ7YVoGaz7KhyO6IPkpsQbXdzDegMgKtYQZ0TvjpPy-9Y_asQ0x_3Un3yq10Nkf_8xp7ih4TM8TbYCMUgUzJkZBHcnQq89DmxeIhoaZyNzcRbk4Y1UzWYGLwrp91w2vCoWtdJZHfj5pD2OPR6FObj4f96qfhVrME0NleV4bW4kabbHmijhFjNEQtPcVp9FUISk-sjijW79mTpS3pyHIt1VGsY6rLL1J2PisIa5cK1wNoj9kjQN4fC58E1FG6TNE1vRIPsv_ne6nxUPYPj2cx9Rtx2Exp4l6hpCuvilUmP77njgszk6rdiBgujBIKfoFvEvrA'

url_sd = "https://first-lpage.salesdrive.me/handler/"
url_sp = "https://api.sendpulse.com/addressbooks/144824/emails"

payload = {
    "form": "Ebpo73kE4coi6C22nypJWXaJkpVncWoPCa_E08CjSbIdBS8yaPZ1WW9",
    "getResultData": "",
    "products": [
        {
            "id": "",
            "name": "",
            "costPerItem": "",
            "amount": "",
            "description": "",
            "discount": "",
            "sku": ""
        }
    ],
    "comment": "",
    "fName": "",
    "lName": "",
    "mName": "",
    "phone": "",
    "email": "",
    "con_comment": "",
    "shipping_method": "",
    "payment_method": "",
    "shipping_address": "",
    "novaposhta": {
        "ServiceType": "",
        "payer": "",
        "area": "",
        "region": "",
        "city": "",
        "cityNameFormat": "",
        "WarehouseNumber": "",
        "Street": "",
        "BuildingNumber": "",
        "Flat": ""
    },
    "ukrposhta": {
        "ServiceType": "",
        "payer": "",
        "type": "",
        "city": "",
        "WarehouseNumber": "",
        "Street": "",
        "BuildingNumber": "",
        "Flat": ""
    },
    "justin": {
        "WarehouseNumber": ""
    },
    "sajt": "",
    "organizationId": "",
    "shipping_costs": "",
    "prodex24source_full": "",
    "prodex24source": "",
    "prodex24medium": "",
    "prodex24campaign": "",
    "prodex24content": "",
    "prodex24term": "",
    "prodex24page": ""
}
async def send_telegram_message(text):
    chat_id = 334511336
    await bot.send_message(chat_id=chat_id, text=text)
def create_admin_user():
    admin_username = 'admin1'
    admin_password = generate_password_hash('1234')
    existing_user = Admin.query.filter_by(username=admin_username).first()
    if existing_user:
        return
    admin_user = Admin(
        username=admin_username,
        password=admin_password,
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return self.title

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(95), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.username}-{self.password}"

with app.app_context():
    create_admin_user()
    db.create_all()
@app.route('/', methods=['POST', 'GET'])
async def home():
# def home():

    item = Item.query.all()
    if request.method == 'POST':
        first_name = request.form['fName']
        email = request.form['email']
        comment = request.form['comment']


        form_data = request.form.to_dict()
        payload.update(form_data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url_sd, data=json.dumps(payload), headers=headers)
        # Виклик SendPulse API для створення контакту
        headers = {
            "Authorization": "Bearer {}".format(TOKEN),
            "Content-Type": "application/json",
        }
        data = {
            "emails": [
                {
                    "email": email,
                    "variables": {
                        "name": first_name
                    }
                }
            ]
        }
        response = requests.post(url_sp, headers=headers, json=data)
        text = f"Інформація з форми:\nІм'я: {first_name}\nEmail: {email}\nПовідомлення: {comment}"
        await send_telegram_message(text)
        # send_telegram_message(text)

    return render_template('index.html', items=item)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('current_user'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form.get('password')

        # Check if the user exists
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            # If the password is correct, store the user ID in the session
            session['current_user'] = admin.id

            # Check if the user is an admin
            if admin.is_admin:
                session['is_admin'] = True
            else:
                session['is_admin'] = False

            return redirect(url_for('home'))
        else:
            return "Wrong email or password. Please try again."

    return render_template('login.html')


@app.route('/logout')
def logout():
    if not session.get('is_admin'):
        return 'Access denied'
    # Видаляємо сеансову змінну `current_user`
    session.pop('current_user', None)
    # Видаляємо сеансову змінну `is_admin`
    session.pop('is_admin', None)
    return redirect(url_for('home'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('is_admin'):
        abort(404)
    if request.method == 'POST':
        title = request.form['title']
        price = int(request.form['price'])

        item = Item(title=title, price=price)

        # Додаємо товар до бази даних
        try:
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'Помилка'
    # Перенаправляємо користувача на сторінку "/home"
    else:
        return render_template('create.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')

    # return render_template('index.html')
    return redirect(url)
if __name__ == '__main__':

    app.run(debug=True)
