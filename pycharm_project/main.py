import sys
import json
import os

from stream_and_process import send_to_training_classification, send_to_training_detection, get_detections, get_classifications
from new_input import extract_imported_json, extract_imported_txt, merge
from run_analysis import compute_stats
from img_urls import all_images

ENV_SETTINGS = json.load(open('./env_settings.json'))


detected_coils_file = os.path.join(ENV_SETTINGS['FILE_LOCATIONS']['DATA_FOLDER'],
                                   ENV_SETTINGS['FILE_LOCATIONS']['SAVED_DETECTED_COILS'])
classified_coils_file = os.path.join(ENV_SETTINGS['FILE_LOCATIONS']['DATA_FOLDER'],
                                     ENV_SETTINGS['FILE_LOCATIONS']['SAVED_CLASSIFIED_COILS'])
new_data_file = os.path.join(ENV_SETTINGS['FILE_LOCATIONS']['DATA_FOLDER'],
                             ENV_SETTINGS['FILE_LOCATIONS']["NEW_DATA"])

detection_model = ENV_SETTINGS['DETECTION_MODEL']
classification_model = ENV_SETTINGS["CLASSIFICATION_MODEL"]


def run(detection = True, classification = True, statistics = True):
    if detection:
        img_list = all_images(camera_name="")
        detected_coils = get_detections(
            buffer = ENV_SETTINGS['MODEL_PARAMETERS']['BUFFER'],
            save_as = detected_coils_file,
            project_id = detection_model["PROJECT_ID"],
            published_name = detection_model["PUBLISHED_NAME"],
            img_list = img_list
        )
    else:
        with open(detected_coils_file) as infile:
            detected_coils = json.load(infile)
    #if we don't re-run the detection we can read the previous detectin results from file for the next step

    if classification:
        classified_coils = get_classifications(
                                overview = detected_coils,
                                save_as = classified_coils_file,
                                project_id = classification_model["PROJECT_ID"],
                                published_name= classification_model["PUBLISHED_NAME"],
                                threshold=ENV_SETTINGS['MODEL_PARAMETERS']['THRESHOLD']
                            )
    else:
        with open(classified_coils_file) as infile:
            classified_coils = json.load(infile)

    if statistics:
        stats = compute_stats(classified_coils, ENV_SETTINGS['MODEL_PARAMETERS']['CAMERA_NAMES'])
        with open( ENV_SETTINGS['FILE_LOCATIONS']['SAVED_STATS'], 'w') as fp:
            json.dump(stats, fp)


def run_training(new_data_format = "json", detection = True, classification = True):
    if new_data_format == "json":
        new_data = extract_imported_json(new_data_file)
    elif new_data_format == "txt":
        new_data = extract_imported_txt(new_data_file)
    else:
        print("wrong new data input")
        return 0
    # call to update the blob storage and merge the data with the urls then we can do the next steps:

    # for testing:
    new_data = json.load(open(os.path.join(ENV_SETTINGS['FILE_LOCATIONS']['DATA_FOLDER'], "template.json")))

    with open(detected_coils_file) as infile:
        detected_coils = json.load(infile)

    #this step adds the urls to the new data
    new_data = merge(detected_coils, new_data)

    if detection:
        send_to_training_detection(new_data, detection_model['PROJECT_ID'], ENV_SETTINGS['MODEL_PARAMETERS']['BUFFER'])
        print("Training detection successfully finished!")
    if classification:
        send_to_training_classification(new_data, ENV_SETTINGS['CLASSIFICATION_MODEL']['PROJECT_ID'])
        print("Training classifier successfully finished!")


if __name__ == "__main__":
    if(sys.argv[1] == "train"):
        print("Starting with training of the classifier...")
        run_training(detection=False)
    
    elif(sys.argv[1] == "traindetection"):
        run_training()

    elif(sys.argv[1] == "classify"):
        run()

    else:
        print("Specify train or classify")
