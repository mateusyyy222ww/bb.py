from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        data = request.json
        new_comment = Comment(comment=data['comment'])
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'comment': new_comment.comment}), 201
    
    comments = Comment.query.all()
    return jsonify([{'comment': c.comment} for c in comments])

if __name__ == '__main__':
    create_tables()  # Chama a função de criação de tabelas antes de rodar o servidor
    app.run(host='0.0.0.0', port=5000)  # Adiciona o host e a porta
