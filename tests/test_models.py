import pytest


@pytest.mark.django_db
def test__str__(client):
    """ It should be able to return a string overview of the record

    Note that we will never have to manually create an AuditLog record
    as the model only serves as a read-only client to the audit log table.

    """
    import datetime
    from auditing import models
    record = models.AuditLog(
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
    assert str(record) == (
        f'{record.schema_name}.{record.table_name}({record.id}) '
        f'by {record.session_user_name} '
        f'on {record.action_tstamp_tx}'
    )
