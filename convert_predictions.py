"""
Script for converting the predicted bounding boxes to pascal VOC format.
"""

from PIL import Image
import os

CLASSES = {
    "0": "1",
    "1": "2",
    "2": "3",
    "3": "4"
}

def choose_objects(objs):
    res = []
    labels = []
    for obj in objs:
        labels.append(obj[0])
    seen = set()
    chosen = []
    for i, label in enumerate(labels):
        if label not in seen:
            seen.add(label)
            chosen.append(i)
    
    i = 0
    while len(chosen) < 5:
        if i not in chosen:
            chosen.append(i)
        i += 1
    for i in chosen:
        res.append(objs[i])
    
    return res


    


labels_dir = "./labels"
img_dir = "./datasets/Norway/test/images"

for file in os.listdir(img_dir):
    name = file.split(".")[0]
    line = f"{file},"
    if f"{name}.txt" in os.listdir(labels_dir):
        img = Image.open(os.path.join(img_dir, file))
        w = img.width
        h = img.height
        with open(os.path.join(labels_dir, f"{name}.txt")) as f:
            objects = f.readlines()
            objects = list(map(lambda x: x.strip("\n").split(" "), objects))
            if len(objects) > 5:
                objects = choose_objects(objects)
            
            for obj in objects:
                line += f" {CLASSES[obj[0]]}"
                
                x_min = int(w*(float(obj[1]) - 0.5*float(obj[3])))
                x_max = int(w*(float(obj[1]) + 0.5*float(obj[3])))

                y_min = int(h*(float(obj[2]) - 0.5*float(obj[4])))
                y_max = int(h*(float(obj[2]) + 0.5*float(obj[4])))

                line += f" {x_min} {y_min} {x_max} {y_max}"
    
    

    with open("submission.csv", "a") as f:
        line = line.replace(" ", "", 1)
        f.write(f"\n{line}")