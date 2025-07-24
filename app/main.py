# app/main.py

from flask import Flask, jsonify, request, redirect, abort
from datetime import datetime, timezone

from . import utils
from .models import url_db, db_lock

app = Flask(__name__)


@app.route('/')
def health_check():
    """Health check endpoint to confirm the service is running."""
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    Creates a short code for a given long URL.
    Accepts a POST request with a JSON body: {"url": "..."}
    """
    # 1. Get and validate the input JSON
    data = request.get_json()
    if not data or 'url' not in data:
        abort(400, description="Invalid request: JSON body with 'url' key is required.")

    original_url = data['url']
    if not utils.validate_url(original_url):
        abort(400, description="Invalid URL format.")

    # 2. Generate a unique short code (safer loop)
    max_retries = 100
    for _ in range(max_retries):
        short_code = utils.generate_short_code()
        if short_code not in url_db:
            break
    else:
        abort(500, description="Could not generate a unique short code after several attempts.")

    # 3. Store the new mapping in our 'database'
    with db_lock:
        url_db[short_code] = {
            "original_url": original_url,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clicks": 0
        }

    # 4. Return the successful response
    short_url = request.host_url + short_code
    return jsonify({
        "short_code": short_code,
        "short_url": short_url
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """
    Redirects a short code to its original long URL.
    Increments the click count for the URL.
    """
    with db_lock:
        if short_code not in url_db:
            abort(404)
        
        url_db[short_code]['clicks'] += 1
        original_url = url_db[short_code]['original_url']

    return redirect(original_url)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Returns analytics for a given short code."""
    if short_code not in url_db:
        abort(404)
    
    stats = {
        "url": url_db[short_code]['original_url'],
        "created_at": url_db[short_code]['created_at'],
        "clicks": url_db[short_code]['clicks']
    }
    return jsonify(stats)

if __name__ == '__main__':
    # Ensure the port is set to 8080
    app.run(host='0.0.0.0', port=8080, debug=True)