"""create jobs table

Revision ID: af1d1c13a1c2
Revises: 61669e80e612
Create Date: 2024-04-10 16:00:53.151816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af1d1c13a1c2'
down_revision: Union[str, None] = '61669e80e612'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'jobs_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE jobs_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'jobs_job_no_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE jobs_job_no_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.jobs
        (
            id integer NOT NULL DEFAULT nextval('jobs_id_seq'::regclass),
            lock boolean,
            job_date timestamp with time zone,
            job_no integer NOT NULL DEFAULT nextval('jobs_job_no_seq'::regclass)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.jobs
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.jobs;
        """
    )
