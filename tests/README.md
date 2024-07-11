# Compliance Tests, does this service comply with the Algo API spec?

First, you need to install the dependencies:

```bash
pip3 install pytest
```

Then, make sure that the server is running and that you can access it.

Then, you can run the tests with the following command:

```bash
cd tests
pytest
```

The tests will try to test the different algorithms provided by the service by looking at their inputs and outputs and by trying to run them with fake data.

Those tests are not exhaustive and are only here to help you to make sure that your service is compliant with the Algo API spec.

The tests won't be able to test the real behavior of your algorithms, they will only test the inputs and outputs of your algorithms.

## Specific tests

If you want to add specific tests for an algorithm, you can create a new file in the `algorithms_specific_tests` directory with the following name and add it to the `ALGORITHMS_SPECIFIC_TESTS` dictionary in the `test_algo_api_compliance.py` file.

```python
from algorithms_specific_tests import objectDetectionMetricsTests

ALGORITHMS_SPECIFIC_TESTS = {
    "ObjectsDetectionMetrics": objectDetectionMetricsTests.test_object_detection_metrics_algorithm
}
```
