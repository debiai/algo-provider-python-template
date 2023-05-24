# ===================================================
# This project is a ready to fill template for an algo-provider service.
# This service follows the Algo API standard.
# More informations in the algo-api/README.md file.
#
# Define your algorithms inputs and outputs,
# and the algorithm itself in the algorithms/algorithms.py file.
#
# Service name: Algo-provider Python Template
# Authors: DebiAI
# Github: https://github.com/debiai/algo-provider-python-template
# License: Apache License 2.0
# ===================================================

import connexion
from flask_cors import CORS
from init import init
from utils.utils import get_app_version

PORT = 3020
OPEN_API_PATH = "algo-api/OpenAPI/Algo_OpenAPI_V0.yaml"

# Setup app
app = connexion.App(__name__)
app.add_api(OPEN_API_PATH, strict_validation=True)
CORS(app.app)

if __name__ == "__main__":
    # Run the service
    print(
        "================ My Algo Service "
        + get_app_version()
        + " ===================="
    )
    init()
    print("============================ RUN ===========================")
    print("App running : http://localhost:{}".format(PORT))
    print("Swagger UI : http://localhost:{}/ui/".format(PORT))
    app.run(port=PORT, debug=True)
