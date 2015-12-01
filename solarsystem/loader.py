"""
Created on 01.12.2015

:author: Rene Hollander
"""

import glob
import json

import os
from os.path import basename, splitext
from solarsystem.body import OrbitingBody, StationaryBody
from solarsystem.orbit import CircularOrbit
from solarsystem.renderer import OrbitingBodyWithRingRenderer, setup_ring_renderer
from util import dts


def load_bodies(directory):
    """
    Loads all bodies that are defined in the JSON files from the given directory

    :param directory: directory to load the bodies from
    :type directory: str
    :return: list of the loaded bodies
    :rtype: list
    """

    files = glob.glob(os.path.join(directory, "*.json"))
    bodies = {}
    for file in files:
        with open(file) as data_file:
            internal_name = splitext(basename(file))[0]
            bodies[internal_name] = load_body(json.load(data_file))
    for key in bodies:
        body = bodies[key]
        if body.parent_internal_name is not None:
            body.parent = bodies[body.parent_internal_name]
            del body.parent_internal_name

    return bodies.values()


def load_body(data):
    """
    Load the body from the specified JSON data. Parent is not set here!

    :param data: JSON data to load the body from
    :return: Body from the supplied data
    :rtype: :class:`solarsystem.body.Body`
    """

    name = data["name"]
    parent = None
    if "parent" in data:
        parent = data["parent"]
    texture = data["texture"]
    basecolor = data["basecolor"]
    radius = data["radius"]
    axial_tilt = data["axial_tilt"]
    sidereal_rotation_period = data["sidereal_rotation_period"] * dts
    has_orbit = False
    orbit = None
    has_ring = False
    ring_texture = None
    ring_inner_radius = None
    ring_outer_radius = None

    if "orbit" in data:
        has_orbit = True
        orbit = load_orbit(data["orbit"])
    if "ring" in data:
        ring_data = data["ring"]
        has_ring = True
        ring_texture = ring_data["texture"]
        ring_inner_radius = ring_data["radius"]["inner"]
        ring_outer_radius = ring_data["radius"]["outer"]

    body = None

    if has_orbit:
        if has_ring:
            body = setup_ring_renderer(ring_texture, ring_inner_radius, ring_outer_radius, OrbitingBody(None, name, texture, basecolor, radius, orbit, axial_tilt, sidereal_rotation_period, renderer=OrbitingBodyWithRingRenderer()))
        else:
            body = OrbitingBody(None, name, texture, basecolor, radius, orbit, axial_tilt, sidereal_rotation_period)
    else:
        body = StationaryBody(None, name, texture, basecolor, radius, axial_tilt, sidereal_rotation_period)

    body.parent_internal_name = parent
    return body


def load_orbit(data):
    """
    Load the orbit from the given data

    :param data: JSON data
    :return: Orbit from the JSON data
    :rtype: :class:`solarsystem.orbit.Orbit`
    """

    type = data["type"]
    if type == "circular":
        radius = data["radius"]
        orbital_period = data["orbital_period"] * dts
        inclination = data["inclination"]
        return CircularOrbit(radius, orbital_period, inclination)
    else:
        raise TypeError("type " + type + " is invalid")
