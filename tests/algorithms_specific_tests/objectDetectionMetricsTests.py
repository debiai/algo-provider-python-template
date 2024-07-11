import requests
import json


def test_object_detection_metrics_algorithm(appUrl):
    test_with_good_values(appUrl)
    test_with_bad_values(appUrl)


def test_with_good_values(appUrl):
    url = appUrl + "algorithms/ObjectsDetectionMetrics/run"

    # Create simple inputs
    inputs = [
        {
            "name": "images_objects_ground_truth",
            "value": [
                [
                    {
                        "class": "a",
                        "coordinates": {
                            "x": 0,
                            "y": 0,
                            "w": 100,
                            "h": 100,
                        },
                    },
                    {
                        "class": "b",
                        "coordinates": {
                            "x": 50,
                            "y": 50,
                            "w": 100,
                            "h": 100,
                        },
                    },
                ]
            ],
        },
        {
            "name": "images_objects_predicted",
            "value": [
                [
                    {
                        "class": "a",
                        "coordinates": {
                            "x": 0,
                            "y": 0,
                            "w": 100,
                            "h": 100,
                        },
                    },
                    {
                        "class": "b",
                        "coordinates": {
                            "x": 50,
                            "y": 50,
                            "w": 100,
                            "h": 100,
                        },
                    },
                    {
                        "class": "c",
                        "coordinates": {
                            "x": 50,
                            "y": 50,
                            "w": 100,
                            "h": 100,
                        },
                    },
                ]
            ],
        },
    ]

    # Call the algorithm
    print("Inputs: " + str(inputs))
    resp = requests.post(url=url, headers={}, json={"inputs": inputs})

    # Check the response
    assert resp.status_code == 200

    # Check the outputs
    outputs = json.loads(resp.text)
    assert type(outputs) is list

    # Check the outputs
    assert len(outputs) == 1
    output = outputs[0]
    print("Output: " + str(output))
    assert "name" in output
    assert output["name"] == "results"
    assert "value" in output
    assert type(output["value"]) is list
    assert len(output["value"]) == len(inputs[0]["value"])

    for value in output["value"]:
        assert "precision" in value
        assert "recall" in value
        assert "f1" in value
        assert type(value["precision"]) is float
        assert type(value["recall"]) is float
        assert type(value["f1"]) is float


def test_with_bad_values(appUrl):
    url = appUrl + "algorithms/ObjectsDetectionMetrics/run"

    # Bad coordinates
    inputs = [
        {
            "name": "images_objects_ground_truth",
            "value": [
                [
                    {
                        "class": "a",
                        "coordinates": {
                            "x1": 0,
                            "y1": 0,
                            "x2": 100,
                            "y2": 100,
                        },
                    },
                ]
            ],
        },
        {
            "name": "images_objects_predicted",
            "value": [
                [
                    {
                        "class": "a",
                        "coordinates": {
                            "x1": 0,
                            "y1": 0,
                            "x2": 100,
                            "y2": 100,
                        },
                    },
                ]
            ],
        },
    ]
    resp = requests.post(url=url, headers={}, json={"inputs": inputs})
    assert resp.status_code == 400
    assert "no x coordinate" in json.loads(resp.text)

    # Empty objects
    inputs = [
        {
            "name": "images_objects_ground_truth",
            "value": [
                [
                    {},
                    {},
                    {},
                    {},
                ]
            ],
        },
        {
            "name": "images_objects_predicted",
            "value": [
                [
                    {},
                    {},
                    {},
                    {},
                ]
            ],
        },
    ]
    resp = requests.post(url=url, headers={}, json={"inputs": inputs})
    assert resp.status_code == 400
    assert "no class" in json.loads(resp.text)

    # Different length
    inputs = [
        {
            "name": "images_objects_ground_truth",
            "value": [
                [
                    {
                        "class": "a",
                        "coordinates": {
                            "x": 0,
                            "y": 0,
                            "w": 100,
                            "h": 100,
                        },
                    },
                ]
            ],
        },
        {
            "name": "images_objects_predicted",
            "value": [
                [
                    {
                        "class": "a",
                        "coordinates": {
                            "x": 0,
                            "y": 0,
                            "w": 100,
                            "h": 100,
                        },
                    },
                ],
                [
                    {
                        "class": "b",
                        "coordinates": {
                            "x": 0,
                            "y": 0,
                            "w": 100,
                            "h": 100,
                        },
                    },
                ],
            ],
        },
    ]
    resp = requests.post(url=url, headers={}, json={"inputs": inputs})
    assert resp.status_code == 400
    assert "must have the same length" in json.loads(resp.text)
