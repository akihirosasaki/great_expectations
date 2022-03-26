gcloud auth application-default login
great_expectations --v3-api init
great_expectations --v3-api datasource new --no-jupyter
jupyter notebook /usr/app/great_expectations/uncommitted/datasource_new.ipynb --allow-root --ip=0.0.0.0
great_expectations --v3-api suite new --no-jupyter
SQLAlchemy==1.4.25


Profiler
- メトリクスとデータの期待結果を生成する

Metric
- 算出されるデータの属性

Expectation
- データについて検証できる宣言方式

dbt init dbt
dbt debug
export DBT_PROFILES_DIR=/usr/app/dbt




