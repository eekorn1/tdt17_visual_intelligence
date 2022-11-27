"""
Script for converting pascal VOC-formated annotations to the format expected by YOLOv5
"""
import xml.etree.ElementTree as ET
import os

CLASSES = {
    "D00": 0,
    "D10": 1,
    "D20": 2,
    "D40": 3
}

def convert(path, target_path):
    tree = ET.parse(path)
    root = tree.getroot()
    size = root.find("size")
    im_width = float(size.find("width").text)
    im_height = float(size.find("height").text)
    
    empty = True
    with open(target_path, "w") as f:
        for obj in root.findall("object"):
            empty = False
            cla = CLASSES[obj.find("name").text]
            bndbox = obj.find("bndbox")

            x_min = float(bndbox.find("xmin").text) / im_width
            y_min = float(bndbox.find("ymin").text) / im_height
            x_max = float(bndbox.find("xmax").text) / im_width
            y_max = float(bndbox.find("ymax").text) / im_height

            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2

            width = x_max - x_min
            height = y_max - y_min

            f.write(f"{cla} {x_center} {y_center} {width} {height}\n")
    
    return empty


if __name__ == "__main__":
    base_path = "./datasets/Norway/train/annotations/xmls/"
    base_target_path = "./datasets/Norway/train/annotations/txts/"
    files = list(sorted(os.listdir(base_path)))
    empty = 0
    for file in files:
        path = base_path + file
        target_path = base_target_path + file.split(".")[0] + ".txt"
        emp = convert(path, target_path)
        if emp:
            empty += 1
    
    print(empty)