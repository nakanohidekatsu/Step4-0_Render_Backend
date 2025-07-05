from sqlalchemy import text
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import pandas as pd
import json
from graphene import ObjectType, String, Int, List, Schema, Mutation, Field
import os
from db_control import crud, mymodels
from db_control.create_tables import init_db
from dotenv import load_dotenv
from typing import Optional

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.scalar())
    