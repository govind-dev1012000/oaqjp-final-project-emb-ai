import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyze the emotion of the given text using Watson NLP Emotion Predict service
    and return formatted emotion scores with dominant emotion
    """
    # Check for blank input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    # URL for the Watson NLP Emotion Predict service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Headers required for the API call
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    # Input data in the required JSON format
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    try:
        # Make the POST request to the Watson NLP service
        response = requests.post(url, headers=headers, json=input_json)
        
        # Check if the request was successful
        if response.status_code == 400:
            # Return None values for all keys when status code is 400
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        response.raise_for_status()
        
        # Convert response text to dictionary
        response_dict = response.json()
        
        # Extract emotion scores from the response
        emotion_predictions = response_dict.get('emotionPredictions', [])
        if not emotion_predictions:
            return {"error": "No emotion predictions found in response"}
        
        # Get the emotion scores from the first prediction
        emotions = emotion_predictions[0].get('emotion', {})
        
        # Extract individual emotion scores
        anger_score = emotions.get('anger', 0)
        disgust_score = emotions.get('disgust', 0)
        fear_score = emotions.get('fear', 0)
        joy_score = emotions.get('joy', 0)
        sadness_score = emotions.get('sadness', 0)
        
        # Create a dictionary of emotions and their scores
        emotion_scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Find the dominant emotion (emotion with highest score)
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Return the formatted output
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
        
    except requests.exceptions.RequestException as e:
        # Return error message if request fails
        return {"error": f"Request failed: {str(e)}"}
    except ValueError as e:
        # Return error message if JSON parsing fails
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        # Return error message for any other exceptions
        return {"error": f"An error occurred: {str(e)}"}