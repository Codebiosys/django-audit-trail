def test_app_is_loaded():
    """ It should ensure that the Audit app is installed. """
    from django.conf import settings
    from audit_trail.apps import AuditTrailConfig as config
    assert config.name in settings.INSTALLED_APPS
