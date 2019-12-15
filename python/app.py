from flask import Flask, render_template, request
from sklearn.externals import joblib

app = Flask(__name__, template_folder='../templates', static_folder='../static')


input_transformer = joblib.load(open('../static/models/input_transformer.pkl', 'rb'))
model = joblib.load(open('../static/models/review_sentiment.pkl', 'rb'))
model_input=""
model_output=""


@app.route('/')
def home():
    return render_template('index.html', image_filename="img/happy.webp", display_mode="none")

@app.route('/predict', methods=['POST'])
def predict():
    # retrieve global variables to store input and output
    global model_input
    global model_output
    
    # get text from the incoming request (submitted on predict button click)
    text = request.form['input_text']
    
    # convert text to model input vector
    final_features = input_transformer.transform([text])
    
    # use classifier's predict method to get prediction
    prediction = model.predict(final_features)
    
    # store model input and output
    model_input = text
    model_output = prediction[0]
    return model_output


@app.route('/save_pred', methods=['POST'])
def save_pred():
    # retrieve global variables
    global model_input
    global model_output

    # vectorize user input
    final_features = input_transformer.transform([model_input])
    
    # get user's button choice (correct/incorrect)
    save_type = request.form["save_type"]
    
    # modify global variable if user selected "incorrect" for retraining
    if(save_type == 'incorrect'):
        if(model_output == 'p'):
            model_output = 'n'
        elif(model_output == 'n'):
            model_output = 'p'
        else:
            print("Error: Model output was neither N nor P")
    

    # Strengthen weight of particular connection
    max_iter = 100
    counter = 0
    for i in range (0,max_iter):
        model.partial_fit(final_features, [model_output])
        if(model.predict(final_features) == [model_output]):
            counter = i
            break
    
    # Save trained model pickle
    joblib.dump(model, '../../review_sentiment.pkl')
    
    
    return ""

if __name__ == "__main__":
    app.run(debug=True)