import pytest


@pytest.fixture
def site():
    from django.contrib.admin.sites import AdminSite
    return AdminSite()


class MockRequest(object):
    pass


request = MockRequest()


def test_AuditTrailAdmin_str(site):
    from audit_trail.admin import AuditTrailAdmin
    from audit_trail.models import Log
    admin = AuditTrailAdmin(Log, site)
    assert str(admin) == 'audit_trail.AuditTrailAdmin'


def test_AuditTrailAdmin_list_display(site):
    """ It should list record columns """

    import datetime
    from audit_trail.admin import AuditTrailAdmin
    from audit_trail.models import Log

    log = Log(
        id=1,
        schema_name='public',
        table_name='recipes',
        relid=123,
        session_user_name='app',
        current_user_name='authorized_user',
        action_tstamp_tx=datetime.datetime.now(),
        action_tstamp_stm=datetime.datetime.now(),
        action_tstamp_clk=datetime.datetime.now(),
        transaction_id=9001,
        client_addr='127.0.0.1',
        client_query='SELECT 1',
        application_name='test',
        application_user_name='tester@localhost.local',
        action='I',
        row_data={},
        changed_fields={},
        statement_only=False
    )
    admin = AuditTrailAdmin(Log, site)

    fields = list(admin.get_fields(request, log))
    assert fields == """
        id
        schema_name
        table_name
        relid
        session_user_name
        current_user_name
        action_tstamp_tx
        action_tstamp_stm
        action_tstamp_clk
        transaction_id
        client_addr
        client_query
        application_name
        application_user_name
        action
        row_data
        changed_fields
        statement_only
    """.split()
