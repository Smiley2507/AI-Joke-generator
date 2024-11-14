from flask import Flask, render_template, request, jsonify, flash
from jokes import generate_joke
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# List of sound effects for like button
LAUGH_SOUNDS = [
    'giggle1.mp3',
    'laugh1.mp3',
    'giggle2.mp3',
    'laugh2.mp3'
]

@app.route('/')
def home():
    """Render the home page with an initial joke"""
    initial_joke = generate_joke()
    return render_template('index.html', joke=initial_joke)

@app.route('/get-joke', methods=['POST'])
def get_joke():
    """Generate a new joke and return it as JSON"""
    try:
        joke = generate_joke()
        sound = random.choice(LAUGH_SOUNDS)
        return jsonify({
            'status': 'success',
            'joke': joke,
            'sound': sound
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/like-joke', methods=['POST'])
def like_joke():
    """Handle joke like action"""
    sound = random.choice(LAUGH_SOUNDS)
    return jsonify({
        'status': 'success',
        'sound': sound
    })

# Vercel requires this
app.debug = False

# Remove the if __name__ == '__main__' block as it's not needed for Vercel