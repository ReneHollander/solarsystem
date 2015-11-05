#version 330 core

layout(location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;

uniform mat4 transformation;

out vec2 texCoord0;

void main() {
    gl_Position = transformation * vec4(position, 1.0);
    texCoord0 = texCoord;
}
