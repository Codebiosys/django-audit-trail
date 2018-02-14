import pytest


@pytest.fixture
def site():
    from django.contrib.admin.sites import AdminSite
    return AdminSite()


class MockRequest(object):
    pass


request = MockRequest()


def test_AuditingAdmin_str(site):
    from auditing.admin import AuditingAdmin
    from auditing.models import AuditLog
    admin = AuditingAdmin(AuditLog, site)
    assert str(admin) == 'auditing.AuditingAdmin'


def test_AuditingAdmin_list_display(site):
    """ It should list record columns """

    import datetime
    from auditing.admin import AuditingAdmin
    from auditing.models import AuditLog

    log = AuditLog(
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
    admin = AuditingAdmin(AuditLog, site)

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
