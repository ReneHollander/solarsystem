from pyglet.gl import *


class Texture(object):
    def __init__(self, path):
        self.image_name = path.split('/')[-1]
        self.image = pyglet.resource.image(self.image_name)
        self.texture = self.image.texture
        self.verify_dimensions()
        glGenerateMipmap(self.texture.target)

    def draw(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        glTexParameterf(self.texture.target, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
        glTexParameterf(self.texture.target, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    def verify_dimensions(self):
        self.verify('width')
        self.verify('height')

    def verify(self, dimension):
        value = self.texture.__getattribute__(dimension)
        while value > 1:
            div_float = float(value) / 2.0
            div_int = int(div_float)
            if not (div_float == div_int):
                raise Exception('image %s is %d, which is not a power of 2' % (
                    dimension, self.texture.__getattribute__(dimension)))
            value = div_int
