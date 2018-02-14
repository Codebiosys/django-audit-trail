def test_app_is_loaded():
    """ It should ensure that the Audit app is installed. """
    from django.conf import settings
    from auditing.apps import AuditingConfig as config
    assert config.name in settings.INSTALLED_APPS
