from __future__ import with_statement
from sys import prefix
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from ObjLoader import ObjLoader
from PIL import Image
import threading
import time, datetime

from camera import Camera

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2


vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""

# filename = "test1.jpg"
img_counter = 0

buffer = []
batch_size = 10

prefix = ["cube", "cone", "sphere"]

def save_images(buff):

    # TODO ADD PREPROCESSING BEFORE SAVING (RESIZING)

    start = glfw.get_time()

    for img in buff:

        name = img[0]   # str
        data = img[1]   # Image

        # Resize the image

        image = pre_processing(data)
        
        image.save(f"images/{prefix[2]}/{name}.jpg", "JPEG")
        # time.sleep(0.3)

    end = glfw.get_time()

    print(f"Saving done in {end - start}")

def pre_processing(image, size=(640, 360)):

    # This is where all of the preprocessing will be done
    # Resizing, cropping etc.

    pp_args = {
    'resample': 0,
    'box': None 
    }

    new_image = Image.Image.resize(image, size, pp_args['resample'], pp_args['box'])

    return new_image
    

def wrapper_func(buff):
    
    save_images(buff)

def render_to_jpg(format="JPEG"):

    global img_counter
    global buffer

    if len(buffer) >= batch_size:

        buffer2 = buffer.copy() # Copy the buffer to clear the original one
        buffer = []
        #threadSaveImages = threading.Thread(target=save_images(buffer2))
        threadSaveImages = threading.Thread(target=wrapper_func, args=[buffer2])
        threadSaveImages.daemon = False
        threadSaveImages.start()

    x, y, width, height = glGetDoublev(GL_VIEWPORT)
    width, height = int(width), int(height)
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    buffer.append((time, image))

    print(len(buffer))

    #image.save(f"images/test{counter}.jpg", format)
    img_counter += 1


def window_resize(window, width, height):

    glViewport(0,0,width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

def key_input_cb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    
    # if key == glfw.KEY_F12 and action == glfw.PRESS:
    #     render_to_jpg()

def main():
    if not glfw.init():
        raise Exception("glfw could not be initialized")

    window = glfw.create_window(WIDTH, HEIGHT, "Main", None, None)

    if not window:
        glfw.terminate()
        raise Exception("Window could not be created")

    glfw.set_window_pos(window, 400, 400)

    glfw.set_window_size_callback(window, window_resize)

    glfw.set_key_callback(window, key_input_cb)

    glfw.make_context_current(window)

    # load the 3d mesh

    meshes = ["cube", "cone", "sphere"]

    filepath = f"meshes/{meshes[2]}.obj"

    object_indices, object_buffer = ObjLoader.load_model(filepath)

    # load shaders

    # def load_shaders(file):
    #     with open(file) as f:
    #         content = f.read()
        
    #     return content

    #vertex_src = load_shaders("vertex_shader.vert")
    #fragment_src = load_shaders("fragment_shader.frag")

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, object_buffer.nbytes, object_buffer, GL_STATIC_DRAW)

    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(0))
    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(12))
    # normals
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(20))

    textures = glGenTextures(1)

    # load texture
    glBindTexture(GL_TEXTURE_2D, textures)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    texture_path = "meshes/checkered.jpg"

    image = Image.open(texture_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH/HEIGHT, 0.1, 100)
    object_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -1, -10]))

    view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    # glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # save images every 5 seconds

    time = glfw.get_time()
    seconds = 1

    while not glfw.window_should_close(window):
        glfw.poll_events()

        current_time = glfw.get_time()
        elapsed_time = current_time - time

        if elapsed_time > seconds:
            #render_to_jpg()
            time = current_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        rot_x = pyrr.Matrix44.from_x_rotation(0.8 * glfw.get_time())

        rotation = pyrr.matrix44.multiply(rot_y, rot_x)

        model = pyrr.matrix44.multiply(rotation, object_pos)

        glBindVertexArray(VAO)
        glBindTexture(GL_TEXTURE_2D, textures)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(object_indices))

        glfw.swap_buffers(window)
    
    cam.save_camera_position()
    glfw.terminate()

if __name__ == '__main__':
    main()