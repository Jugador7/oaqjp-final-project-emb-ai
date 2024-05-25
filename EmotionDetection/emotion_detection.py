"""
This module provides a simple Flask web application and a function
for sentiment analysis using the Watson NLP service.
"""
import requests

def emotion_detector(text_to_analyze):
    """
    This function analyzes a string and sends it to Watson to detect the emotion it represents.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    json = { "raw_document": { "text": text_to_analyze } }
    
    try:
        response = requests.post(url, json=json, headers=headers, timeout=10)
        # Set a timeout of 10 seconds
        response.raise_for_status()  # Raises an HTTPError for bad responses
        formatted_response = response.json()

        if response.status_code == 200:
            emotion_scores = formatted_response['emotionPredictions'][0]['emotion']
            anger_score = emotion_scores['anger']
            disgust_score = emotion_scores['disgust']
            fear_score = emotion_scores['fear']
            joy_score = emotion_scores['joy']
            sadness_score = emotion_scores['sadness']
            # Determine the dominant emotion
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        else:
            anger_score = None
            disgust_score = None
            fear_score = None
            joy_score = None
            sadness_score = None
            dominant_emotion = None
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'anger': None, 'disgust' : None,'fear' : None,
                'joy' : None,'sadness' : None, 'dominant_emotion': None}

    return {
        'anger': anger_score, 
        'disgust' : disgust_score,
        'fear' : fear_score,
        'joy' : joy_score,
        'sadness' : sadness_score, 
        'dominant_emotion': dominant_emotion
    }

#ejecutar python
#from emotion_detection import emotion_detector
#emotion_detector("I love this new technology.")