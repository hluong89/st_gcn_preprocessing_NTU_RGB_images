# Given RGB videos with the filename in the format of NTU dataset (e.g., S004C001P003R001A017_rgb), this Python script
# reads NTU_RGB video and slips dataset into training and testing in the format of Kinetics dataset.
# The format is as follows
# 1 json file for training set. Format: {}
# 1 json file for testing set
# 1 folder for training set
# 1 folder for testing set

import os
import json

#ntu_RGB_video_dir = "/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/hien_data/ntu/nturgb+d_rgb"
#ntu_RGB_video_dir = "data_testing"
ntu_RGB_video_dir = "/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/hien_data/ntu/nturgb+d_rgb"

kinetics_dataset_dir = "kinetics_dataset"

# Note: also change in the convert_RGB_images_into_skeleton_info_based_on_openpose

training_cameras = [2, 3]

max_frame = 300
max_body = 2
num_joint = 18

# label index and label name
action = {'1': 'drink water', '2': 'eat meal/snack', '3': 'brushing teeth', '4': 'brushing hair', '5': 'drop',
          '6':'pickup', '7':'throw', '8':'sitting down', '9':'standing up', '10': 'clapping',
          '11': 'reading', '12': 'writing', '13': 'tear up paper', '14':'wear jacket', '15':'take off jacket',
          '16':'wear a shoe', '17':'take off a shoe', '18': 'wear on glasses', '19': 'take off glasses', '20':'put on a hat/cap',
          '21': 'take off a hat/cap', '22': 'cheer up', '23': 'hand waving', '24':'kicking something', '25':'put something inside pocket ',
          '26':'hopping (one foot jumping)', '27':'jump up', '28': 'make a phone call/answer phone', '29': 'playing with phone/tablet', '30':'typing on a keyboard',
          '31': 'pointing to something with finger', '32': 'taking a selfie', '33': 'check time (from watch)', '34':'rub two hands together', '35':'nod head/bow',
          '36':'shake head', '37':'wipe face', '38': 'salute', '39':'put the palms together' , '40':'cross hands in front (say stop)',
          '41': 'sneeze/cough', '42': 'staggering', '43': 'falling', '44': 'touch head (headache)', '45': 'touch chest (stomachache/heart pain)',
          '46': 'touch back (backache)', '47': 'touch neck (neckache)', '48': 'nausea or vomiting condition', '49': 'use a fan (with hand or paper)/feeling warm', '50': 'punching/slapping other person',
          '51': 'kicking other person', '52': 'pushing other person', '53': 'pat on back of other person', '54': 'point finger at the other person', '55': 'hugging other person',
          '56': 'giving something to other person', '57': 'touch other person\'s pocket', '58': 'handshaking', '59': 'walking towards each other', '60': 'walking apart from each other'}

# list all video files in the folder
all_file_name_list = os.listdir(ntu_RGB_video_dir)
print(len(all_file_name_list), all_file_name_list)
video_name_list = [all_file_name_list[i] for i in range(len(all_file_name_list)) if all_file_name_list[i].endswith('avi')]
print(len(video_name_list), video_name_list)

training_list = []
testing_list = []

def split_training_and_testing(video_list):
    # this function slips training and testing dataset based on the filename.
    # camera 1 for tesing (e.g., C001), cameras 2 and 3 for training (e.g., C002 and C003)
    for i in range(len(video_list)):
        camera_id = video_list[i].split('P')[0][-1]
        print(camera_id, video_list[i])
        if int(camera_id) in training_cameras:
            training_list.append(video_list[i])
        else:
            testing_list.append(video_list[i])


def write_json_file(video_list, filename):
    with open(filename, 'w') as write_file:
        # for each filename, write the filename, label name, and label number in the json file
        data = {}
        for i in range(len(video_list)):
            filename = video_list[i].split('.')[0]
            label_index = int(video_list[i].split('_')[0].split('A')[1])
            label =  action[str(label_index)]
            #print(label)
            # data +=  filename + "\": {" + "\"has_skeleton\": true," + "\"label\": " + "\"" + label + "\"," + "\"label_index\":" + str(label_index) + "}"
            # if i != len(video_training_list) -1:
            #     data += ','
            # write data as a dictionary
            file_data = {}
            file_data['has_skeleton'] = True
            file_data['label'] = label
            file_data['label_index'] = label_index
            data[filename] = file_data
        print(type(data), data)
        json.dump(data, write_file)

    # with open('target.json','r') as target_file:
    #     data_string = json.load(target_file)
    # print(type(data_string), data_string)

split_training_and_testing(video_name_list)
print(len(training_list), training_list)
print(len(testing_list), testing_list)

train_file_dir = os.path.join(ntu_RGB_video_dir, 'kinetics_train_label.json')
write_json_file(training_list,train_file_dir)
val_file_dir = os.path.join(ntu_RGB_video_dir, 'kinetics_val_label.json')
write_json_file(testing_list, val_file_dir)