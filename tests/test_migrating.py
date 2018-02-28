from unittest import mock
import pytest


@pytest.fixture
def apps():
    """ Mocks 'apps.get_model()' parameter in migration """
    from .models import DummyModel
    mocked_apps = mock.MagicMock()
    mocked_apps.get_model = mock.MagicMock(return_value=DummyModel)
    return mocked_apps


@pytest.fixture
def schema_editor():
    """ Mocks 'schema_editor.execute()' in migration """
    mocked_schema_editor = mock.MagicMock()
    mocked_schema_editor.execute = mock.MagicMock()
    return mocked_schema_editor


def test_AddAuditToModel_upgrade(apps, schema_editor):
    """ It should emit proper upgrade query for specified model """
    from audit_trail.migrating import AddAuditToModel as Operation
    operation = Operation('DummyModel', 'tests')
    operation.code(apps, schema_editor)
    schema_editor.execute.assert_called_with(
        "SELECT audit.audit_table('tests_dummymodel', 't', 't', '{}')")


def test_AddAuditToModel_upgrade_exclude_sql(apps, schema_editor):
    """ It should allow omission of SQL in audit log """
    from audit_trail.migrating import AddAuditToModel as Operation
    operation = Operation('DummyModel', 'tests', include_query=False)
    operation.code(apps, schema_editor)
    schema_editor.execute.assert_called_with(
        "SELECT audit.audit_table('tests_dummymodel', 't', 'f', '{}')")


def test_AddAuditToModel_upgrade_exclude_cols(apps, schema_editor):
    """ It should allow exclusion of certain columns """
    from audit_trail.migrating import AddAuditToModel as Operation
    operation = Operation('DummyModel', 'tests', exclude=['id'])
    operation.code(apps, schema_editor)
    schema_editor.execute.assert_called_with(
        "SELECT audit.audit_table('tests_dummymodel', 't', 't', '{id}')")


def test_AddAuditToModel_downgrade(apps, schema_editor):
    """ It should downgrade """
    from audit_trail.migrating import AddAuditToModel as Operation
    operation = Operation('DummyModel', 'tests', exclude=['id'])
    operation.reverse_code(apps, schema_editor)
    assert schema_editor.execute.mock_calls == [
        mock.call('DROP TRIGGER IF EXISTS audit_trigger_row ON tests_dummymodel'),
        mock.call('DROP TRIGGER IF EXISTS audit_trigger_stm ON tests_dummymodel')
    ]
