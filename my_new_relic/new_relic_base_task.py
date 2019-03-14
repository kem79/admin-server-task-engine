from celery import Task
import os


class NewRelicBaseTask(Task):

    _api_key = None
    _admin_api_key = None
    _applications = None

    @property
    def api_key(self):
        if self._api_key:
            return self._api_key
        self._api_key = os.getenv('NEW_RELIC_API_KEY', '2273150b68d110bf1e1036e56c46607db519dd91ece4800')
        return self._api_key

    @property
    def admin_api_key(self):
        if self._admin_api_key:
            return self._admin_api_key
        self._admin_api_key = os.getenv('NEW_RELIC_API_KEY', 'f15de6949525e4aa37bf38aa0311074e')
        return self._admin_api_key
