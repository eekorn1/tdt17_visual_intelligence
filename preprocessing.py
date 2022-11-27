"""
Script for preprocessing the data
"""

import os
import random
import shutil

base_path = "data_norway/Norway/train/"
target_base_path = "datasets/norway_drop_empty/"

im = base_path + "images/"
label = base_path + "annotations/txts/"

target_im = target_base_path + "images/"
target_label = target_base_path + "labels/"

ims = list(sorted(os.listdir(im)))
labels = list(sorted(os.listdir(label)))

random_drop_prob = 0.7

empty = 0

cats = {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0
}
indicies = []
i = 0
for l in labels:
    with open(label + l, "r") as f:
        emp = True
        for line in f.readlines():
            cat = line.split(" ")[0]
            cats[cat] += 1
            emp = False
        
    if emp:
        if random.random() > random_drop_prob:
            empty += 1
            indicies.append(i)
    
    else:
        indicies.append(i)
    
    i +=1



random.shuffle(indicies)

train_size = int(0.85*len(indicies))
val_size = len(indicies) - train_size


train_ims = []
train_labels = []

for i in indicies[:train_size]:
    train_ims.append(ims[i])
    train_labels.append(labels[i])


val_ims = []
val_labels = []
for i in indicies[train_size:train_size+val_size]:
    val_ims.append(ims[i])
    val_labels.append(labels[i])    


for i in range(train_size):
    shutil.copyfile(im + train_ims[i], target_im + "train/" + train_ims[i])
    shutil.copyfile(label + train_labels[i], target_label + "train/" + train_labels[i])
    
for i in range(val_size):
    shutil.copyfile(im + val_ims[i], target_im + "val/" + val_ims[i])
    shutil.copyfile(label + val_labels[i], target_label + "val/" + val_labels[i])
