from flask import Flask, render_template, request, Response, current_app
from jahnra import Jahnra
from json import dumps


app = Flask(__name__)
with app.app_context():
    current_app.jahnra = Jahnra('./db.csv', False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict_genre', methods=['POST'])
def guess_genre():
    lyrics = request.json['lyrics']
    prediction = app.jahnra.predict('ri', lyrics)

    res = {}
    res['prediction'] = prediction
    # TODO other stuffs about prediction here
    return Response(dumps(res), mimetype='application/json')

if __name__ == '__main__':
    app.run(
            host='0.0.0.0',
            debug=True
    )
