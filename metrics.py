def calculate_accuracy(labels, predicted):

    # Calculate the total number of predictions
    total = labels.size(0)

    # Calculate the number of correct predictions
    correct = (predicted == labels).sum().item()

    # Calculate the accuracy
    accuracy = 100 * correct / total

    return accuracy

def calculate_metrics(labels, predicted):
    
    # Ensure binary output by checking the maximum and minimum values
    assert labels.max() <= 1 and labels.min() >= 0, "Labels must be binary."
    assert predicted.max() <= 1 and predicted.min() >= 0, "Predictions must be binary."
    
    # Calculate TP, TN, FP, FN
    TP = ((predicted == 1) & (labels == 1)).sum().item()
    TN = ((predicted == 0) & (labels == 0)).sum().item()
    FP = ((predicted == 1) & (labels == 0)).sum().item()
    FN = ((predicted == 0) & (labels == 1)).sum().item()
    
    # Calculate metrics
    sensitivity = TP / (TP + FN) if (TP + FN) != 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) != 0 else 0
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = sensitivity  # Recall is the same as sensitivity
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    
    return sensitivity, specificity, precision, f1_score
