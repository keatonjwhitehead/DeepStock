from googleapiclient import discovery
from googleapiclient import errors
import json
import subprocess
import logging
import time

class AIPlatformModel:
	def __init__(self, project_id):
		self._project_id = project_id
		self._service = discovery.build('ml', 'v1')

	def upload_to_bucket(self, local_path, gcs_path):
		subprocess.call("gsutil -m cp -r {} {}".format(local_path, gcs_path), shell=True)

	def model_exists(self, model_name):
		logging.info('Creating model {}'.format(model_name))
		models = self._service.projects().models()
		try:
			response = models.list(parent='projects/{}'.format(self._project_id)).execute()
			if response:
				for model in response['models']:
					print(model['name'])
					if model['name'].rsplit('/', 1)[1] == model_name:
						return True
				return False
		except errors.HttpError as err:
			logging.error('%s', json.loads(err.content.decode('utf-8'))['error']['message'])

	def create_model(self, model_name):
		if not self.model_exists(model_name):
			body = {
				'name': model_name,
				'regions': 'us-central1',
				'description': 'MLflow model'
			}
			parent = 'projects/{}'.format(self._project_id)
			try:
				service_request = self._service.projects().models().create(
					parent=parent, body=body).execute()
			except errors.HttpError as err:
				logging.error('"%s". Skipping model creation.', json.loads(err.content.decode('utf-8'))['error']['message'])
		else:
			logging.warning('{} already exists'.format(model_name))

	def deploy_model(self, model_path, model_name, model_version):
		model_version = 'mflow_{}'.format(model_version)
		try:
			model_versions = self._service.projects().models().versions().list(
				parent='projects/{}/models/{}'.format(self._project_id, model_name)).execute()
		except errors.HttpError as err:
			logging.error('%s', json.loads(err.content.decode('utf-8'))['error']['message'])

		model_version_exists = False
		if model_versions:
			for version in model_versions['versions']:
				if version['name'].rsplit('/', 1)[1] == model_version:
					model_version_exists = True

		if not model_version_exists:
			body = {
				'name': model_version,
				'deploymentUri': model_path,
				'framework': 'TENSORFLOW',
				'runtimeVersion': '1.14',
				'pythonVersion': '3.5',
			}
			parent = 'projects/{}/models/{}'.format(self._project_id, model_name)
			deploy_success = False
			try:	
				response = self._service.projects().models().versions().create(
					parent=parent, body=body).execute()
				op_name = response['name']
				while True:
					deploy_status = self._service.projects().operations().get(name=op_name).execute()
					if deploy_status.get('done'):
						logging.info('Model {} with version {} deployed.'.format(model_name, model_version))
						deploy_success = True
						break
					if deploy_status.get('error'):
						logging.error(deploy_status['error'])
						raise RuntimeError('Failed to deploy model for serving: {}'.format(deploy_status['error']))
					logging.info('Waiting for %d seconds for "%s" with "%s" version to be deployed.',
						10, model_name,
						model_version)
					time.sleep(10)
			except errors.HttpError as err:
				logging.error('"%s". Unable to deploy model', json.loads(err.content.decode('utf-8'))['error']['message'])
		
			if deploy_success:
				try:
					response = self._service.projects().models().versions().setDefault(name='{}/versions/{}'.format(parent, model_version)).execute()
				except errors.HttpError as err:
					logging.error('"%s". Unable to set model as default', json.loads(err.content.decode('utf-8'))['error']['message'])

		else:
			logging.warning('Model {} with version {} already exists'.format(model_name, model_version))