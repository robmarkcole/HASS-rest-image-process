## Introduction
The [image processing components](https://home-assistant.io/components/image_processing/) currently (v 0.62) available within home-assistant can be split into two categories:

1. Cloud: components which use a cloud service, accessed via a REST API (e.g. Microsoft, OpenALPR Cloud)
2. Local with dependencies: components which run locally but require the user to install an extra image processing package (e.g. dblib, openCV)

Using either of these two categories of components presents a set of compromises.

**Cloud** For the cloud based components, it is necessary to setup authentication (often tricky), processing time depends on the speed of the cloud service and network performance, the free tier services typically allow a limited number of image processing requests. On the other hand the image processing and service maintenance is handled by an external provider, and there are no hardware requirements.

**Local with dependencies** The local components require the user to manually install an image processing package, and this may not be straightforward. For example, installing openCV on a raspberry pi can take a long time and require a level of user experience. On the other hand, all processing takes place locally so there is no dependence on an external provider or sensitivity to network performance.

## Solution: a local API via Hassio add-on
In my view, it is preferable to combine the best features of both approaches, by using a local REST API. For example, [this post](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html) describes how to run a local REST API to perform object recognition using a [model](https://github.com/fchollet/deep-learning-models/blob/master/resnet50.py) that has been trained on the [image-net](http://www.image-net.org/) library. The user runs a local Flask server, and performs image processing by posting images to the server using a simple REST API. This image processing server could be deployed as a Hassio add-on, and indeed the home-assistant developer docs give an example of deploying a simple server [here](https://home-assistant.io/developers/hassio/addon_tutorial/). I don't yet know how fast image processing can be performed on a pi as a Hassio add-on, but will soon test. For the development of this custom component, I will run the image processing server on my MAC.

## This custom component
This custom component will simply perform the work of the example script [simple_request.py](https://github.com/jrosebr1/simple-keras-rest-api/blob/master/simple_request.py) (editied version shown below). The component wraps this script up as an image processing component that can be configured to process images captured by a configured home-assistant camera.
```python
simple_request.py

# import the necessary packages
import requests

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:5000/predict"
IMAGE_PATH = "dog.jpg"

# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()
payload = {"image": image}

# submit the request
response = requests.post(KERAS_REST_API_URL, files=payload).json()

# ensure the request was sucessful
if response["success"]:
	# loop over the predictions and display them
	for (i, result) in enumerate(response["predictions"]):
		print("{}. {}: {:.4f}".format(i + 1, result["label"],
			result["probability"]))

# otherwise, the request failed
else:
	print("Request failed")
  ```

  To run the image processing server, follow [the instructions to install here](https://github.com/jrosebr1/simple-keras-rest-api#) and start the server with ```python run_keras_server.py```
