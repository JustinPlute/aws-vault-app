#!/usr/bin/env python3

"""
Author: Justin Plute (rplute@gmail.com)
Title: AWS Vault Application
Description: Fetches SSM secrets and connects to MySQL RDS instance
"""

import json
import sys
import logging
import boto3
import pymysql
import rds_config

#rds settings
rds_host  = rds_config.db_host
db_name = rds_config.db_name

SSM_ENV = os.environ.get("SSM_ENV", "dev")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_ssm_parameters(ssm_env=None):
    """
    Gets user and password secrets from AWS SSM Param Store
    """

    client = self.session.client("ssm")

    password = client.get_parameter(
        Name=f"/env/{ssm_env}/service-now/password",
        WithDecryption=True
        )

    user = client.get_parameter(
        Name=f"/env/{ssm_env}/service-now/user",
        WithDecryption=True

    return user["Parameter"]["Value"], password["Parameter"]["Value"]

def handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """

    name, pwd = get_ssm_parameters(SSM_ENV)

    try:
        conn = pymysql.connect(rds_host, user=name, passwd=pwd, db=db_name, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

    item_count = 0

    with conn.cursor() as cur:
        cur.execute("create table Employee3 ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
        cur.execute('insert into Employee3 (EmpID, Name) values(1, "Joe")')
        cur.execute('insert into Employee3 (EmpID, Name) values(2, "Bob")')
        cur.execute('insert into Employee3 (EmpID, Name) values(3, "Mary")')
        conn.commit()
        cur.execute("select * from Employee3")
        for row in cur:
            item_count += 1
            logger.info(row)

    return "Added %d items from RDS MySQL table" %(item_count)