from flask import Flask, render_template, request, redirect, jsonify, url_for
import os
from dotenv import load_dotenv
import openai
from datetime import datetime

# Load .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI-KEY")

# Flask app setup
app = Flask(__name__)

# Load OpenAI client (new v1.x style)
client = openai.OpenAI(api_key=openai_api_key)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    filepath = 'data/goals.txt'
    os.makedirs('data', exist_ok=True)

    if request.method == 'POST':
        goal = request.form['goal']
        if goal:
            with open(filepath, 'a') as f:
                f.write(goal + '\n')
        return redirect('/goals')

    goals = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            goals = f.readlines()
    return render_template('goals.html', goals=[g.strip() for g in goals])

@app.route('/delete_goal/<int:goal_index>')
def delete_goal(goal_index):
    filepath = 'data/goals.txt'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            goals = f.readlines()
        if 0 <= goal_index < len(goals):
            del goals[goal_index]
        with open(filepath, 'w') as f:
            f.writelines(goals)
    return redirect('/goals')

@app.route('/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/quotes')
def quotes():
    filepath = 'data/quotes.txt'
    if not os.path.exists(filepath):
        os.makedirs('data', exist_ok=True)
        with open(filepath, 'w') as f:
            f.write("Push yourself, because no one else is going to do it for you.\nStay consistent.\nKeep learning.")

    with open(filepath, 'r') as f:
        quotes = [line.strip() for line in f if line.strip()]
    return render_template('quotes.html', quotes=quotes)

@app.route('/ai')
def ai_page():
    return render_template('ai.html')

@app.route('/ai', methods=['POST'])
def ask_ai():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'No input provided'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant for students."},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({'response': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
