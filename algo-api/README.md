# Algo API

## Context

An algo-provider is a service that allow projects members to create and run algorithms with DebiAI. The API allows users to interact with a large number and variety of algorithms, and to make their own algorithms available.

## Getting started

Let's say you want to make available one or more algorithms to DebiAI. You can do so by creating a Web service (an algo-provider) that implements the Algo API, to help you with the creation of this service, you can start from our [Python template](https://github.com/debiai/algo-provider-python-template).

## API Reference

Full API reference is available in the yaml file :

- [Algo API V0](./OpenAPI/Algo_OpenAPI_V0.yaml)

To view the API reference in a more readable format, you can use the [Swagger Editor](https://editor.swagger.io/).

### API Endpoints

| Endpoint                                           | Description                           |
| -------------------------------------------------- | ------------------------------------- |
| [GET /algorithms](#get-algorithms)                 | Get the list of available algorithms. |
| [POST /algorithms/{id}/run](#post-algorithmsidrun) | Run an algorithm.                     |

### GET /algorithms

Get the list of available algorithms.

#### Request

    GET /algorithms

#### Response

List of algorithms that are available.

```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "author": "string",
    "tags": ["string"],
    "version": "string",
    "creationDate": "string",
    "updateDate": "string",
    "inputs": [
      {
        "name": "string",
        "type": "string",
        "description": "string"
      }
    ],
    "outputs": [
      {
        "name": "string",
        "type": "string",
        "description": "string"
      }
    ]
  }
]
```

**Types**

The Algo API supports the following types for the inputs and outputs:

- [string](supportedTypes.md#string)
- [number](supportedTypes.md#number)
- [boolean](supportedTypes.md#boolean)
- [array](supportedTypes.md#array)

**Tags**

The tags are used to categorize the algorithms, they are not mandatory.
Some possible tags are:

- inference
- train
- calculations
- metrics

### POST /algorithms/{id}/run

Run an algorithm.

The algorithm's `id` is the one specified in the [GET /algorithms]() response.

The inputs will follow the algorithm's inputs specified in the [GET /algorithms]() response.

The outputs need to follow the algorithm's outputs specified in the [GET /algorithms]() response.

#### Request

```json
{
  "inputs": [
    {
      "name": "string",
      "value": "string, number, boolean or array"
    }
  ]
}
```

#### Response

```json
{
  "outputs": [
    {
      "name": "string",
      "value": "string, number, boolean or array"
    }
  ]
}
```

## Moving average use case

### Defining the algorithm

If you want to make available for example a simple moving average calculation algorithm, you will need to specify the following:

- The algorithm's `name`
- The algorithm's `description`
- The algorithm's `author`
- The algorithm's `version`
- The algorithm's `inputs`
- The algorithm's `outputs`

In the case of the moving average algorithm, the `inputs` can be the following:

- Some data:

  - The name of the input: `data`
  - The type of the input: `array`
  - The description of the input: `The data to calculate the moving average on.`

- Optionally, a parameter (the number of periods for example):
  - The name of the input: `periods`
  - The type of the input: `integer`
  - The description of the input: `The number of periods to calculate the moving average on.`

The single `output` will be the following:

- The moving average:
  - The name of the output: `moving_average`
  - The type of the output: `array`
  - The description of the output: `The moving average of the data.`

### Formatting the algorithm

To make the algorithm available, you will need to format it in a specific way by following the [Algo API](./OpenAPI/Algo_OpenAPI_V0.yaml) specifications.

#### Get /algorithms

```json
[
  {
    "id": "moving_average",
    "name": "Moving average",
    "description": "Calculate the moving average of a data.",
    "tags": ["calculations"],
    "author": "DebiAI",
    "version": "1.0.0",
    "inputs": [
      {
        "name": "data",
        "description": "The data to calculate the moving average on.",
        "type": "array",
        "arrayType": "number",
        "lengthMin": 1,
        "lengthMax": 100000
      },
      {
        "name": "periods",
        "description": "The number of periods to calculate the moving average on.",
        "type": "number",
        "default": 3,
        "min": 1,
        "max": 100
      }
    ],
    "outputs": [
      {
        "name": "moving_average",
        "description": "The moving average of the data.
                        The results length will be the length of the data",
        "type": "array",
        "arrayType": "number",
      }
    ]
  }
]
```

This will make the algorithm easily available to the program with the other algorithms.

#### Post /algorithms/{id}

The `id` of the algorithm is the same as the `id` you specified in the `GET /algorithms` endpoint.
You will receive an input that correspond to the `inputs` you specified in the `GET /algorithms` endpoint.
In the case of the moving average algorithm, you will receive an input in the following format:

```json
{
  "inputs": [
    {
      "name": "data",
      "value": [1, 2, 3, 4, 5, ...]
    },
    {
      "name": "periods",
      "value": 10
    }
  ],
}
```

After you have calculated the moving average, you will need to return the output in the following format:

```json
{
  "outputs": [
    {
      "name": "moving_average",
      "value": [1.1, 1.2, 1.3, 1.4, 1.5, ...]
    }
  ]
}
```

If the algorithm fails, you can return an error in the following format:

```json
{
  "error": {
    "code": "string",
    "message": "string"
  }
}
```
