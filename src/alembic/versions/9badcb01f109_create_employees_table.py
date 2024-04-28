"""create employees table

Revision ID: 9badcb01f109
Revises: 11ecba53c729
Create Date: 2024-04-10 15:51:41.896730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9badcb01f109'
down_revision: Union[str, None] = '11ecba53c729'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'employees_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE employees_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.employees
        (
            id integer NOT NULL DEFAULT nextval('employees_id_seq'::regclass),
            lock boolean,
            appointment_date date,
            termination_date date,
            home_address text COLLATE pg_catalog."default",
            tel_no text COLLATE pg_catalog."default",
            email text COLLATE pg_catalog."default",
            name text COLLATE pg_catalog."default",
            surname text COLLATE pg_catalog."default",
            departments_id integer,
            employee_no text COLLATE pg_catalog."default",
            sa_id_number text COLLATE pg_catalog."default"
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.employees
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.employees;
        """
    )

