import argparse
import json
import os
from pathlib import Path

DIRECTORY_OUTPUT: str = "./output"


def convert(coco_annotations_file: str, consider_supercategory: bool):
    if not Path(coco_annotations_file).exists():
        print(f"File \"{coco_annotations_file}\" not found.")
        return

    with open(file=coco_annotations_file, mode="r") as file:
        coco_annotations = json.load(fp=file)

        categories = {}
        for category in coco_annotations["categories"]:
            categories[category["id"]] = category["supercategory"] if consider_supercategory else category["name"]

        images = {}
        for image in coco_annotations["images"]:
            images[image["id"]] = {
                "file_name": image["file_name"],
                "height": image["height"],
                "width": image["width"]
            }

        anylabeling_annotations = {}
        for annotation in coco_annotations["annotations"]:
            if anylabeling_annotations.get(annotation["image_id"]) is None:
                anylabeling_annotations[annotation["image_id"]] = {
                    "version": "0.3.3",
                    "flags": {},
                    "shapes": [],
                    "imagePath": images[annotation["image_id"]]["file_name"],
                    "imageData": None,
                    "imageHeight": images[annotation["image_id"]]["height"],
                    "imageWidth": images[annotation["image_id"]]["width"]
                }
            anylabeling_annotations[annotation["image_id"]]["shapes"].append({
                "label": categories[annotation["category_id"]],
                "text": "",
                "points": [
                    [
                        annotation["bbox"][0],
                        annotation["bbox"][1],
                    ],
                    [
                        annotation["bbox"][0] + annotation["bbox"][2],
                        annotation["bbox"][1] + annotation["bbox"][3]
                    ]
                ],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            })

        if not Path(DIRECTORY_OUTPUT).exists():
            os.mkdir(DIRECTORY_OUTPUT)

        for key, anylabeling_annotation in anylabeling_annotations.items():
            suffix = Path(anylabeling_annotation['imagePath']).suffix
            with open(file=f"{DIRECTORY_OUTPUT}/{str(anylabeling_annotation['imagePath']).replace(suffix, '.json')}",
                      mode="w") as f:
                json.dump(obj=anylabeling_annotation, fp=f, indent=5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--coco-annotations-file", type=str, default="./_annotations.coco.json",
                        help="COCO annotations file.")
    parser.add_argument("-s", "--consider-supercategory", action="store_true",
                        help="Consider supercategory as category.")
    opt = parser.parse_args()

    convert(coco_annotations_file=opt.coco_annotations_file, consider_supercategory=opt.consider_supercategory)

    print("Conversion finished.")
