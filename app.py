from fastapi import FastAPI, HTTPException, Query
from fastapi import Depends, HTTPException, status
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
from sqlalchemy import create_engine, insert, delete, update, select ,BigInteger, Column


# from openai import OpenAI

# # アプリケーション初期化時にテーブルを作成
init_db()

class SHOUHIN(BaseModel):
    PRD_ID: int
    CODE: int
    NAME: str
    PRICE: int
    PRICE_INC_TAX: int

class TORIHIKI(BaseModel):
    TRD_ID: Optional[int] = None
    DATETIME: str
    EMP_CD: str
    STORE_CD: str
    POS_NO: str
    TOTAL_AMT: int
    TTL_AMT_EX_TAX: int
    TTL_AMT_INC_TAX: int

# class Base(DeclarativeBase):
#     pass

class TORIMEI(BaseModel):
    TRD_ID: int
    DTL_ID: int
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int
    PRD_PRICE_INC_TAX: int
    TAX_CD: str

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####  nakano add Start  ####
# .envファイルを読み込む
load_dotenv()
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

###　●●●　Local用　　●●●
# 環境変数からAPIキーを取得
# OpenAI.api_key = os.getenv("OPENAI_API_KEY")
# kokudo_api_key = os.getenv("kokudo_API_KEY")

###　●●●　Host用　　●●●
# シークレットからAPIキーを取得
# OpenAI.api_key  = st.secrets["OPENAI_API_KEY"]

####  nakano add End  ####

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

@app.get("/shouhin")
def read_shouhin(CODE: int = Query(...)):
    result = crud.myselect(mymodels.SHOUHIN, CODE)
    if not result:
        raise HTTPException(status_code=404, detail="")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


@app.post("/torihiki")
def create_torihiki(
    data: TORIHIKI,
#    session: Session = Depends(get_session)  # 必要に応じてセッションを依存注入
):
    # TRD_ID は自動採番なので除外
    payload = data.dict(exclude_none=True, exclude={"TRD_ID"})
    # CRUD 実行（引数は適宜調整）
    crud.myinsert_torihiki(TORIHIKI_ORM, payload)
    new_id = crud.myselect_TRD_ID(TORIHIKI_ORM)
    return {"TRD_ID": new_id}


# def create_TORIHIKI(TORIHIKI: TORIHIKI):
#     print("nakano TORIHIKI",TORIHIKI)
#     values = TORIHIKI.dict()
    
#     tmp = crud.myinsert_torihiki(mymodels.TORIHIKI, values)
#     result = crud.myselect_TRD_ID(mymodels.TORIHIKI)
#     return result

@app.post("/torimei")
def create_TORIMEI(TORIMEI: TORIMEI):
    print("nakano TORIMEI",TORIMEI)
    values = TORIMEI.dict()
    
    result = crud.myinsert_torimei(mymodels.TORIMEI, values)
    return result
