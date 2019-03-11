class _BaseDeploymentConfiguration:
    result_expire = 3600
    timezone = ['Asia/Shanghai']
    include = ['app.performance_baseline_tasks',
               'app.hello_tasks']