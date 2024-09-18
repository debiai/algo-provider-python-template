from utils.utils import get_input_from_inputs
import numpy as np
import pandas as pd



def validate_classification_object(obj, object_type):
    predicted_object_keys = ["class", "confidence"]
    if object_type == "gt":
        assert type(obj) == str
    elif object_type == "prediction":
        for k in predicted_object_keys:
            if not k in obj.keys():
                raise TypeError("The object is missing the key ", k)
    else:
        raise TypeError("The object should have a gt or prediction type")


def validate_detection_object(obj, object_type):
    gt_object_keys = ["category", "bounding_box"]
    detected_object_keys = ["category", "bounding_box", "confidence"]
    bounding_box_format = ["x", "y", "w", "h"]

    if object_type == "gt":
        for k in gt_object_keys:
            if not k in obj.keys():
                raise TypeError("")
        for i in bounding_box_format:
            if not i in obj.get("bounding_box", {}).keys():
                raise TypeError("")
            
    elif object_type == "detections":
        for k in detected_object_keys:
            if not k in obj.keys():
                raise TypeError("")
        for i in bounding_box_format:
            if not i in obj.get("bounding_box", {}).keys():
                raise TypeError("")
    
    else:
        raise TypeError("")
    


def compute_confusion_matrix(gt_y, pred_y, labels):
    if labels is None:
        labels = set(gt_y)

    assert len(gt_y) == len(pred_y)
    confusion_matrix = np.zeros(len(labels), len(labels))
    for i in range(len(gt_y)):
        if gt_y[i] == pred_y[i]:
            confusion_matrix[gt_y[i], gt_y[i]] += 1
        else:
            confusion_matrix[gt_y[i], pred_y[i]] += 1
            confusion_matrix[pred_y[i], gt_y[i]] += 1

    return confusion_matrix


def classification_metrics(inputs):

    gt_y = get_input_from_inputs(
        inputs,
        "ground_truths",
        expected_input_type="array",
        expected_list_type="string"
    )

    pred_y = get_input_from_inputs(
        inputs,
        "predictions",
        expected_input_type="array",
        expected_list_type="string"
    )

    # Get the list of the ground truths labels
    labels = set(gt_y)

    # The ground truths and the predictions should have the same length
    assert len(gt_y) == len(pred_y)

    # Validate the ground truths and predictions

    # Compute confusion matrix
    confusion_matrix = compute_confusion_matrix(gt_y, pred_y, labels)

    # Compute TP, TN, FP and FN for each class
    results = dict.fromkeys(labels, {"TP": 0, "TN": 0, "FP": 0, "FN": 0})   
    for k, _ in results.items():
        tp = confusion_matrix[k, k] 
        fp = confusion_matrix[:, k] - tp
        fn = confusion_matrix[k, :] - tp
        results[k]["TP"] = tp
        results[k]["FP"] = fp
        results[k]["FN"] = fn
        results[k]["TN"] = len(gt_y) - tp - fp - fn

    # Compute Precision and Recall for each class 
    precision_recall_per_class = dict.fromkeys(labels, {"Precision": .0, "Recall": .0})
    for k, _ in results.items():
        precision_recall_per_class[k]["Precision"] = results[k]["TP"] / (results[k]["TP"] + results[k]["FP"])
        precision_recall_per_class[k]["Recall"] = results[k]["TP"] / (results[k]["TP"] + results[k]["FN"])

    precision = sum([v["Precision"] for _, v in precision_recall_per_class.items()]) / len(labels)
    recall = sum([v["Recall"] for _, v in precision_recall_per_class.items()]) / len(labels)
    f1_score =  2 * (precision * recall) / (precision + recall)
    total_metrics = {"Precision": precision, "Recall": recall, "f1-score": f1_score}

    return precision_recall_per_class, total_metrics


