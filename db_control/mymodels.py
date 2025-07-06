from sqlalchemy import String, Integer ,BigInteger, Column , ForeignKey,Identity
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import datetime


class Base(DeclarativeBase):
    pass

class SHOUHIN(Base):
    __tablename__ = 'SHOUHIN'
    PRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CODE: Mapped[int] = mapped_column(Integer)
    NAME: Mapped[str] = mapped_column(String(50))
    PRICE: Mapped[int] = mapped_column(Integer)
    PRICE_INC_TAX: Mapped[int] = mapped_column(Integer)

# class TORIMEI(Base):
#     __tablename__ = 'TORIMEI'
#     trd_id = mapped_column(BigInteger, ForeignKey('TORIHIKI.TRD_ID'), primary_key=True)
#     dtl_id = mapped_column(
#         Integer,
#         Identity(start=1, cycle=False),
#         primary_key=True
#     )
#     prd_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     prd_code: Mapped[str] = mapped_column(String(13))
#     prd_name: Mapped[str] = mapped_column(String(50))
#     prd_price: Mapped[int] = mapped_column(Integer)
#     prd_price_inc_tax: Mapped[int] = mapped_column(Integer)
#     tax_cd: Mapped[str] = mapped_column(String(2))

class TORIMEI(Base):
    __tablename__ = 'TORIMEI'
    TRD_ID: Mapped[int] = mapped_column(Integer)
    DTL_ID: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    PRD_ID: Mapped[int] = mapped_column(Integer)
    PRD_CODE: Mapped[str] = mapped_column(String(13))
    PRD_NAME: Mapped[str] = mapped_column(String(50))
    PRD_PRICE: Mapped[int] = mapped_column(Integer)
    PRD_PRICE_INC_TAX: Mapped[int] = mapped_column(Integer)
    TAX_CD: Mapped[str] = mapped_column(String(2))

class TORIHIKI(Base):
    __tablename__ = 'TORIHIKI'
    TRD_ID: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    DATETIME: Mapped[str] = mapped_column(String)
    EMP_CD: Mapped[str] = mapped_column(String(10))
    STORE_CD: Mapped[str] = mapped_column(String(5))
    POS_NO: Mapped[str] = mapped_column(String(3))
    TOTAL_AMT: Mapped[int] = mapped_column(Integer)
    TTL_AMT_EX_TAX: Mapped[int] = mapped_column(Integer)
    TTL_AMT_INC_TAX: Mapped[int] = mapped_column(Integer)
    
# class TORIHIKI_ORM(Base):
#     __tablename__ = "TORIHIKI"
#     TRD_ID: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
#     DATETIME: Mapped[str] = mapped_column(String, nullable=False)
#     EMP_CD: Mapped[str] = mapped_column(String, nullable=False)
#     STORE_CD: Mapped[str] = mapped_column(String, nullable=False)
#     POS_NO: Mapped[str] = mapped_column(String, nullable=False)
#     TOTAL_AMT: Mapped[int] = mapped_column(Integer, nullable=False)
#     TTL_AMT_EX_TAX: Mapped[int] = mapped_column(Integer, nullable=False)
#     TTL_AMT_INC_TAX: Mapped[int] = mapped_column(Integer, nullable=False)


