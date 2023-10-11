import argparse
from datasets import load_dataset
from util import detect_lang
from sklearn.metrics import f1_score

def main():
    # Load the dataset
    dataset = load_dataset('NbAiLab/nbnn_language_detection', split='dev')
    
    # Initialize variables to count correct and wrong predictions
    correct = 0
    total = 0
    y_true = []
    y_pred = []
    
    # Loop over the dataset
    for sample in dataset:
        text = sample['text']
        true_lang = sample['language']
        
        # Detect the language
        detected_lang, _ = detect_lang(text, langs=["nob","nno"],return_proba=True)
        
        # Check if the detected language is correct
        if detected_lang == true_lang:
            correct += 1
        else:
            print(f"Error: Text: '{text}' | Prediction: {detected_lang} | Target: {true_lang}")
        
        # For calculating F1 score
        y_true.append(true_lang)
        y_pred.append(detected_lang)
        
        total += 1
    
    # Calculate accuracy
    accuracy = correct / total
    print(f"Accuracy: {accuracy:.4f}")

    # Calculate F1 score
    f1 = f1_score(y_true, y_pred, average='weighted')
    print(f"F1 Score: {f1:.4f}")

if __name__ == "__main__":
    main()

