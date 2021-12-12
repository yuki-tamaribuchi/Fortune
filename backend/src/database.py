from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# "種類+ドライバ://ユーザネーム:パスワード@ホスト:ポート/データベース?charset=キャラセット"
#SQL_ALCHEMY_DATABASE_URL = "mysql+pymysql://fortune_db_user:password@db/fortune_db?charset=utf8mb4"
SQL_ALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "")


#DBエンジンのインスタンスを作成。
engine = create_engine(
	SQL_ALCHEMY_DATABASE_URL
)

#セッション作成。セッションとは、コネクションを確立してから切断するまでの一連の単位のこと。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#モデルベースクラス。これを拡張して、ORMで扱うモデルクラスにする。
Base = declarative_base()