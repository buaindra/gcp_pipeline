# changeble terraform variable --start--
# google project
project_id = "gcp-pipeline-354810"
project_number = "265589241500"
region = "us-central1"
zone = "us-central1-a"
deletion_protection = "false"
# changeble terraform variable --end--


# default terraform variable --start--
# service account
sa_id = "sa-gcp-pipeline"

# cloud sql
cloudsql_database_version = "POSTGRES_14"
cloudsql_machine_type = "db-f1-micro"
cloudsql_user = "postgres"
cloudsql_pswd = "admin@1243"

# cloud composer
composer_name = "composer-env"
composer_image_version = "composer-2.0.18-airflow-2.2.5"

# default terraform variable --end--