"""
Ref:
    1. Python Lib for Authentication:
        1. https://googleapis.dev/python/google-auth/1.7.0/user-guide.html
        2. stackoverflow: https://stackoverflow.com/questions/53472429/how-to-get-a-gcp-bearer-token-programmatically-with-python
    2. gcloud module: https://pypi.org/project/gcloud/
    3. Cloud pubsub:
        1. https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library
        2. https://googleapis.dev/python/pubsub/latest/index.html
        3. Rest API: https://cloud.google.com/pubsub/docs/reference/rest
        4. Samples: https://cloud.google.com/pubsub/docs/samples/
    4. Cloud Sql:
        1. https://pypi.org/project/cloud-sql-python-connector/
    5. Cloud Composer:
        1. Sample Git: https://github.com/googleapis/python-orchestration-airflow/tree/main/samples/generated_samples
        2. GOOGLE doc for Rest API: https://cloud.google.com/composer/docs/reference/rest/v1/projects.locations.environments/create?hl=en
    6. Cloud Security (Secret-Manager):
        1. https://cloud.google.com/secret-manager/docs/reference/libraries
        2. https://cloud.google.com/python/docs/reference/secretmanager/latest
    7. Sendgrid Email from Composer:
        1. https://cloud.google.com/composer/docs/composer-2/configure-email


Required services/apis needs to enable:
    1. gcloud services enable pubsub.googleapis.com
    2. gcloud services enable composer.googleapis.com
        1. provide Cloud Composer v2 API Service Agent Extension role to Composer API Service Agent service account
    3. gcloud services enable secretmanager.googleapis.com
        1. provide secretmanager.secretAccessor role to service account, associated with the composer env.

Required Packages:
    1. pip install --upgrade google-auth
    2. pip install --upgrade google-cloud-pubsub
    3. python3 -m pip install requests
    4. pip install --upgrade google-cloud-secret-manager

python3 ~/gcp/gcp_infra_utility.py
"""

import google.auth  # for default authentication
import google.auth.transport.requests  # to refresh the google credentials
from google.oauth2 import service_account  # for service account authentication
# import googleapiclient.discovery
# from oauth2client.client import GoogleCredentials
from google.cloud import pubsub_v1  # python client for pub-sub
from google.cloud import secretmanager
# from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1.types import Secret
import os  # get file location and other stuffs
import sys  # required for accessing parameter while calling python file
import requests  # required for rest api call
from requests.models import PreparedRequest  # to pass parameter into the rest api url
import json  # required for convert python obj to json obj
import configparser
import logging


