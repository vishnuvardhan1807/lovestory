from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle

# initialize a Flask app
app = Flask(__name__)

@app.route("/")
@cross_origin()
def index():
    return render_template('home.html')
    
# route to show predictions in web ui
@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def predict():
    if request.method == "POST":
        try:
            rate_marraige = float(request.form["rate_marraige"])
            age = float(request.form["age"])
            yrs_married = float(request.form["yrs_married"])
            children = float(request.form["children"])
            religious = float(request.form["religious"])
            educ = float(request.form["edu"])
            occupation = float(request.form["occupation"])

            # open and load the model and scaler
            model = 'model.pickle'
            scaler = 'scaler.pkl'

            loaded_model = pickle.load(open(model, 'rb'))
            loaded_scaler = pickle.load(open(scaler, 'rb'))
            
            # scale the inputs
            values = [[rate_marraige, age, yrs_married, children,
                       religious, educ, occupation]]
            values = loaded_scaler.transform(values)
            
            # make predictions
            prediction = loaded_model.predict(values)
            
            # show predictions in webpage
            return render_template('result.html', prediction=prediction[0])
        
        except Exception as e:
            print('The Exception message is:', e)
            return 'something is wrong'
        
    else:
        return render_template('index.html')
            
            

if __name__ == '__main__':
    app.run(debug=True)