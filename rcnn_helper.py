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
