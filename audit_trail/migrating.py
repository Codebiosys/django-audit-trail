from django.db import migrations


def AddAuditToModel(name, app_label=None, include_query=True, exclude=[]):
    """ Enables auditing for the generated table

    This method will return all callback for Django migrations to attach
    a trigger to the postgres database table specified by name and app_label.

    :param name: Django model name
    :type name: str
    :param app_label: Django app location of model
    :type app_label: str
    :param include_query: Include the query in the audit? (Default: True)
    :type include_query: bool
    :param exclude: list of columns to omit from the audit record (e.g. blobs)
    :type include_query: list

    :returns: migrations.RunPython -- A migration for the model
    """

    def _get_table(apps, schema_editor):
        Model = apps.get_model(app_label, name)
        table = Model._meta.db_table
        return table

    def upgrade(apps, schema_editor):
        table = _get_table(apps, schema_editor)
        include_query_sql = 't' if include_query else 'f'
        exclude_sql = ','.join(exclude)
        query = ' '.join(f"""
            SELECT audit.audit_table('{table}', 't', '{include_query_sql}', '{{{exclude_sql}}}')
        """.split())
        schema_editor.execute(query)

    def downgrade(apps, schema_editor):
        table = _get_table(apps, schema_editor)
        schema_editor.execute(f"DROP TRIGGER IF EXISTS audit_trigger_row ON {table}")
        schema_editor.execute(f"DROP TRIGGER IF EXISTS audit_trigger_stm ON {table}")

    return migrations.RunPython(upgrade, downgrade)
