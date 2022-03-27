from django.http import JsonResponse
from .models import LogRegModel
import google.auth
import os
from google.cloud import bigquery


def get_score(request):
    if request.method == 'GET':
        model_name = request.GET.get('model_name')
        session_id = request.GET.get('session_id')
        model = LogRegModel.objects.get(model_name=model_name)
        scoring_sql = model.sql_text + f'\nwhere session_id={session_id}'

        key_path = 'tabbyai-sa-test-key.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
        credentials, your_project_id = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        bqclient = bigquery.Client(credentials=credentials, project=your_project_id)
        result = bqclient.query(scoring_sql).result().to_dataframe()

        if result.shape[0]:
            result_first_row = result.iloc[0]
            result_json = result_first_row.to_json()

            return JsonResponse(result_json)
