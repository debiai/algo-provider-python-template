# Supported types

The Algo API supports the following types for the inputs and outputs:

## string

```json
{
  "type": "string"
}
```

You can specify those optional parameters:

```json
{
  "type": "string",
  "availableValues": ["string"],
  "default": "string"
}
```

## number

```json
{
  "type": "number"
}
```

You can specify those optional parameters:

```json
{
  "type": "string",
  "availableValues": ["number"],
  "default": "number",
  "min": "number",
  "max": "number"
}
```

## boolean

```json
{
  "type": "boolean"
}
```

You can specify an optional default value:

```json
{
  "type": "boolean",
  "default": "boolean"
}
```

## array

When you specify an array, you need to specify the type of the array's elements.
The available types are:

- string
- number
- boolean
- dict
- array

```json
{
  "type": "array",
  "arrayType": "string"
}
```

You can specify those optional parameters:

```json
{
  "type": "array",
  "arrayType": "string",
  "lengthMin": "number",
  "lengthMax": "number"
}
```

Back to the [Algo API](README.md) page.
