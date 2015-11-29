from pyglet.gl import *
from util.texture import Texture


class SkySphere():
    def __init__(self, filename, radius):
        self.radius = radius
        self.texture = Texture(filename)
        self.sphere = gluNewQuadric()
        gluQuadricNormals(self.sphere, GLU_SMOOTH)
        gluQuadricTexture(self.sphere, GL_TRUE)

    def draw(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDisable(GL_CULL_FACE)
        self.texture.draw()
        gluSphere(self.sphere, self.radius, 50, 50)
