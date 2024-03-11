# Convert COCO Annotations to Anylabeling

## How to run

```
python ./convert_coco_annotations_to_anylabeling/main.py
```

### Parameters

```
-a, --coco-annotations-file   COCO annotations file. Default: "./_annotations.coco.json".
-s, --consider-supercategory  Consider supercategory as category.
```

### Example

```
python ./convert_coco_annotations_to_anylabeling/main.py -s
```
