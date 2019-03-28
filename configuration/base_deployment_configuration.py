class _BaseDeploymentConfiguration:
    result_expire = 300
    timezone = ['Asia/Shanghai']
    include = ['app.performance_baseline_tasks',
               'app.hello_tasks']