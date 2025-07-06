# app.py

from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
import json
import os

from db_control import crud, mymodels
from db_control.create_tables import init_db
from dotenv import load_dotenv
from typing import Optional

# アプリケーション初期化時にテーブルを作成
init_db()

# === Pydantic モデル ===
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

class TORIMEI(BaseModel):
    # TRD_ID: int
    # DTL_ID: int
    # PRD_ID: int
    # PRD_CODE: str
    # PRD_NAME: str
    # PRD_PRICE: int
    # PRD_PRICE_INC_TAX: int
    # TAX_CD: str
    
    trd_id:      int
    dtl_id:      Optional[int] = None  # 自動採番列は任意
    prd_id:      int
    prd_code:    str
    prd_name:    str
    prd_price:   int
    prd_price_inc_tax: int
    tax_cd:      str
    
    class Config:
        # JSON 側で大文字キーを使うなら次を有効化
        alias_generator = str.upper
        allow_population_by_field_name = True
        
#     model_config = ConfigDict(populate_by_name=True)
    
app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# .envファイルを読み込む
load_dotenv()
print("DATABASE_URL:", os.getenv("DATABASE_URL"))


@app.get("/")
def index():
    return {"message": "FastAPI top page!"}


@app.get("/shouhin")
def read_shouhin(CODE: int = Query(...)):
    result = crud.myselect(mymodels.SHOUHIN, CODE)
    if not result:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    items = json.loads(result)
    return items[0] if items else None


@app.post("/torihiki")
def create_torihiki(data: TORIHIKI):
    # Pydantic モデル → dict
    payload = data.dict(exclude_none=True, exclude={"TRD_ID"})
    # ORM モデルを正しく渡す
    crud.myinsert_torihiki(mymodels.TORIHIKI, payload)
    # 最大 TRD_ID を取得
    new_id = crud.myselect_TRD_ID(mymodels.TORIHIKI)
    return {"TRD_ID": new_id}


@app.post("/torimei")
# def create_torimei(data: TORIMEI):
#     values = data.dict()
#     # ORM モデルを正しく渡す
#     result = crud.myinsert_torimei(mymodels.TORIMEI, values)
#     return {"status": result}

# def create_torimei(data: TORIMEI):
#     payload = data.model_dump()        # → {'trd_id':…, 'dtl_id':…, …}
#     crud.myinsert_torimei(mymodels.TORIMEI, payload)
#     return {"status": "inserted"}


def create_torimei(data: TORIMEI):
    # dtl_id は DB 側で生成させるので除外
    payload = data.model_dump(by_alias=True, exclude_unset=True, exclude={"dtl_id"})
    new = crud.insert_torimei_and_return(data_model=mymodels.TORIMEI, values=payload)
    return {"trd_id": new.trd_id, "dtl_id": new.dtl_id}

