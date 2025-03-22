from PIL import ImageDraw
from PIL import Image
import moondream
from collections import OrderedDict
#model = moondream.vl(model="/usr/share/ollama/.ollama/models/moondream-0_5b-int8.mf.gz")
#img = Image.open('/home/ttombbab/Downloads/Download/640px-Cairo_museum_8.jpg')
#encoded_image = model.encode_image(img)
#print(model.caption(encoded_image)['caption'])
#print(model.query(encoded_image,'what is in this image?')['answer'])
#print(model.detect(encoded_image,'pryamid-shaped'))
#Bounding_box(img,detect['objects'][0])

model= moondream.vl(model="/usr/share/ollama/.ollama/models/moondream-0_5b-int8.mf.gz")

class moonhelp(object):
    global model
    def __init__(self,img,NonLocal=False,caption=True):
        self.model = model
        if NonLocal:
            self.img = self.open_image_from_url(img)
        elif img == None:
            print('No Image')
            return
        else:
            self.img = Image.open(img)
        self.detected = {}
        self.querys = ''
        self.querys_quest = ''
        self.detected_item = ''
        self.detect_image = self.img
        self.boxes = []
        self.points = []
        self.crops = []
        #print('Encodeing Image')
        self.encoded_img = self.model.encode_image(self.img)
        #print('Generating caption')
        if caption:
            self.caption = self.model.caption(self.encoded_img)['caption']
        else:
            self.caption = ''
      
        
			

    def Bounding_box(self,img,box):
        x_min = int(round(box['x_min']*img.size[0]))
        x_max = int(round(box['x_max']*img.size[0]))
        y_min = int(round(box['y_min']*img.size[1]))
        y_max = int(round(box['y_max']*img.size[1]))   
        return (x_min,y_min,x_max,y_max)
        
    def box_to_point(self,box):
        point = (int(((box[2]-box[0])/2)+box[0]),int(((box[3]-box[1])/2)+box[1]))
        return point
        
    def remove_duplacates(self,box_list):
        ud = OrderedDict()
        for d in box_list:
            ks = tuple(d.items())
            ud[ks]=d
        return list(ud.values())
        
    def Image_box(self,boxes,outlinecolor):
        img2= self.img.copy()
        draw = ImageDraw.Draw(img2)
        for box in boxes:
            draw.rectangle(self.Bounding_box(img2,box),outline=outlinecolor)
        return img2
    

    def detect(self,item,outlinecolor=(255,255,0)):
        self.detected_item = item
        self.boxes = []
        self.points = []
        self.detected = self.model.detect(self.encoded_img,item)
        if len(self.detected['objects']) == 0:
            return self.img
        else:
            d_objects = self.remove_duplacates(self.detected['objects'])
            for box in d_objects:
                self.boxes.append(self.Bounding_box(self.img,box))
                self.points.append(self.box_to_point(self.Bounding_box(self.img,box)))
            self.detect_image = self.Image_box(d_objects,outlinecolor)
            return self.detect_image
            
    def detect_crops(self,item,outlinecolor=(255,255,0)):
        self.detected_item = item
        crops = []
        self.boxes = []
        self.points = []
        self.detected = self.model.detect(self.encoded_img,item)
        if len(self.detected['objects']) == 0:
            self.crops = []
            return self.img
        else:
            d_objects = self.remove_duplacates(self.detected['objects'])
            for box in d_objects:
                self.boxes.append(self.Bounding_box(self.img,box))
                self.points.append(self.box_to_point(self.Bounding_box(self.img,box)))
                crops.append(self.img.crop(self.Bounding_box(self.img,box)))
            self.crops = crops
            return crops
                
    def query(self,quest):
        self.querys_quest = quest
        self.querys = self.model.query(self.encoded_img,quest)['answer']
        return self.querys
        
    def open_image_from_url(self,url):
        import requests
        response = requests.get(url)
        from io import BytesIO    
        if response.status_code != 200:
            print(f"Failed to download the image. Status code: {response.status_code}")
            return None
    
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        return img
    
