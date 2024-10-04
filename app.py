from flask import Flask, request, jsonify, render_template_string
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

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Complete a História</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; }
            h1 { color: #333; text-align: center; }
            #story { margin: 20px 0; font-size: 1.5em; color: #555; text-align: center; }
            textarea { width: 100%; height: 100px; padding: 10px; border: 2px solid #007bff; border-radius: 5px; resize: none; font-size: 16px; }
            button { background-color: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 10px; display: block; width: 100%; transition: background-color 0.3s ease; }
            button:hover { background-color: #0056b3; }
            #commentsSection { margin-top: 20px; }
            #commentsList { list-style-type: none; padding: 0; }
            #commentsList li { background: white; margin: 10px 0; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
        </style>
    </head>
    <body>
        <h1>Complete a História</h1>
        <p id="story">Era uma vez um médico chamado Dr. Simão Bacamarte...</p>
        <textarea id="comment" placeholder="Escreva seu nome e sua versão da historia aqui..."></textarea>
        <button id="submitComment">Enviar Comentário</button>
        
        <div id="commentsSection">
            <h2>Comentários</h2>
            <ul id="commentsList"></ul>
        </div>

        <script>
            function fetchComments() {
                fetch('/comments')
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(comment => addCommentToList(comment.comment));
                    })
                    .catch(error => {
                        console.error('Erro ao buscar comentários:', error);
                    });
            }

            document.getElementById('submitComment').addEventListener('click', function() {
                const comment = document.getElementById('comment').value;
                if (comment) {
                    fetch('/comments', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ comment })
                    })
                    .then(response => response.json())
                    .then(data => {
                        addCommentToList(data.comment);
                        document.getElementById('comment').value = ''; // Limpa o campo
                    })
                    .catch(error => {
                        console.error('Erro ao enviar o comentário:', error);
                    });
                } else {
                    alert("Por favor, escreva um comentário antes de enviar.");
                }
            });

            function addCommentToList(comment) {
                const commentsList = document.getElementById('commentsList');
                const li = document.createElement('li');
                li.textContent = comment;
                commentsList.appendChild(li);
            }

            // Carrega os comentários ao iniciar a página
            fetchComments();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

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
    app.run(debug=True)
