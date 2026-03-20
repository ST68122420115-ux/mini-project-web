from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv
load_dotenv()

from models import db, User, Character
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"             
login_manager.login_message = "Please log in first"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    for i, u in enumerate(users, start=1):
        u.id_temp = i
    return render_template('users.html', users=users)


@app.route('/edit_user/<int:id>', methods=['GET','POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.uid = request.form['uid']
        user.server = request.form['server']
        db.session.commit()
        flash("User updated successfully", "success")
        return redirect('/users')
    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("You have deleted your account", "success")
        return redirect(url_for('home'))
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully", "success")
    return redirect('/users')


@app.route('/dashboard')
@login_required
def dashboard():
    q = request.args.get('q')
    if q:
        characters = Character.query.filter(Character.name.contains(q)).all()
    else:
        characters = Character.query.all()
    return render_template('dashboard.html', characters=characters)


@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        char = Character(
            name=request.form['name'],
            element=request.form['element'],
            level=request.form['level'],
            constellation=request.form['constellation'],
            region=request.form['region'],
            img=request.form['img']
        )
        db.session.add(char)
        db.session.commit()
        flash("Character added successfully", "success")
        return redirect('/dashboard')
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    char = Character.query.get_or_404(id)
    if request.method == 'POST':
        char.name = request.form['name']
        char.element = request.form['element']
        char.level = request.form['level']
        char.constellation = request.form['constellation']
        char.region = request.form['region']
        char.img = request.form['img']
        db.session.commit()
        flash("Character updated successfully", "success")
        return redirect('/dashboard')
    return render_template('edit.html', char=char)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    char = Character.query.get_or_404(id)
    db.session.delete(char)
    db.session.commit()
    flash("Character deleted successfully", "success")
    return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            return render_template('login.html', error="Account not found")
        if user.password != request.form['password']:
            return render_template('login.html', error="The password is incorrect")
        login_user(user)
        flash("Logged in successfully", "success")
        return redirect(url_for('home'))  
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="Username already exists!")
        user = User(
            username=username,
            password=request.form['password'],
            uid=request.form['uid'],
            server=request.form['server']
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please login.", "success")
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('home')) 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)