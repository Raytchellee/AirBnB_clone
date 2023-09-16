#!/usr/bin/python3
"""Defines Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent one amenity.
    Attributes:
        name: The name of the amenity.
    """

    name = ""
