from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)


def generate_short_url(num_chars=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(num_chars))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        # ✅ Verify URL correctness
        if not original_url.startswith(('http://', 'https://')):
            return "Invalid URL. Please include http:// or https://"
        
        short_url = generate_short_url()
        new_entry = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_entry)
        db.session.commit()
        return render_template('home.html', short_url=short_url)
    return render_template('home.html')


@app.route('/<short_url>')
def redirect_url(short_url):
    entry = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(entry.original_url)


@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)

with app.app_context(): 
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)


