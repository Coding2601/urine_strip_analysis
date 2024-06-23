from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
import cv2
import numpy as np

class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.data['image']               #get the image from the request
        file_path = default_storage.save(file_obj.name, file_obj) #save the image
        image_path = default_storage.path(file_path)    #get the path of the image
        colors = self.process_image(image_path)         #process the image
        obj = {}                                    #dictionary to store the colors

        obj['URO'] = colors[0]
        obj['BIL'] = colors[1]
        obj['KET'] = colors[2]
        obj['BLD'] = colors[3]
        obj['PRO'] = colors[4]
        obj['NIT'] = colors[5]
        obj['LEU'] = colors[6]
        obj['GLU'] = colors[7]
        obj['SG'] = colors[8]
        obj['PH'] = colors[9]
        
        return Response({'colors': obj})                 #return the colors

    def process_image(self, image_path):
        image = cv2.imread(image_path)                  # Load the image
        strip_roi = image[100:200, 50:450]  #assumed, the strip is in a specific position and orientation.
        colors = []                                    #list to store the colors of the strip
        segment_height = strip_roi.shape[0] // 10     #height of each segment
        for i in range(10):
            segment = strip_roi[i * segment_height:(i + 1) * segment_height, :]  #get the segment
            avg_color_per_row = np.average(segment, axis=0)         #average color of the segment
            avg_color = np.average(avg_color_per_row, axis=0)    #average color of the segment
            colors.append(avg_color.tolist())                 #append the color to the list
        return colors