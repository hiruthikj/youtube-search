# import logging
# from typing import Any

# import boto3
# import pandas as pd
# import sqlalchemy
# from fastapi import HTTPException, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from fastapi.routing import APIRouter

# from .extenstions.logging_router import LoggingRoute

from fastapi import APIRouter

from .config import settings
from .extenstions.logging_router import LoggingRoute

search_router = APIRouter(prefix=settings.API_V1_STR, route_class=LoggingRoute)


# @search_router.post(path="/list")
# def add_metrics_tracking(metrics_record):
#     try:
#         logger = logging.getLogger()
#         logger.info(f"add_metrics_tracking Input: {metrics_record}")

#         metrics_record = metrics_record.model_dump()
#         metrics_record["time"] = pd.to_datetime(
#             metrics_record["time"], unit="s", utc=True
#         )
#         metrics_record["date"] = metrics_record["time"].date()
#         metrics_record["date"] = str(metrics_record["date"])

#         logger.info(
#             f"add_metrics_tracking Input after Transformation: {metrics_record}"
#         )

#         df = pd.DataFrame([metrics_record])
#         logger.info(f"Dataframe to write to apiAuditCache: {get_printable(df)}")
#         api_audit_cache_table = "apiAuditCache"

#         dialect = "mysql"
#         # driver = "mysqlconnector"
#         driver = "pymysql"

#         url_object = sqlalchemy.URL.create(
#             drivername=f"{dialect}+{driver}",
#             username=settings.DBUSER,
#             password=settings.DBPWD,
#             host=settings.DBHOST,
#             database=Databases.EXTENGRAPIS,
#             port=3306,
#         )

#         engine = sqlalchemy.create_engine(url_object, echo=False)
#         with engine.connect() as conn:
#             rows_affected = df.to_sql(
#                 name=api_audit_cache_table, con=conn, if_exists="append", index=False,
#             )
#             logger.info(f"Inserted into {api_audit_cache_table}")

#         if settings.BACKUP_PUSH_PARQUET:
#             parquet_bucket_name = settings.ATHENA_DATABASE
#             parquet_file_name = "data.snappy.parquet"
#             parquet_subfolder = settings.PARQUET_S3_BACKUP_SUBFOLDER

#             aws_region = settings.AWS_REGION
#             boto3.setup_default_session(region_name=aws_region)

#             create_or_append_parquet_to_s3(
#                 df,
#                 parquet_bucket_name,
#                 parquet_subfolder,
#                 parquet_file_name,
#                 partition_cols=["date"],
#             )


#         response = {
#             "status": RequestStatus.SUCCESS,
#         }
#         return JSONResponse(
#             content=jsonable_encoder(response),
#             status_code=status.HTTP_201_CREATED,
#         )

#     except Exception:
#         logger.exception("add_metrics_tracking Failed")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal Server Error",
#         )
