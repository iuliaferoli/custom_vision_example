import json
import random
import os
import operator

from cropping import crop_img, process_image
from custom_vision import detect_coils, classify_coils, add_classification_images, add_detection_images


#use as a patch to deal with the new folder structure,
# need to change the way we deal with the path in each function then delete this or move to archive
def get_proper_name(file_name):
    import os
    script_dir = os.path.dirname(__file__)
    rel_path = "data/" + file_name
    path = os.path.join(script_dir, rel_path)
    return path


#from the list of coils detected in the image - pick the "right one"
#currently taking the one most at the bottom - must be changed in the future / depending on case
# @refactor - make the way we pick the top coil a parameter that can be changed
def get_top_coil(coordinates):
    index, _ = max(enumerate([el.bounding_box.top for el in coordinates]), key=operator.itemgetter(1))
    return coordinates[index].bounding_box

#get the top score/probability for the classification - is it positive or negative?
def get_top_prob(response):
    index, _ = max(enumerate([el["probability"] for el in response]), key=operator.itemgetter(1))
    return response[index]['tagName']

#only return damages if probability is higher than threshold (replace above function)
def get_prediction_label(response, threshold):
    damages_probability = [item for item in response if item['tagName'] == 'damages'][0]['probability']
    return 'damages' if damages_probability > threshold else 'Negative'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#these labels need to be standardized in the projects so this shouldn't be exist
#it's because we get the labels from the folder names and they are not the same as the labels in the project
# - fix either one then remove function from code
# @refactor
def fix_label(name):
    if name == "Transport damage":
        return "damages"
    if name == "No transport damage":
        return "Negative"
    else:
        return "wrong"

#save_as - boolean if we want to update the json file
def get_detections(buffer, save_as, project_id, published_name, img_list):
    results = []
    for image in img_list:
        result = {}
        camera_name = "_".join(image["name"].split("_", 2)[:2])
        coordinates = detect_coils(image["url"], project_id, published_name)
        if coordinates != []:
            coord = get_top_coil(coordinates)
            intermediary = crop_img(image["url"], coord, buffer)
            cropped_image = intermediary[0]
            coord = intermediary[1]
            if cropped_image != []:
                result["camera_name"] = camera_name
                result["coordinates"] = coord
                result["coil_id"] = image["name"].split("_")[-1].split(".")[0]
                result["url"] = image["url"]
                result["label"] = fix_label(image["url"].split("/")[-2])
                results.append(result)
    if save_as != "":
        with open(save_as, 'w') as fp:
            json.dump(results, fp)
    return results



#if we run with less than the entire data set
def get_sample(overview, sample_size):
    sorted_sample = [
        overview[i] for i in random.sample(range(len(overview)), sample_size)
    ]
    return sorted_sample


#merged should be a json in our standard format
def send_to_training_detection(merged, project_id, buffer):
    for sample in merged:
        intermediary = process_image(sample["url"], sample["coordinates"], buffer)
        add_detection_images(intermediary[0], intermediary[1], project_id)


#send all images of label to the project as training data (to be tagged manualy)
def send_to_training_classification(overview, project_id):
    for image in overview:
        #buffer here is 0 since I'm getting the coordinates from the json that have already been buffed
        intermediary = crop_img(image["url"], image["coordinates"], 0)
        add_classification_images(intermediary[0], image["label"], project_id)


#go though our result json and update when we have new results/prediction (so we don't re-run the detection when we're just updating the classifier)
def get_classifications(overview, save_as, threshold, project_id, published_name):
    results = []
    for image in overview:
        intermediary = crop_img(image["url"], image["coordinates"], 0)
        cropped_image = intermediary[0]
        coord = intermediary[1]
        if cropped_image != []:
            # @refactor change here once the classificaiton is done with the SDK instead of API
            classifications = classify_coils(cropped_image, project_id, published_name)
            image["prediction"] = get_prediction_label(classifications, threshold)
            results.append(image)
    if save_as != "":
        with open(save_as, 'w') as fp:
            json.dump(results, fp)
    return results