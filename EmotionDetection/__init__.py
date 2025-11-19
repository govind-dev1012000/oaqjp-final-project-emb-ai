"""
EmotionDetection - A package for detecting emotions in text using Watson NLP
"""

__version__ = "1.0.0"
__author__ = "IBM DevOps Student"

# Import the main function to make it available at package level
from .emotion_detection import emotion_detector

__all__ = ['emotion_detector']