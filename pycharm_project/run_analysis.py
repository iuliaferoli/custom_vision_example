#input overview is the json with our results
#cameras are the camera names - should be in different file we get the names from
# @refactor
def get_stats(overview, cameras):
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    for image in overview:
        if image["camera_name"] in cameras:
            if image["prediction"] == "damages":
                if image["label"] == "damages":
                    true_positives += 1
                elif image["label"] == "Negative":
                    false_positives += 1
            elif image["prediction"] == "Negative":
                if image["label"] == "Negative":
                    true_negatives += 1
                elif image["label"] == "damages":
                    false_negatives += 1
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)
    return [precision, recall, accuracy, true_positives, true_negatives, false_positives, false_negatives]

def compute_stats(overview, cameras):

    per_cameras = {}
    per_cameras["all"] = get_stats(overview, cameras)

    for camera in cameras:
        per_cameras[camera] = get_stats(overview, [camera])

    return per_cameras

