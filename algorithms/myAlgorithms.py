from utils.utils import get_input_from_inputs

# We have here the functions that will do the actual work of the algorithms.


def addition(inputs):
    # Expected inputs:
    # {
    #     "name": "a",
    #     "value": 5,
    # },
    # {
    #     "name": "b",
    #     "value": 5,
    # }

    # Expected outputs:
    # {
    #     "name": "sum",
    #     "value": 10,
    # },

    a = get_input_from_inputs(inputs, "a", "number")
    b = get_input_from_inputs(inputs, "b", "number")
    # The get_input_from_inputs function will check that the inputs are valid
    # It will raise a TypeError exception if the input is not valid
    # The exception will be catched by the algorithms.py file and will return a 400 error

    return [
        {
            "name": "sum",
            "value": a + b,
        }
    ]


def statistics_of_list(inputs):
    # Expected inputs:
    # {
    #     "name": "data",
    #     "value": [1, 2, 3, 4, 5],
    # }

    # Expected outputs:
    # {
    #     "name": "average",
    #     "value": 3,
    # },
    # {
    #     "name": "median",
    #     "value": 3,
    # },

    data = get_input_from_inputs(inputs, "data", "array", "number")
    # If you want, you can specify the type of the elements
    # of the array for the input validation

    average = sum(data) / len(data)
    median = data[len(data) // 2]

    return [
        {
            "name": "average",
            "value": average,
        },
        {
            "name": "median",
            "value": median,
        },
    ]


def multiply_lists(inputs):
    # Expected inputs:
    # {
    #     "name": "list1",
    #     "value": [1, 2, 3, 4, 5],
    # },
    # {
    #     "name": "list2",
    #     "value": [1, 2, 3, 4, 5],
    # }

    # Expected outputs:
    # {
    #     "name": "product",
    #     "value": [1, 4, 9, 16, 25],
    # },

    list1 = get_input_from_inputs(inputs, "list1", "array", "number")
    list2 = get_input_from_inputs(inputs, "list2", "array", "number")

    # You can raise an exception depending on the algorithm needs
    if len(list1) != len(list2):
        raise TypeError("list1 and list2 must have the same length")

    product = [a * b for a, b in zip(list1, list2)]

    return [
        {
            "name": "product",
            "value": product,
        }
    ]


def add_strings(inputs):
    # Expected inputs:
    # {
    #     "name": "string1",
    #     "value": "Hello",
    # },
    # {
    #     "name": "string2",
    #     "value": "World",
    # }

    # Expected outputs:
    # {
    #     "name": "string",
    #     "value": "Hello World",
    # },

    string1 = get_input_from_inputs(inputs, "string1", "string")
    string2 = get_input_from_inputs(inputs, "string2", "string")

    string = string1 + " " + string2

    return [
        {
            "name": "concatenated string",
            "value": string,
        }
    ]
