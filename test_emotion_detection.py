import sys
import os

# Add the current directory to Python path
sys.path.append('.')

from EmotionDetection import emotion_detector

def run_tests():
    """Simple unit test function for emotion detection"""
    
    test_data = [
        ("I am glad this happened", "joy"),
        ("I am really mad about this", "anger"),
        ("I feel disgusted just hearing about this", "disgust"),
        ("I am so sad about this", "sadness"),
        ("I am really afraid that this will happen", "fear")
    ]
    
    print("🧪 Running Emotion Detection Unit Tests")
    print("=" * 40)
    
    all_passed = True
    
    for statement, expected in test_data:
        result = emotion_detector(statement)
        
        if "error" in result:
            print(f"❌ ERROR: {statement}")
            print(f"   {result['error']}")
            all_passed = False
            continue
            
        actual = result['dominant_emotion']
        status = "✅ PASS" if actual == expected else "❌ FAIL"
        
        print(f"{status}: '{statement}'")
        print(f"   Expected: {expected}, Got: {actual}")
        
        if actual != expected:
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    run_tests()