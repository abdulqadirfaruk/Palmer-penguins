from flask import Flask, render_template, request, send_file, redirect, url_for
from database import Connect
import datetime
import pickle
import numpy

app = Flask(__name__)


connection = Connect.get_connection()
db = connection["penguins"]


svm = pickle.load(open('svm_model.pkl', 'rb'))
randomForest = pickle.load(open('rf_model.pkl', 'rb'))

header = open("results.txt", "w")
header.write("Bill_length; Bill_width; Flipper_length; Body_mass; Sex; Island; Prediction" + "\n")
header.close()
prediction_result = None
acc = ""
date = datetime.datetime.now()


@app.route('/')
def index():
    global prediction_result
    col = db["reviews"]
    reviews = col.find()
    return render_template('index.html', reviews=reviews)


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    global prediction_result, acc

    b_length = request.form['bl']
    b_width = request.form['bw']
    f_length = request.form['fl']
    b_mass = request.form['mass']
    sex = request.form['sex']
    island = request.form['island']
    model = request.form['model']

    features = numpy.array([[b_length, b_width, f_length, b_mass, sex, island]])

    if model == "0":
        prediction_result = svm.predict(features)
        acc = 98.5
    elif model == "1":
        prediction_result = randomForest.predict(features)
        acc = 95.5

    feature = features.tolist()

    if feature[0][4] == "0":
        feature[0][4] = "Male"
    elif feature[0][4] == "1":
        feature[0][4] = "Female"

    if feature[0][5] == "0":
        feature[0][5] = "Biscoe"
    elif feature[0][5] == "1":
        feature[0][5] = "Dream"
    elif feature[0][5] == "2":
        feature[0][5] = "Torgerson"

    value = prediction_result
    if value == 0:
        value = "Adelie"
    elif value == 1:
        value = "Gentoo"
    elif value == 2:
        value = "Chinstrap"

    output = numpy.append(feature, value)
    file = open("results.txt", "a")
    file.write(str(output) + "\n")
    file.close()
    return redirect(url_for('prediction'))


@app.route('/prediction', methods=['GET'])
def prediction():
    col = db["reviews"]
    reviews = col.find()
    return render_template('index.html', reviews=reviews, data=prediction_result, accuracy=acc)


@app.route('/export', methods=['POST', 'GET'])
def export():
    path = "results.txt"
    return send_file(path, as_attachment=True)


@app.route('/post', methods=['POST', 'GET'])
def post():
    name = request.form['name']
    comment = request.form['comment']
    time_stamp = date.strftime("%x %X %Z")

    col = db["reviews"]

    data = {"name": name, "comment": comment, "time_stamp": time_stamp}
    col.insert_one(data)
    return redirect(url_for('index'))


@app.route('/refresh', methods=['POST'])
def clear():
    if request.form['refresh'] == 'clear':
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
