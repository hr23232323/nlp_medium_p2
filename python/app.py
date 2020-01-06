from flask import Flask, render_template, request
from sklearn.externals import joblib
import csv

#app initialization
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# load models
input_transformer = joblib.load(open(app.static_folder + '/models/input_transformer.pkl', 'rb'))
model = joblib.load(open(app.static_folder + '/models/review_sentiment.pkl', 'rb'))

# global variables for data persistence across requests
model_input=""
model_output=""

# main index page route
@app.route('/')
def home():
    return render_template('index.html', image_filename="img/happy.webp", display_mode="none")

# route for prediction of sentiment analysis model and classifier
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

# route for incremental training of model
@app.route('/save_pred', methods=['POST'])
def save_pred():
    # retrieve global variables
    global model_input
    global model_output

    # vectorize user input
    final_features = input_transformer.transform([model_input])
    
    # get user's button choice (correct/incorrect)
    save_type = request.form["save_type"]

    # return text
    return_text = "The weights were strengthened, thank you for teaching me!"
    
    # modify global variable if user selected "incorrect" for retraining
    if(save_type == 'incorrect'):
        return_text = "The weights were changed, thank you for correcting me!"
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
    joblib.dump(model, (app.static_folder + '/models/review_sentiment.pkl'))
    
    # fields inside CSV to store for retrain verification
    fields = [model_input, model_output, counter]
    
    #retrain model
    with open((app.root_path + '/user_teaching_data.csv'), 'a') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
    
    # return confirmation code for user
    return return_text

if __name__ == "__main__":
    app.run(debug=True)