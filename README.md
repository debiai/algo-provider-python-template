# Algo-provider Python template

<div align="center" style="background:white; border-radius:20px">
  <img src="logo.png" width="200" height="200">
</div>
<br>

This project is a ready to fill algo-provider template

It exposes some simple addition and multiplication algorithms as an example.

## Algo API

To make your algorithm compatible with DebiAI, you need to follow the Algo API standard, more informations on [the Algo API here](./algo-api/README.md).

This template is already compatible with the Algo API and is ready to be used.

## How to use

Setup the project with the following command:

```bash
git clone https://github.com/debiai/algo-provider-python-template.git
```

Install the dependencies and the submodules with the following commands:

```bash
pip install -r requirements.txt
```

Define your algorithms inputs and outputs, and the algorithm itself in the algorithms/algorithms.py file.

Then, you can run the server with the following command:

```bash
python websrv.py
```

## Config

This template comes with a config file template that you can use to configure the server. You can find it in the config/config.ini file.

To add elements to the config file, you will need to add them in the config/config.ini file and in the config/init_config.py file.

## Testing

This template comes with some tests to help you to make sure that your service is compliant with the API.

The tests will try to test the diffent algorithms provided by the service by looking at their inputs and outputs and by trying to run them with fake data.

Those tests are not exhaustive and are only here to help you to make sure that your service is compliant with the API spec.

The tests won't be able to test the real behaviour of your algorithms, they will only test the inputs and outputs of your algorithms.

[MORE INFO ON THE TESTS HERE](tests/README.md)

# Deployment

To help you to deploy this service, this template comes with a Dockerfile.

## Docker local deployment

To build the Docker image locally, you can use the following commands:

```bash
# First, download your project
git clone https://github.com/debiai/algo-provider-python-template.git
cd algo-provider-python-template

# Then, build the Docker image
docker build -t algo-provider-python-template .
```

Then, you can run the Docker image with the following command:

```bash
docker run -p 3020:3020 algo-provider-python-template
```

Make sure to adapt the project and image name to your algo-provider.

You can then manually push the image to the registry with the following command:

# Need help?

Let us know if you need help with this template by opening an issue on this repository.
