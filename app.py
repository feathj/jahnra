from flask import Flask, render_template, request, response, current_app


app = Flask(__name__)
# with app.app_context():
    # current_app.jahnra = Jahnra()

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/check_user', methods=['POST'])
# def check_user():
    # img_buffer = request.files['webcam']
    # res = {}
    # detected_faces = app.recognizer.detect_faces(img_buffer)
    # res['detected_faces'] = detected_faces
    # return Response(json.dumps(res),  mimetype='application/json')

if __name__ == '__main__':
    app.run(
            host='0.0.0.0',
            debug=True
    )
