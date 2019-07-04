## Installation
- install the packages from requirements
- create your custom vision projects and get all the necessary infromation
- copy env_settings_example.json and fill in the CHANGEME variables
- run the flask app (next section)


## Run flask app (for visualising the interface of the project)
In Powershell:
- Navigate to project folder
- $env:FLASK_APP = "webservice.py"
- Flask run

In browser:
- Go to http://localhost:5000


## Code overview of files/scripts (where to find what)
 - To run everything (send training images, get predictions, get statistics) - main
 - All parameters you need to fill in - all_parameters - TO DO add all the links to your projects here before running
 - Process new input (labeled images for example) - new_input
  	- templates/template example for the input
 - Connections between code and custom vision projects (https://www.customvision.ai) - custom_vision_api
 - Funcitons for training/running - steam_and_process
 - Getting the data from a blob storage - img_urls
 - Showing the results on a web app - show_images
 - Run statistics - run_analysis
 - showcases the results/steps via a Web App - webservices


## Pipeline (the steps the code takes)
- takes in raw images from the cameras (images that we uploaded to the blob storage, with initial information we have from given labels - either coordinates for the detection task, or damanged/not damaged labels for the classification task)
- detects the coils; and selects the most likely one if there are multiple
- crops the coil with a buffer around the detection frame (wider crop to ensure edges are included)
- classifies the coil and returns a prediction
- calculates statistics over entire data set
