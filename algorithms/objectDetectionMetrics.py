from utils.utils import get_input_from_inputs


def validate_object(obj, object_type, image_index, object_index):
    required_keys = ["class", "coordinates"]
    coordinate_keys = ["x", "y", "w", "h"]

    for key in required_keys:
        if key not in obj:
            raise TypeError(
                f"The {object_type} object {object_index} in image {image_index} \
 has no {key}"
            )

    for key in coordinate_keys:
        if key not in obj["coordinates"]:
            raise TypeError(
                f"The {object_type} object {object_index} in image {image_index} \
has no {key} coordinate"
            )


def object_is_in_list(obj, obj_list):
    for obj2 in obj_list:
        if obj["class"] == obj2["class"]:
            return True
    return False


def objects_detection_metrics(inputs):
    # Expected inputs:
    # [{
    #     "name": "images_objects_ground_truth",
    #     "value": [
    #         [
    #             {
    #                 "class": "images_objects_ground_truth",
    #                 "coordinates": {"x": 0, "y": 0, "w": 100, "h": 100},
    #             }
    #         ]
    #     ],
    # },
    # {
    #     "name": "images_objects_predicted",
    #     "value": [
    #         [
    #             {
    #                 "class": "images_objects_predicted",
    #                 "coordinates": {"x": 0, "y": 0, "w": 100, "h": 100},
    #             }
    #         ]
    #     ],
    # }]

    # Expected outputs:
    # {
    #     "name": "results",
    #     "value": [{"precision": 0.5, "recall": 0.5, "f1": 0.5}],
    # },

    images_ground_truth = get_input_from_inputs(
        inputs,
        "images_objects_ground_truth",
        expected_input_type="array",
        expected_list_type="array",
    )

    objects_predicted = get_input_from_inputs(
        inputs,
        "images_objects_predicted",
        expected_input_type="array",
        expected_list_type="array",
    )

    # Check that the two lists have the same length
    if len(images_ground_truth) != len(objects_predicted):
        raise TypeError("The two lists must have the same length")

    # Validate images_ground_truth
    for i, image in enumerate(images_ground_truth):
        for j, obj in enumerate(image):
            validate_object(obj, "Ground truth", i, j)

    # Validate objects_predicted
    for i, image in enumerate(objects_predicted):
        for j, obj in enumerate(image):
            validate_object(obj, "Predicted", i, j)

    # Calculate the metrics
    results = []
    for i, image in enumerate(images_ground_truth):
        tp = 0
        fp = 0
        fn = 0
        for obj in image:
            if object_is_in_list(obj, objects_predicted[i]):
                tp += 1
            else:
                fn += 1
        for obj in objects_predicted[i]:
            if not object_is_in_list(obj, image):
                fp += 1
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)
        results.append({"precision": precision, "recall": recall, "f1": f1})

    return [{"name": "results", "value": results}]
