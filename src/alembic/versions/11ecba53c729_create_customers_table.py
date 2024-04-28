"""create customers table

Revision ID: 11ecba53c729
Revises: 2ad808ca3ffc
Create Date: 2024-04-07 13:19:52.224116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11ecba53c729'
down_revision: Union[str, None] = '2ad808ca3ffc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'customers_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE customers_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.customers
        (
            id integer NOT NULL DEFAULT nextval('customers_id_seq'::regclass),
            lock boolean,
            address text COLLATE pg_catalog."default",
            company_name text COLLATE pg_catalog."default"
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.customers
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.customers;
        """
    )
