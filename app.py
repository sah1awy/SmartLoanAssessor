from flask import Flask, Response, url_for, redirect, render_template, request, jsonify
import pickle
import math
import pandas as pd
import numpy as np

app = Flask(__name__)
model = pickle.load(open("model.pkl",'rb'))
scaler = pickle.load(open('scaler.pkl','rb'))
feats = ['no_of_dependents', 'income_annum', 'loan_amount', 'loan_term',
       'cibil_score', 'residential_assets_value',
       'commercial_assets_value', 'luxury_assets_value',
       'bank_asset_value']
selected_feats = ['no_of_dependents', 'income_annum', 'loan_amount', 'loan_term',
       'cibil_score', 'residential_assets_value', 'commercial_assets_value',
       'bank_asset_value']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    no_of_dependents = float(request.form.get("no_of_dependents"))
    income_annum = float(request.form["income_annum"])
    loan_amount = float(request.form["loan_amount"])
    loan_term = float(request.form["loan_term"])
    cibil_score = float(request.form["cibil_score"])
    residential_assets_value = float(request.form["residential_assets_value"])
    commercial_assets_value = float(request.form["commercial_assets_value"])
    luxury_assets_value = float(request.form["luxury_assets_value"])
    bank_asset_value = float(request.form["bank_asset_value"])
    x = np.array([no_of_dependents, income_annum, loan_amount, loan_term,
       cibil_score, residential_assets_value,
       commercial_assets_value, luxury_assets_value,
       bank_asset_value])
    x_scaled = scaler.transform(np.array(x,ndmin=2))
    mask = np.array([True if feat in selected_feats else False for feat in feats])
    x_scaled = x_scaled.flatten()
    x_masked = x_scaled[mask]
    x_masked = np.array(x_masked,ndmin=2)
    res = model.predict(x_masked)[0]
    # Our model treating approved as 0 and rejected as 1
    if res == 0:
        cat = 'Approved'
    else:
        cat = 'Rejected'
    return render_template("index.html",prediction_text="Loan Status: {}".format(cat))


if __name__ == "__main__":
    app.run(debug=True)
    