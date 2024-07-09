from .myAlgorithms import addition, statistics_of_list, multiply_lists, add_strings


# This is the controller of the service,
# It contains the endpoints that will be exposed to the platform
# We need to expose the following endpoints:
# - /algorithms: Get the list of algorithms that this service can provide
# - /algorithms/{algorithmId}/use: Use an algorithm
# Those two endpoints are defined in the OpenAPI
# The two functions below are the implementation of those endpoints


def get_algorithms():
    """Get all algorithms that this service can provide

    Returns:
        list: List of algorithms
    """

    # This template service exposes tree simples algorithms:
    # 1- Addition: Addition of two numbers
    #   - Input: Two numbers
    #   - Output: a number, the sum of the two input numbers
    # 2- StatisticsOfList: Statistics of a list of numbers
    #   - Input: list of numbers
    #   - Output1: a number, the average of the input list
    #   - Output1: a number, the median of the input list
    # 3- MultiplyLists:
    #   - Input: Two lists of numbers
    #   - Output: a list of numbers, the multiplication of the two input lists

    # We define the algorithms as a list of dictionaries:

    algorithms = [
        # Algorithm 1: Addition
        {
            "id": "Addition",
            "name": "Addition of two numbers",
            "description": "Calculate the sum of two numbers",
            "author": "DebiAI",
            "version": "1.0.0",
            "tags": ["calculations"],
            "inputs": [
                {
                    "name": "a",
                    "description": "First number",
                    "type": "number",
                    "default": 5,
                },
                {
                    "name": "b",
                    "description": "Second number",
                    "type": "number",
                    "default": 5,
                    # You can specify some available values for the input:
                    "availableValues": [2, 5, 10, 100, 1000],
                    "min": 0,
                    "max": 1000,
                    # This will help the user to choose the right value
                },
            ],
            "outputs": [
                {
                    "name": "sum",
                    "description": "Sum of the two numbers",
                    "type": "number",
                }
            ],
        },
        # Algorithm 2: StatisticsOfList
        {
            "id": "StatisticsOfList",
            "name": "Statistics of a list of numbers",
            "description": "Calculate the average and the median of a list of numbers",
            "author": "DebiAI",
            "version": "1.0.0",
            "tags": ["calculations", "statistics"],
            "inputs": [
                {
                    "name": "data",
                    "description": "List of numbers",
                    "type": "array",
                    "arrayType": "number",
                    "lengthMin": 1,
                    "lengthMax": 100000,
                }
            ],
            "outputs": [
                {
                    "name": "average",
                    "description": "Average of the list",
                    "type": "number",
                },
                {
                    "name": "median",
                    "description": "Median of the list",
                    "type": "number",
                },
            ],
        },
        # Algorithm 3: MultiplyLists
        {
            "id": "MultiplyLists",
            "name": "Multiply two lists of numbers",
            # Multi-line description:
            "description": """Multiply two lists of numbers,
the two lists must have the same length,
the result will be a list of the same length as the two input lists""",
            "author": "DebiAI",
            "version": "1.0.0",
            # You can specify the creation and update dates of the algorithm
            "creationDate": "2023-03-22",
            "updateDate": "2023-03-24",
            "tags": ["calculations"],
            "inputs": [
                {
                    "name": "list1",
                    "description": "First list of numbers",
                    "type": "array",
                    "arrayType": "number",
                },
                {
                    "name": "list2",
                    "description": "Second list of numbers",
                    "type": "array",
                    "arrayType": "number",
                },
            ],
            "outputs": [
                {
                    "name": "product",
                    "description": "Multiplication of the two lists",
                    "type": "array",
                    "arrayType": "number",
                }
            ],
        },
        # Algorithm 4: concatenate strings
        {
            "id": "addStrings",
            "version": "1.0.0",
            "inputs": [
                {
                    "name": "string1",
                    "type": "string",
                },
                {
                    "name": "string2",
                    "type": "string",
                    "availableValues": ["titi", "tata", "tutu"],
                },
            ],
            "outputs": [
                {
                    "name": "concatenated string",
                    "description": """concatenated string, with a
space between the two strings""",
                    "type": "string",
                }
            ],
        },
    ]

    # Keep in mind that you can add as many algorithms as you want
    # and that you can build the algorithms list dynamically
    # You can for example fill the "availableValues" field depending
    # of what is available in a database such as a list of models

    # For more information about the algorithm format, see the Algo API documentation:
    # algo-api/README.md

    return algorithms, 200


def use_algorithm(algorithmId, body):
    """Use an algorithm

    Args:
        algorithmId (str): Algorithm ID
        body (dict): Dictionary containing the algorithm inputs

    Returns:
        list: Algorithm outputs, must follow the algorithm description
    """

    algorithm_inputs = body["inputs"]

    try:
        # We call the algorithm based on its ID
        if algorithmId == "Addition":
            return addition(algorithm_inputs)
        elif algorithmId == "StatisticsOfList":
            return statistics_of_list(algorithm_inputs)
        elif algorithmId == "MultiplyLists":
            return multiply_lists(algorithm_inputs)
        elif algorithmId == "addStrings":
            return add_strings(algorithm_inputs)

        # Add as many algorithms as you want

    except TypeError as e:
        # The algorithm was called with invalid inputs
        error_message = "Invalid inputs for algorithm {}: {}".format(
            algorithmId, str(e)
        )
        print(error_message)
        return error_message, 400

    print("Algorithm {} not found".format(algorithmId))
    return "Algorithm not found", 404
