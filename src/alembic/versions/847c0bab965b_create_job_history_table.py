"""create job_history table

Revision ID: 847c0bab965b
Revises: 0cd833c595c7
Create Date: 2024-04-10 16:08:30.975601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '847c0bab965b'
down_revision: Union[str, None] = '0cd833c595c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'jobs_history_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE jobs_history_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.jobs_history
        (
            id integer NOT NULL DEFAULT nextval('jobs_history_id_seq'::regclass),
            lock boolean,
            action_date timestamp with time zone,
            jobs_id integer,
            departments_id integer,
            owner_employees_id integer,
            status text COLLATE pg_catalog."default",
            comment text COLLATE pg_catalog."default",
            payment_id integer,
            action_user text COLLATE pg_catalog."default"
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.jobs_history
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.jobs_history;
        """
    )