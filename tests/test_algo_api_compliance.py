# This template comes with some tests to help you to make sure
# that your service is compliant with the Algo API spec.

# The tests will try to test the different algorithms provided by the
# service by looking at their inputs and outputs and by trying to
# run them with fake data.

# Those tests are not exhaustive and are only here to help you to
# make sure that your service is compliant with the Algo API spec.

# The tests won't be able to test the real behavior of your algorithms,
# they will only test the inputs and outputs of your algorithms.

import requests
import json

from algorithms_specific_tests import objectDetectionMetricsTests

appUrl = "http://localhost:3020/"

algorithms = []

ALGORITHMS_SPECIFIC_TESTS = {
    "ObjectsDetectionMetrics": objectDetectionMetricsTests.test_object_detection_metrics_algorithm  # noqa
}


def test_get_algorithms():
    global algorithms
    url = appUrl + "algorithms"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    algorithms = json.loads(resp.text)
    assert type(algorithms) is list

    for dp in json.loads(resp.text):
        assert type(dp) is dict
        assert "id" in dp
        assert "inputs" in dp
        assert "outputs" in dp

    print("Number of algorithms: " + str(len(algorithms)))


def test_run_algorithm():
    for algorithm in algorithms:
        print("Testing algorithm: " + algorithm["id"])

        if algorithm["id"] in ALGORITHMS_SPECIFIC_TESTS:
            ALGORITHMS_SPECIFIC_TESTS[algorithm["id"]](appUrl)
            continue

        url = appUrl + "algorithms/" + algorithm["id"] + "/run"

        # Create fake inputs
        inputs = []
        for input_spec in algorithm["inputs"]:
            input = {"name": input_spec["name"], "value": None}

            if "default" in input_spec:
                input["value"] = input_spec["default"]
            elif "availableValues" in input_spec:
                input["value"] = input_spec["availableValues"][0]
            else:
                if input_spec["type"] == "number":
                    input["value"] = 10
                elif input_spec["type"] == "string":
                    input["value"] = "test"
                elif input_spec["type"] == "boolean":
                    input["value"] = True
                elif input_spec["type"] == "array":
                    if input_spec["arrayType"] == "number":
                        input["value"] = [1, 2, 3, 4, 5]
                    elif input_spec["arrayType"] == "string":
                        input["value"] = ["a", "b", "c", "d", "e"]
                    elif input_spec["arrayType"] == "boolean":
                        input["value"] = [True, False, True, False, True]
                    elif input_spec["arrayType"] == "dict":
                        input["value"] = [{"a": 1}, {"b": 2}, {"c": 3}]
                    elif input_spec["arrayType"] == "array":
                        input["value"] = [[1, 2], [3, 4], [5, 6]]
                    else:
                        input["value"] = [1, 2, 3, 4, 5]
                elif input_spec["type"] == "dict":
                    input["value"] = {"a": 1, "b": 2, "c": 3}
                else:
                    input["value"] = "test"

            inputs.append(input)

        # Call the algorithm
        print("Inputs: " + str(inputs))
        resp = requests.post(url=url, headers={}, json={"inputs": inputs})

        # Check the response
        assert resp.status_code == 200

        # Check the outputs
        outputs = json.loads(resp.text)
        assert type(outputs) is list
        assert len(outputs) == len(algorithm["outputs"])
        for output in outputs:
            assert "name" in output
            assert "value" in output
            assert output["name"] in [
                output_spec["name"] for output_spec in algorithm["outputs"]
            ]

            # Check the type of the output
            output_spec = [
                output_spec
                for output_spec in algorithm["outputs"]
                if output_spec["name"] == output["name"]
            ][0]
            if output_spec["type"] == "number":
                assert type(output["value"]) is int or type(output["value"]) is float

            if output_spec["type"] == "string":
                assert type(output["value"]) is str

            if output_spec["type"] == "boolean":
                assert type(output["value"]) is bool

            if output_spec["type"] == "list":
                assert type(output["value"]) is list
                for value in output["value"]:
                    if output_spec["arrayType"] == "number":
                        assert type(value) is int or type(value) is float
                    if output_spec["arrayType"] == "string":
                        assert type(value) is str
                    if output_spec["arrayType"] == "boolean":
                        assert type(value) is bool

            print("Output: " + str(output))
