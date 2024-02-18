def generate_samples(anchor_tlbr_boxes, label_tlbr_boxes, label_classes, iou_fcn, pos_iou_threshold=0.5, neg_iou_threshold=0.3):
    positive_samples = []
    negative_samples = []

    for candidate_tlbr_box in candidate_tlbr_boxes:
        max_iou = 0
        matched_class = -1  # Default to -1 for negative samples
        matched_box_tlbr = None  # Use None for unmatched boxes

        for gt_box_tlbr, gt_class in zip(label_tlbr_boxes, label_classes):
            current_iou = iou_fcn(candidate_tlbr_box, gt_box_tlbr)
            if current_iou > max_iou:
                max_iou = current_iou
                matched_box_tlbr = gt_box_tlbr if current_iou >= neg_iou_threshold else None
                if current_iou >= pos_iou_threshold:
                    matched_class = gt_class
                elif current_iou < neg_iou_threshold:
                    matched_class = -1
                else:
                    matched_class = None

        if matched_class is not None and matched_class != -1:
            positive_samples.append((candidate_tlbr_box, matched_box_tlbr, matched_class))
        elif matched_class == -1:
            negative_samples.append((candidate_tlbr_box, None, matched_class))

    return positive_samples, negative_samples

def hard_negative_sampler(X, y, svm, n_hard_negatives=10):

    # Predict on all samples
    if svm:  # If a preliminary model is provided, use it to find hard negatives
        confidences = svm.decision_function(X[y == -1])
        # Sort negatives by confidence, higher means more confident (and wrong)
        hard_negatives_indices = np.argsort(-confidences)[:n_hard_negatives]
        hard_negatives = X[y == -1][hard_negatives_indices]
        hard_negatives_labels = y[y == -1][hard_negatives_indices]
        
        # Combine hard negatives with positive samples
        X_final = np.vstack([X[y == 1], hard_negatives])
        y_final = np.concatenate([y[y == 1], hard_negatives_labels])
    else:  # If no model is provided, skip hard negative mining
        X_final = X
        y_final = y
        
    return X_final, y_final

def train_svms_for_rcnn(samples, n_classes, hard_negative_sampler, C=1.0, n_hard_negatives=10):
    
    # Initialize a list to hold an SVM model for each class
    svms = [SVC(kernel='linear', C=C) for _ in range(n_classes)]

    # Extract features and labels from samples
    X = np.array([sample[0] for sample in samples])  # Convert list to numpy array for efficiency
    y = np.array([sample[1] for sample in samples])

    for class_idx in range(n_classes):
        
        # Treat the current class as positive (1) and all others as negative (-1)
        y_binary = np.where(y == class_idx, 1, -1)

        # Train a preliminary SVM model
        preliminary_svm = SVC(kernel='linear', C=C)
        preliminary_svm.fit(X, y_binary)
        
        # Perform hard negative mining
        X_train, y_train = hard_negative_sampler(X, y_binary, preliminary_svm, n_hard_negatives)

        # Train the SVM for the current class
        svms[class_idx].fit(X_train, y_train)

    return svms

import torch

def extract_features(x, model):
    # Ensure the model is in evaluation mode and gradient computation is off
    model.eval()
    with torch.no_grad():
        # Directly pass the input through the model
        features = model(x)
    return features
