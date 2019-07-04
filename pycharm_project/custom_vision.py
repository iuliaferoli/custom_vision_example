import json
import cv2
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

ENV_SETTINGS = json.load(open('./env_settings.json'))

trainer = CustomVisionTrainingClient(ENV_SETTINGS['TRAINING_KEY'], endpoint=ENV_SETTINGS['ENDPOINT'])
predictor = CustomVisionPredictionClient(ENV_SETTINGS['PREDICTION_KEY'], endpoint=ENV_SETTINGS['ENDPOINT'])


# detect coil in one image with project_id detector
# change the name of the published iteration with a parameter @refactor
def detect_coils(img_url, project_id, published_name):
    try:
        result = predictor.detect_image_url_with_no_store(project_id, published_name, img_url)
        return result.predictions
    except:
        print("error with coil detection " + img_url)
        return([])


# add an image to training (with tag)
def add_detection_images(image, coordinates, project_id):
    ret, buf = cv2.imencode('.jpg', image)
    tag_id = trainer.get_tags(project_id)[0].id
    region = Region(tag_id=tag_id, left=coordinates[0],top=coordinates[1],width=coordinates[2],height=coordinates[3])
    img = ImageFileCreateEntry(name="test", contents=buf.tobytes(), regions=[region], tag_ids=[tag_id])
    return trainer.create_images_from_files(project_id, images=[img])


def classify_coils(cropped_img, project_id, published_name):
    try:
        result = predictor.classify_image(project_id, published_name, cropped_img)
        return(result.predictions)
    except:
        print("error with coil classification ")
        return([])


# training function for the classification
# TODO: error handling if tag name is not found
def add_classification_images(image, my_tag, project_id):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,buf = cv2.imencode('.jpg', image)
    all_tags = trainer.get_tags(project_id)
    tag_id = [tag for tag in all_tags if tag.name == my_tag][0]
    img = ImageFileCreateEntry(name="test", contents=buf.tobytes(), tag_ids=[tag_id])
    result = trainer.create_images_from_files(project_id, images = [img])
    return(result)