def compute_iou(bbox1, bbox2):

    # Compute the intersection of bbox1 and bbox2
    xA = max(bbox1[0], bbox2[0])
    yA = max(bbox1[1], bbox2[1])
    xB = min(bbox1[0] + bbox1[2], bbox2[0] + bbox2[2])
    yB = min(bbox1[1] + bbox1[3], bbox2[1] + bbox2[3])
    intersection = (xB - xA + 1) * (yB - yA + 1)

    # Compute the union of bbox1 and bbox2
    area1 = bbox1[2] * bbox1[3]
    area2 = bbox2[2] * bbox2[3]
    union = area1 + area2 - intersection

    # Compute IoU
    iou = float(intersection / union)

    return iou


def object_detection_metrics(inputs):
    gt = get_input_from_inputs(
        inputs,
        "ground_truths",
        expected_input_type="array",
        expected_list_type="object"
    )

    detections = get_input_from_inputs(
        inputs,
        "detections",
        expected_input_type="array",
        expected_list_type="object"
    )

    categories = get_input_from_inputs(
        inputs,
        "categories",
        expected_input_type="array",
        expected_list_type="string"
    )

    iou_threshold = get_input_from_inputs(
        inputs,
        "iou_threshold",
        expected_input_type="number"
    )

    images_names = list(gt.keys())
    metrics_per_category = pd.DataFrame(data=np.zeros((len(categories), 6)), index=categories, 
                                    columns=["All_GT", "All_Detections", "TP", "FP", "Precision", "Recall"])
    metrics_per_image = pd.DataFrame(data=np.zeros((len(images_names), 6)), index=images_names, 
                                    columns=["All_GT", "All_Detections", "TP", "FP", "Precision", "Recall"])
    
    for idx in range(len(images_names)):
        image_name = images_names[idx]
        gt_objects = gt.get(image_name, list())
        metrics_per_image.at[image_name, "All_GT"] = len(gt_objects)
        detected_objects = detections.get(image_name, list())
        ordered_detected_objects = sorted(detected_objects, key=lambda d: d['confidence'], reverse=True)
        metrics_per_image.at[image_name, "All_Detections"] = len(detected_objects)

        for i in range(len(gt_objects)):    # Loop through GT
            category1 = gt_objects[i]["category"]
            bbox1 = list(gt_objects[i]["bounding_box"].values())
            metrics_per_category.at[category1, "All_GT"] += 1

            for j in range(len(ordered_detected_objects)):  # Loop through Detections
                category2 = ordered_detected_objects[j]["category"]
                bbox2 = list(ordered_detected_objects[j]["bounding_box"].values())
                metrics_per_category.at[category2, "All_Detections"] += 1

                iou = compute_iou(bbox1, bbox2)

                if iou >= iou_threshold:
                    if not gt[image_name][i].get("found", False):
                        if category1 == category2:
                            gt[image_name][i]["found"] = True
                            gt[image_name][i]["confidence"] = ordered_detected_objects[j]["confidence"]
                            metrics_per_category.at[category1, "TP"] += 1
                            metrics_per_image.at[image_name, "TP"] += 1
                        else:
                            gt[image_name][i]["found"] = False
                            metrics_per_category.at[category2, "FP"] += 1
                            metrics_per_image.at[image_name, "FP"] += 1
                    else:
                        metrics_per_category.at[category2, "FP"] += 1
                        metrics_per_image.at[image_name, "FP"] += 1
                        
                else:
                    continue

    for idx, row in metrics_per_category.iterrows():
        metrics_per_category.at[idx, "Precision"] = metrics_per_category.loc[idx, "TP"] / (metrics_per_category.loc[idx, "TP"] + metrics_per_category.loc[idx, "FP"])
        metrics_per_category.at[idx, "Recall"] = metrics_per_category.loc[idx, "TP"] / metrics_per_category.loc[idx, "All_GT"]

    for idx, row in metrics_per_image.iterrows():
        metrics_per_image.at[idx, "Precision"] = metrics_per_image.loc[idx, "TP"] / (metrics_per_image.loc[idx, "TP"] + metrics_per_image.loc[idx, "FP"])
        metrics_per_image.at[idx, "Recall"] = metrics_per_image.loc[idx, "TP"] / metrics_per_image.loc[idx, "All_GT"]

    # Covert data frames to Dicts 
    
    return [metrics_per_category, metrics_per_image, gt]
        