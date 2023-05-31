from google.cloud import vision
from google.oauth2 import service_account
from typing import Sequence

def analyse_image(image_bytes: str, feature_types: Sequence=[vision.Feature.Type.TEXT_DETECTION]):
    credentials = service_account.Credentials.from_service_account_file(
        "./credentials.json"
    )
    client = vision.ImageAnnotatorClient(credentials=credentials)

    image = vision.Image(content=image_bytes)
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)

    return response

def get_text(response: vision.AnnotateImageResponse):
    # print(response.text_annotations[0].description)
    return response.text_annotations[0].description
    # for annotation in response.text_annotations:
    #     vertices = [f"({v.x}, {v.y})" for v in annotation.bounding_poly.vertices]
    #     print(
    #         f"{repr(annotation.description):42}",
    #         ",".join(vertices),
    #         sep=" | "
    #     )


# with open("./assets/images/chandra.png", "rb") as file:
#     image_bytes = file.read()

# response = analyse_image(
#     image_bytes=image_bytes, feature_types=[vision.Feature.Type.TEXT_DETECTION]
# )
# print_text(response)
