# Import
from flask import Flask, render_template,request, redirect
# Podłączenie biblioteki bazy danych
from flask_sqlalchemy import SQLAlchemy
from speech_recog import speech


app = Flask(__name__)
# Podłączanie SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Tworzenie bazy danych
db = SQLAlchemy(app)
# Tworzenie tabeli

class Card(db.Model):
    # Tworzenie kolumn
    # id
    id = db.Column(db.Integer, primary_key=True)
    #Tytuł
    title = db.Column(db.String(100), nullable=False)
    #Opis
    subtitle = db.Column(db.String(300), nullable=False)
    # Tekst
    text = db.Column(db.Text, nullable=False)

    # Wyprowadzanie obiektu i identyfikatora
    def __repr__(self):
        return f'<Card id={self.id}>'


#Zadanie #2. Utwórz tabelę użytkowników
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User id={self.id}>'


# Uruchamianie strony zawartości
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['login']
        form_password = request.form['password']
        
        # Zadanie #4. Wdrożyć autoryzację
        users = User.query.all()
        for user in users:
            if form_login == user.login:
                if form_password == user.password:
                    return redirect("/index")
                else:
                    error = "Niepoprawne hasło"
                    return render_template('login.html', error=error)

        error = "Nie ma użytkownika z takim loginem"
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        # Zadanie #3. Zadbaj o to, aby dane użytkownika zostały zapisane w bazie danych
        new_user = User(login=login, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    else:    
        return render_template('registration.html')


# Uruchamianie strony zawartości
@app.route('/index')
def index():
    # Wyświetlanie wpisów z bazy danych
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Uruchomienie strony z wpisem
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Uruchomienie strony tworzenia wpisu
@app.route('/create')
def create():
    return render_template('create_card.html')

# Formularz zgłoszeniowy
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        if request.form['action'] == 'create':
            title =  request.form['title']
            subtitle =  request.form['subtitle']
            text =  request.form['text']

            # Tworzenie obiektu, który zostanie wysłany do bazy danych
            card = Card(title=title, subtitle=subtitle, text=text)

            db.session.add(card)
            db.session.commit()
            return redirect('/index')
        else:
            recording = speech()
            return render_template('create_card.html', text=recording)
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
