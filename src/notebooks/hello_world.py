# Databricks notebook source

print("Hello World!")

# COMMAND ----------

dbutils.widgets.text("environment", "")
dbutils.widgets.text("commit_msg", "")

# COMMAND ----------

environment = dbutils.widgets.get("environment")
print(f"Running in environment: {environment}")

# COMMAND ----------

commit_msg = dbutils.widgets.get("commit_msg")
print(f"This is the commit message: {commit_msg}")