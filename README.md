## Introduction
The [image processing components](https://home-assistant.io/components/image_processing/) currently (v 0.65) available within home-assistant can be split into two categories:

1. Cloud: components which use a cloud service, accessed via a REST API (e.g. Microsoft, OpenALPR Cloud)
2. Local with dependencies: components which run locally but require the user to install an extra image processing package (e.g. dblib, openCV)

Using either of these two categories of components presents a set of compromises.

**Cloud** For the cloud based components, it is necessary to setup authentication (often tricky), processing time depends on the speed of the cloud service and network performance, the free tier services typically allow a limited number of image processing requests. On the other hand the image processing and service maintenance is handled by an external provider, and there are no hardware requirements.

**Local with dependencies** The local components require the user to manually install an image processing package, and this may not be straightforward. For example, installing openCV on a raspberry pi can take a long time and require a level of user experience. On the other hand, all processing takes place locally so there is no dependence on an external provider or sensitivity to network performance.

## Solution: a local API rest API
In my view, it is preferable to combine the best features of both approaches, by using a local REST API. For example, [this post](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html) describes how to run a local REST API to perform object recognition using a [model](https://github.com/fchollet/deep-learning-models/blob/master/resnet50.py) that has been trained on the [image-net](http://www.image-net.org/) library. The user runs a local Flask server, and performs image processing by posting images to the server using a simple REST API. This image processing server could be deployed as a Hassio add-on, and indeed the home-assistant developer docs give an example of deploying a simple server [here](https://home-assistant.io/developers/hassio/addon_tutorial/). I don't yet know how fast image processing can be performed on a pi as a Hassio add-on, but will soon test. For the development of this custom component, I will run the image processing server on my MAC.

## machinebox.io
[machinebox.io](https://machinebox.io/) are machine learning models bundled in a Docker image and exposed via a local rest API. The [Tagbox](https://machinebox.io/docs/tagbox/recognizing-images) model can be used to classify images. I am running Docker on my [Synology DS216+II](https://www.amazon.co.uk/Synology-DS218-Bay-Desktop-Enclosure/dp/B075L82DP1/ref=pd_lpo_vtph_147_bs_t_1?_encoding=UTF8&psc=1&refRID=S07X2DD6H9G1ZFV39VDE) with [8GB RAM](https://www.amazon.co.uk/gp/product/B008PK5RSW/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) (classification time approx 6 seconds) whilst Home-Assistant is running on a raspberry pi using [Hassio](https://home-assistant.io/hassio/). My camera is a simple [USB webcam](https://www.amazon.co.uk/gp/product/B000Q3VECE/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1).

To use this component with machinebox.io, on your machine with Docker (Synology in my case), first set your credentials using `MB_KEY="you_key"`. Next run the [tagbox container](https://machinebox.io/docs/tagbox) with `docker run -p 8080:8080 -e "MB_KEY=$MB_KEY" machinebox/tagbox`.

Next add the following to your Home-Assistant config (on my pi):
```yaml
image_processing:
  - platform: rest_api
    name: general_classifier
    url: http://localhost:8080/tagbox/check
    source:
      - entity_id: camera.local_file
    concepts:
      - Dog # make case insensitive
      - Pet
```

<p align="center">
<img src="https://github.com/robmarkcole/HASS-rest-image-process/blob/master/images/HA_view.png" width="700">
</p>
