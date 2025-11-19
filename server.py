"""
Flask server for Emotion Detection application.
This module provides a web interface for analyzing emotions in text.
"""

import sys
import os
from flask import Flask, render_template, request

# Add the current directory to path to import our package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from EmotionDetection import emotion_detector
except ImportError as import_error:
    print(f"Error importing EmotionDetection: {import_error}")
    print("Make sure the EmotionDetection package is properly set up")
    emotion_detector = None

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the main application page.
    
    Returns:
        str: Rendered HTML template for the main page.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    """
    Analyze emotion from text provided as query parameter.
    
    Returns:
        str: Formatted emotion analysis results or error message.
    """
    if emotion_detector is None:
        return "Emotion detection service is not available. Please check the server configuration.", 500

    try:
        text_to_analyze = request.args.get('textToAnalyze', '').strip()

        # Analyze emotion using our package
        result = emotion_detector(text_to_analyze)

        # Check for blank input or None dominant_emotion
        if result.get('dominant_emotion') is None:
            return "Invalid text! Please try again!", 400

        # Check for other errors from emotion_detector
        if "error" in result:
            return f"Emotion analysis failed: {result['error']}", 500

        # Format the response as requested
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )

        return response_text

    except Exception as exception:
        return f"An unexpected error occurred: {str(exception)}", 500


if __name__ == '__main__':
    print("Starting Emotion Detection Server...")
    print("Access the application at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)