import yaml
from yaml.loader import SafeLoader


def get_app_version():
    # Read the version from the API YAML file
    OPEN_API_PATH = "algo-api/OpenAPI/Algo_OpenAPI_V0.yaml"
    try:
        with open(OPEN_API_PATH) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data["info"]["version"]
    except Exception as e:
        print(e)
        return "?.?.?"


def get_input_from_inputs(
    inputs, input_name, expected_input_type=None, expected_list_type=None
):
    # Get the input from of the inputs list from a given name
    # Check the type and the subtype if needed

    for i, input in enumerate(inputs):
        if "name" not in input:
            raise TypeError("Input n°{} has no name".format(i))

        if "value" not in input:
            raise TypeError("Input {} has no value".format(input["name"]))

        if input["name"] == input_name:
            # Check the type
            if expected_input_type == "number":
                if not isinstance(input["value"], (int, float)):
                    raise TypeError(
                        "Input {} is not a number, but a {}".format(
                            input_name, type(input["value"])
                        )
                    )
            elif expected_input_type == "string":
                if not isinstance(input["value"], str):
                    raise TypeError(
                        "Input {} is not a string but a {}".format(
                            input_name, type(input["value"])
                        )
                    )
            elif expected_input_type == "array":
                if not isinstance(input["value"], list):
                    raise TypeError(
                        "Input {} is not an array but a {}".format(
                            input_name, type(input["value"])
                        )
                    )

                # Check the subtype
                if expected_list_type == "number":
                    for value in input["value"]:
                        if not isinstance(value, (int, float)):
                            raise TypeError(
                                "Input {} is not an array of numbers but of {}".format(
                                    input_name, type(value)
                                )
                            )
                elif expected_list_type == "string":
                    for value in input["value"]:
                        if not isinstance(value, str):
                            raise TypeError(
                                "Input {} is not an array of strings but of {}".format(
                                    input_name, type(value)
                                )
                            )
                elif expected_list_type == "object":
                    for value in input["value"]:
                        if not isinstance(value, dict):
                            raise TypeError(
                                "Input {} is not an array of objects but of {}".format(
                                    input_name, type(value)
                                )
                            )
                elif expected_list_type == "array":
                    for value in input["value"]:
                        if not isinstance(value, list):
                            raise TypeError(
                                "Input {} is not an array of arrays but of {}".format(
                                    input_name, type(value)
                                )
                            )

            # Return the value
            return input["value"]

    raise TypeError("Input {} not found in inputs".format(input_name))


# Add other utils functions here
