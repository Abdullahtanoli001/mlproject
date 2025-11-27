## End to end MAchine Learning Projects


import dagshub
dagshub.init(repo_owner='Abdullahtanoli001', repo_name='mlproject', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1) 