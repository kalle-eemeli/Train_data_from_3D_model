from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians
import os


# TODO also save and check going_up / going_right

if os.path.exists('./last_cam_position.txt'):
    with open('last_cam_position.txt', 'r') as f:
        content = f.readline()
        arr = content.split(',')
        
        last_camera_pos = Vector3([float(arr[0]), float(arr[1]), float(arr[2])])

        #print(last_camera_pos)
        
else:
    last_camera_pos = Vector3([0.0, 4.0, 3.0])

MAX_X = 7
MAX_Y = 4

class Camera:
    def __init__(self, target=Vector3([0.0, 0.0, 0.0])):
        self.camera_pos = last_camera_pos
        self.camera_front = Vector3([0.0,0.0,-1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.target = target

        self.jaw = -90
        self.pitch = 0

        self.going_up = False
        self.going_right = False

    def save_camera_position(self):
        #last_camera_pos = self.camera_pos

        vec_to_string = ','.join(map(str, self.camera_pos))

        with open("last_cam_position.txt", 'w') as f:
            f.write(vec_to_string)

    def get_view_matrix(self):

        # UP DOWN
        if self.camera_pos.y >= MAX_Y:
            self.going_up = False

        if self.camera_pos.y <= -MAX_Y:
            self.going_up = True

        if self.going_up == True:
            self.camera_pos.y += 0.01
        elif self.going_up == False:
            self.camera_pos.y -= 0.01

        # LEFT RIGHT
        if self.camera_pos.x >= MAX_X:
            self.going_right = False

        if self.camera_pos.x <= -MAX_X:
            self.going_right = True

        if self.going_right == True:
            self.camera_pos.x += 0.01
        elif self.going_right == False:
            self.camera_pos.x -= 0.01

        #return matrix44.create_look_at(self.camera_pos, self.target, self.camera_up)
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalize(front)
        self.camera_right = vector.normalize(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalize(vector3.cross(self.camera_right, self.camera_front))