# Databricks notebook source

print("Hello World!")

# COMMAND ----------

dbutils.widgets.text("environment", "")

# COMMAND ----------

environment = dbutils.widgets.get("environment")
print(f"Running in environment: {environment}")