

# This script slips RGB video into RGB frames

import cv2
import numpy as np
import os
import json
#from json import encoder
import shutil
import time

# video_path = 'data_testing/testing_people'
# skeleton_dir =  '/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/Code/st_gcn_preprocessing_NTU_RGB_images/data_testing/testing_people/json/'

video_path = '/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/hien_data/ntu/nturgb+d_rgb'
#skeleton_dir =  '/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/Code/st_gcn_preprocessing_NTU_RGB_images/data_testing/testing_people/json/'
skeleton_dir ='/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/hien_data/ntu/ntugrb_skeleton_Folder_frames_18_03/jsonBackUp'

training_cameras = [2, 3]

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


# list all video files
all_file_list =  os.listdir(video_path)
video_file_list = [all_file_list[i] for i in range(len(all_file_list)) if all_file_list[i].endswith('.avi')]
#print(video_file_list[0])

def slip_RGB_video_into_frames(video_name, video_dir):

    folder_name = os.path.join(video_path,video_name.split('.')[0])
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    cap = cv2.VideoCapture(os.path.join(video_dir, video_name))
    ret, frame = cap.read()

    count = 0

    while ret:
        cv2.imwrite(os.path.join(folder_name, video_name.split('.')[0] + '_{}.jpg'.format(count)), frame)
        ret, frame = cap.read()
        count += 1


# list_all_folder_and_file = os.listdir(skeleton_dir)
# list_all_folder = [list_all_folder_and_file[i] for i in range(len(list_all_folder_and_file)) if
#                    os.path.isdir(os.path.join(dir, list_all_folder_and_file[i]))]
# for i in range(len(list_all_folder)):

# this script converts all json files of 1 video from openpose format into kinetics format
def convert_skeleton_multiple_json_files_of_one_video(json_dir):
    all_folder_and_file = os.listdir(json_dir)
    all_json_file = [all_folder_and_file[i] for i in range(len(all_folder_and_file)) if all_folder_and_file[i].endswith('.json')]
    json_info = {}
    data = []

    for i in range(len(all_json_file)):
        frame_info = {}
        frame_info['frame_index'] = i + 1
        fname = all_json_file[i].split('rgb')[0] + 'rgb_' + str(i) + '.json'
        #print(fname)
        fname_with_dir = os.path.join(json_dir, fname)
        skeleton = convert_skeleton_one_json_file(fname_with_dir)
        frame_info['skeleton'] = skeleton
        data.append(frame_info)
    json_info['data'] = data

    label_index = int(all_json_file[0].split('_')[0].split('A')[1])
    json_info['label_index'] = label_index
    json_info['label'] = action[str(label_index)]

    #fname_final = all_json_file[0].split('_')[0] + '.json'
    print('final name: ',json_dir, type(json_dir))
    fname_final = json_dir.split('/')[-1] + '.json'
    #fname_final = all_json_file[0].split('.')[0][0:-3] + '.json'
    print('fname_final: ', fname_final)
    time.sleep(1)
    #skeleton_final_dir = json_dir.split('')
    fname_final_dir = os.path.join(json_dir, fname_final)
    write_skeleton_info_from_one_json_file(fname_final_dir, json_info)

# write json file
def write_skeleton_info_from_one_json_file(fname, skeleton_info):
    with open(fname, 'w') as fw:
        #json.encoder.FLOAT_REPR = lambda skeleton_info: format(skeleton_info, '.3f')
        json.dump(skeleton_info, fw)


# this script converts one json file from openpose format into kinetics format
def convert_skeleton_one_json_file(json_fname):
    skeleton = {}

    score_point = 0.0
    with open(json_fname, 'r') as fr:
        joints = json.load(fr)

    multi_person_skeleton_list = []
    for joint in joints:

        person_info = {}
        pose_info = []
        score_info = []
        for i in range(18):
            joint_x, joint_y = joint['joints'][i]
            #joint_x, joint_y = str(joint_x)[0:5], str(joint_y)[0:5]
            joint_x, joint_y = round(joint_x,3), round(joint_y,3)
            if joint_x == -1:
                joint_x = 0.0
            if joint_y == -1:
                joint_y = 0.0

            pose_info.append(joint_x)
            pose_info.append(joint_y)
            score_info.append(score_point)
        person_info['pose'] = pose_info
        person_info['score'] = score_info
        multi_person_skeleton_list.append(person_info)
        # print("pose_info: ", pose_info)
        # print("score_info: ", score_info)
        # print('Multi: ', multi_person_skeleton_list)
    return multi_person_skeleton_list



# copy and split skeleton files into training and validating sets
train_skeleton_dir = '/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/Code/st_gcn_preprocessing_NTU_RGB_images/ntu_RGB_into_kinetics_dataset_preprocess/kinetics_train'
val_skeleton_dir = '/media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/Code/st_gcn_preprocessing_NTU_RGB_images/ntu_RGB_into_kinetics_dataset_preprocess/kinetics_val'

def copy_and_split_skeleton_files_into_training_and_val_sets(skeleton_all_img_dir, train_dir, val_dir):
    all_skeleton_folder_list = os.listdir(skeleton_all_img_dir)
    #print(len(all_skeleton_folder_list), all_skeleton_folder_list)
    print(len(all_skeleton_folder_list))
    for i in range(len(all_skeleton_folder_list)):


        # fname = all_skeleton_folder_list[i]
        camera_id = int(all_skeleton_folder_list[i].split('P')[0][-1])
        #print('camera: ', camera_id, all_skeleton_folder_list[i])
        fname = all_skeleton_folder_list[i] + '.json'
        print(i, '.... file name: ', fname)
        skeleton_org = os.path.join(os.path.join(skeleton_all_img_dir, all_skeleton_folder_list[i]), fname)
        if camera_id in training_cameras:
            shutil.copy(skeleton_org, train_dir)
        else:
            shutil.copy(skeleton_org, val_dir)



# Step 1:
# Point to the folder of RGB videos by changing 'video_path'
# Run this script to slip RGB videos into frames
# for i in range(len(video_file_list)):
#    slip_RGB_video_into_frames(video_file_list[i], video_path)

# Step 2: In openpose, run easy_run_openpose_forRGB.py to convert RGB frames into skeleton json file
# Location of file: /media/hien/b606dd41-ce02-4d1c-a14c-e0f67858c948/Code/poseestimation/tf_pose
# change 'dir' variable. dir = video_path above

# Step 3:
# Change 'skeleton_dir' to the skeleton folder
# Run this script to convert skeleton infomation (from step 2) into the final format
# list all video files
#
# all_skeleton_folder_list =  os.listdir(skeleton_dir)
#
# for i in range(len(all_skeleton_folder_list)):
#    # skeleton_dir = os.path.join(video_path, video_file_list[i].split('.')[0])
#    # print(skeleton_dir, type(skeleton_dir))
#    skeleton_dir_for_one_video = os.path.join(skeleton_dir, all_skeleton_folder_list[i])
#    print('skeleton for one video', skeleton_dir_for_one_video)
#    convert_skeleton_multiple_json_files_of_one_video(skeleton_dir_for_one_video)

# Step 4: split the skeleton information of video into training and validating sets which is consistent with the training
# and validating set files
copy_and_split_skeleton_files_into_training_and_val_sets(skeleton_dir, train_skeleton_dir, val_skeleton_dir)