class GCP_Infra_Utility(object):

    def __init__(self, project_id=None, region=None, cred_path=None):
        self.scope = []
        self.scope.append('https://www.googleapis.com/auth/cloud-platform')
        try:
            if project_id is None and cred_path is None:
                self.credentials, self.project_id = google.auth.default(scopes=self.scope)
            else:
                # credentials = GoogleCredentials.get_application_default()
                # self._compute = googleapiclient.discovery.build(
                #     'compute', 'v1', cache_discovery=False, credentials=credentials)

                self.credentials = service_account.Credentials.from_service_account_file(
                    cred_path).with_scopes(self.scope)
                self.project_id = project_id

        except Exception as e:
            print(f"error: {e}")

        auth_req = google.auth.transport.requests.Request()
        self.credentials.refresh(auth_req)
        self.rest_api_headers = {
            'Authorization': f'Bearer {self.credentials.token}',
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.pudsub_api_base_url = "https://pubsub.googleapis.com"
        self.pubsub_api_version = "v1"
        self.publisher = pubsub_v1.PublisherClient()

        if region is None:
            self.region = "us-central1"
        else:
            self.region = region

        self.secret_client = secretmanager.SecretManagerServiceClient()
        # self.secret_client = secretmanager_v1.SecretManagerServiceClient()

    def create_pubsub_topic(self, topic_id):
        # gcloud services enable pubsub.googleapis.com

        out = self.get_pubsub_topic(topic_id)

        if topic_id not in out.get("topic_list", []):
            topic_path = self.publisher.topic_path(self.project_id, topic_id)
            topic = self.publisher.create_topic(request={"name": topic_path})
            return topic.name
        else:
            return f"Topic: {topic_id} already exists"

    def get_pubsub_topic(self, topic_id=None):

        response = {}
        topic_list = []
        topic_subscriptions = []
        project_path = f"projects/{self.project_id}"

        for topic in self.publisher.list_topics(request={"project": project_path}):
            topic_name = str(topic).strip().split("/")[-1].replace('"', '')
            topic_list.append(topic_name)

        if (topic_id is not None and topic_id in topic_list):
            topic_list = []
            topic_list.append(topic_id)

        response["topic_list"] = topic_list
        response["topic_subscriptions"] = {}

        for topic_id in topic_list:
            topic_path = self.publisher.topic_path(self.project_id, topic_id)
            list_topic_subscriptions = self.publisher.list_topic_subscriptions(request={"topic": topic_path})
            for subscription in list_topic_subscriptions:
                topic_subscriptions.append(subscription)

            response["topic_subscriptions"][topic_id] = topic_subscriptions

        return response

    # used google cloud rest api with python request module
    def create_composer_env(self, composer_env_config):

        composer_env_config_dict = json.loads(composer_env_config.replace('\n', ''))
        composer_env_name = composer_env_config_dict.get("name", "").split("/")[-1]
        location = composer_env_config_dict.get("name", "").split("/")[-3]
        out = self.get_composer_env(composer_env_name, location)
        if out.get("composer_env_name", "") == composer_env_name:
            return {"Reason": "Same composer environment in same location already exists"}
        else:
            parent = f"projects/{self.project_id}/locations/{self.region}"
            base_url = f"https://composer.googleapis.com/v1beta1/{parent}/environments"

            response = requests.post(base_url, data=composer_env_config, headers=self.rest_api_headers)
            return response.json()

    def update_composer_env(self, composer_env_config, updatemask, updatemask_config):
        composer_env_config_dict = json.loads(composer_env_config.replace('\n', ''))
        composer_env_name = composer_env_config_dict.get("name", "").split("/")[-1]
        location = composer_env_config_dict.get("name", "").split("/")[-3]

        name = f"projects/{self.project_id}/locations/{location}/environments/{composer_env_name}"
        base_url = f"https://composer.googleapis.com/v1beta1/{name}"

        response = requests.get(base_url, headers=self.rest_api_headers)
        if response.json().get("name", "").split("/")[-1].upper() == composer_env_name.upper():
            params = {
                "updateMask": updatemask
            }
            req = PreparedRequest()
            req.prepare_url(base_url, params)
            update_response = requests.patch(req.url, data=updatemask_config, headers=self.rest_api_headers)
        return update_response.json()

    def get_composer_env(self, composer_env_name=None, location=None):

        parent = f"projects/{self.project_id}/locations/{self.region}"
        base_url = f"https://composer.googleapis.com/v1beta1/{parent}/environments"

        response = requests.get(base_url, headers=self.rest_api_headers)
        if composer_env_name is not None and location is not None:
            composer_env_details = {}
            for item in response.json().get("environments", []):
                comp_name = item.get("name", "").split("/")[-1]
                comp_location = item.get("name", "").split("/")[-3]
                if (composer_env_name.upper() == comp_name.upper()) and (location.upper() == comp_location.upper()):
                    composer_env_details["composer_env_name"] = composer_env_name
                    composer_env_details["composer_location"] = location
                    composer_env_details["composer_details"] = item
                    break
            return composer_env_details
        else:
            return response.json()

    def create_secret(self, secret_id, secret_data):
        parent = f"projects/{self.project_id}"
        secret = self.secret_client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        version = self.secret_client.add_secret_version(
            request={"parent": secret.name, "payload": {"data": secret_data}}
        )
        return str(secret.name) + "_" + str(version)

    def clean_up(self):
        """
        gcloud pubsub subscriptions delete my-sub
        gcloud pubsub topics delete my-topic
        """
        pass


if __name__ == "__main__":
    file_name = sys.argv[0]
    print(f"{file_name} has been started executing...")
    current_path = os.path.dirname(__file__)
    print(f"current_path: {current_path}")
    current_file = os.path.realpath(__file__)
    print(f"current_file: {current_file}")

    env = "DEV"
    config = configparser.ConfigParser()
    config.read(f"{current_path}/config.properties")

    input_dict = {}
    input_dict["composer_env_config"] = config[env]["config"]

    input_dict["updatemask_pypiPackages"] = config.get(env, "updatemask_pypiPackages").split(", ")[:]
    updatemask_pypiPackages = ["config.softwareConfig.pypiPackages." + str(i) for i in
                               input_dict["updatemask_pypiPackages"]]
    input_dict['updatemask_config_pypiPackages'] = config[env]["updatemask_config_pypiPackages"]

    input_dict["updatemask_airflowConfig"] = config.get(env, "updatemask_airflowConfig").split(", ")[:]
    updatemask_airflowConfig = ["config.softwareConfig.airflowConfigOverrides." + str(i) for i in
                                input_dict["updatemask_airflowConfig"]]
    input_dict['updatemask_config_airflowConfig'] = config[env]["updatemask_config_airflowConfig"]

    # input_dict["updatemask_envvariables"] = config.get(env, "updatemask_envvariables").split(", ")[:]
    updatemask_envvariables = "config.softwareConfig.envVariables"
    input_dict['updatemask_config_envvariables'] = config[env]["updatemask_config_envvariables"]

    obj = GCP_Infra_Utility()
    print(f"project_id: {obj.project_id}")

    # # create topic
    # out = obj.create_pubsub_topic("test-topic")
    # print(f"{out}")

    # # get topic details
    # out = obj.get_pubsub_topic()
    # print(f"{out}")

    ## if you specify the composer config in same file, follow below
    # input_dict['composer_env_config'] = """{
    #                                           "config": {
    #                                           }
    #                                        }"""

    # create composer env
    # out = obj.create_composer_env(input_dict['composer_env_config'])
    # print(f"{out}")

    # update composer env for pypipackage installation
    # out = obj.update_composer_env(input_dict['composer_env_config'],
    #     updatemask_pypiPackages, input_dict['updatemask_config_pypiPackages'])
    # print(f"{out}")

    # update composer env for airflowconfig override
    # out = obj.update_composer_env(input_dict['composer_env_config'],
    #     updatemask_airflowConfig, input_dict['updatemask_config_airflowConfig'])
    # print(f"{out}")

    # update composer env for composer env variable
    # out = obj.update_composer_env(input_dict['composer_env_config'],
    #     updatemask_envvariables, input_dict['updatemask_config_envvariables'])
    # print(f"{out}")

    # get composer env list
    # out = obj.get_composer_env(composer_env_name="test", location="us-central1")
    # print(f"{out}")

    # create secret
    # out1 = obj.create_secret("airflow-connections-sendgrid_default", b"sendgrid://apikey:SG.A20nM@smtp.sendgrid.net:587")
    # print(f"secret1: {out1} created")
    # out2 = obj.create_secret("airflow-variables-from_email", b"indranil.pal.test@gmail.com")
    # print(f"secret2: {out2} created")
