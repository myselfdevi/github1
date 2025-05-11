from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

CSV_FILE = 'gold_savings.csv'

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['Date', 'Gold_grams', 'Gold_value'])
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        grams = float(request.form['grams'])
        rate = float(request.form['rate'])
        value = grams * rate
        date = datetime.now().strftime('%Y-%m-%d')
        new_entry = pd.DataFrame([[date, grams, value]], columns=['Date', 'Gold_grams', 'Gold_value'])

        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        return redirect(url_for('summary'))
    return render_template('add.html')

@app.route('/summary')
def summary():
    df = pd.read_csv(CSV_FILE)
    total_grams = df['Gold_grams'].sum()
    total_value = df['Gold_value'].sum()
    return render_template('summary.html', grams=total_grams, value=total_value)

@app.route('/progress')
def progress():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # Plot
    plt.figure(figsize=(8, 4))
    plt.plot(df['Date'], df['Gold_grams'].cumsum(), marker='o')
    plt.title("Gold Savings Progress")
    plt.xlabel("Date")
    plt.ylabel("Total Gold (grams)")
    plt.tight_layout()
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()
    return render_template('progress.html', plot_url=plot_path)

if __name__ == '__main__':
    app.run(debug=True)