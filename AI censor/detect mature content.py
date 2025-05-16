from ultralytics import YOLO
import numpy as np

def filter_content(detected: dict, filt: list):
    '''
    Function that compare filter and detected objects
    Gets:
        detected: dict of objects were detected on image and True or False deppends on availability
        filt: list of objects shouldn't be passed to chat
    Returns:
        If image meets the requirements:
            True
        Else:
            False 
    '''
    for element in filt:
        if detected[element]:
            return False
    return True

def detect_mature(image: np.ndarray):
    '''
    Finds certain object can be undesirable for administrator using YOLOv8
    Gets:
        image: np.ndarray containing testing image
    Returns:
        mature_content: dict of objects were detected on image and True or False deppends on availability
    '''
    model = YOLO("best.pt")
    results = model.predict(image, save=False)
    
    mature_content = {
        'EXPOSED_BELLY': False, 
        'EXPOSED_BREAST_F': False, 
        'EXPOSED_BREAST_M': False, 
        'EXPOSED_BUTTOCKS': False, 
        'EXPOSED_GENITALIA_F': False, 
        'EXPOSED_GENITALIA_M': False
    }

    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.5:
                mature_content[model.names[int(box.cls)]] = True
    
    return mature_content