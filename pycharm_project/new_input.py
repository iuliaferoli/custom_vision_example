#In this file we can have functions that deal with getting new input:
#converting from excel or csv or non-standard format to our json structure and saving that file to be used
#checking if any new pictures need to be saved to the blob storage
#putting those images in the blob storage

#run this when we get new input, run to update files&blob storage, when finished we can run the rest of the code
import json

#read the new file sent by Benjamin and create the json in our correct format (we were given file name and coodinates)
#return the list of dictionaries
def extract_imported_txt(path):
    imported = []
    with open(path) as infile:
        for row in infile:
            entry = {}
            camera, coord = row.strip("\n").split(";")
            camera_name = "_".join(camera.split("_", 2)[:2])
            entry["camera_name"] = camera_name
            entry["coil_id"] = camera.split("_")[-1].split(".")[0]
            entry["coordinates"] = [int(el) for el in coord[1:-1].split(",")]
            #entry["original_name"] = camera
            imported.append(entry)
    return imported

def extract_imported_json(path):
    with open(path) as infile:
        new_data = json.load(infile)
    return new_data

#check if any of the new imported ids are not already saved in the blob storage
# (by comparing with the IDs already in the result json files rather than calling to the blob directly
def find_new_ids(new_data, old_data):
    ids = [row["coil_id"] for row in old_data]
    exceptions = []
    for line in new_data:
        if line["coil_id"] not in ids:
            exceptions.append(line)
    return exceptions

   ##########################
    #Then should...
    #update blob storage with the images in the exception list (not done automatically at the moment
    # from blob storage i get the URLs and from imported I get the coordinates, then combine the information (url_data)
    #then we merge them
    ##############################

def merge(url_data, new_data):
    merged = []
    for element in url_data:
        element["coil_id"] = element["name"].split("_")[-1].split(".")[0]
        element["camera_name"] = "_".join(element["name"].split("_", 2)[:2])
        for other_element in new_data:
            if (other_element["coil_id"] == element["coil_id"]) and (
                    other_element["camera_name"] == element["camera_name"]):
                new_element = {**element, **other_element}
                merged.append(new_element)
                break
    return merged

