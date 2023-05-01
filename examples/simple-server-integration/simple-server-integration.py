from printwatch.client import PrintWatch
from flask import Flask

app = Flask(__name__)

@app.route('/inference')
def inference():
    # Create Client object
    # Insert the global api key for your organization/cloud platform
    # create default payload. In production, forward info from request
    client = PrintWatch("INSERT_API_KEY")

    # Get the image from the request.
    image = request.get_json().get("image")

    # Run the inference synchronously.
    response = client.infer(image)

    # Post-process the response according to what is required by
    # your organization's requirements


    return response

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
