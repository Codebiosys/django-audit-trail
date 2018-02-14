from django.db import models

from django.contrib.postgres import fields as postgres


class AuditLog(models.Model):
    """ Audit logging table.

    This table is reflected from the existing audit log
    extension table. These records are read-only to the application for history
    tracking purposes.

    See: https://github.com/m-martinez/pg-audit-json.git
    """
    class Meta:
        managed = False
        db_table = '"audit"."log"'

    id = models.BigIntegerField(
        primary_key=True,
        help_text='Unique identifier for each auditable event'
        )
    schema_name = models.TextField(
        help_text='Database schema audited table for this event is in'
        )
    table_name = models.TextField(
        help_text='Non-schema-qualified table name of table occurred in'
        )
    relid = models.IntegerField(
        help_text='Table OID. Changes with drop/create.'
        )
    session_user_name = models.TextField(
        help_text='Login/session user whose statement caused the audited event'
        )
    current_user_name = models.TextField(
        help_text=(
            'Effective user that cased audited event '
            '(if authorization level changed)')
        )
    action_tstamp_tx = models.DateTimeField(
        help_text=(
            'Transaction start timestamp for transaction in which '
            'audited event occurred')
        )
    action_tstamp_stm = models.DateTimeField(
        help_text=(
            'Wall clock time at which audited event\'s trigger call occurred')
        )
    action_tstamp_clk = models.DateTimeField(
        help_text=(
            'Statement start timestamp for tx in which audited event occurred')
        )
    transaction_id = models.BigIntegerField(
        help_text=(
            'Identifier of transaction that made the change. '
            'Unique when paired with action_tstamp_tx.')
        )
    client_addr = models.GenericIPAddressField(
        null=True,
        help_text=(
            'IP address of client that issued query. '
            'Undefined for unix socket.')
        )
    client_query = models.TextField(
        help_text=(
            'Top-level query that caused this auditable event. '
            'May be more than one.')
        )
    application_name = models.TextField(
        help_text=(
            'Client-set session application name when this audit '
            'event occurred.')
        )
    application_user_name = models.TextField(
        help_text=(
            'Client-set session application user when this audit '
            'event occurred')
        )
    action = models.TextField(
        help_text='Action type'
        )
    row_data = postgres.JSONField(
        help_text=(
            'Record value. Null for statement-level trigger. '
            'For INSERT this is null becuase there was nothing there before. '
            'For DELETE and UPDATE it is the old tuple.')
        )
    changed_fields = postgres.JSONField(
        help_text=(
            'New values of fields for INSERT or those changed by '
            'UPDATE (i.e a diff). Null for DELETE.')
        )
    statement_only = models.BooleanField(
        help_text=(
            'TRUE if audit event is from an FOR EACH STATEMENT trigger. '
            'FALSE for FOR EACH ROW.')
        )

    def __str__(self):
        return (
            f'{self.schema_name}.{self.table_name}({self.id}) '
            f'by {self.session_user_name} '
            f'on {self.action_tstamp_tx}'
        )
