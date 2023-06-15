"""
Routes for all admin related stuffs
"""

from fastapi import APIRouter
from db.operations import *

admin_route = APIRouter(prefix="/admin", tags=["admin"])
