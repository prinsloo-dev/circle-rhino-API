"""create quotes table

Revision ID: 61669e80e612
Revises: 37abb4c7f6ee
Create Date: 2024-04-10 15:56:07.801833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61669e80e612'
down_revision: Union[str, None] = '37abb4c7f6ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'quotes_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE quotes_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'quotes_quote_no_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE quotes_quote_no_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.quotes
        (
            id integer NOT NULL DEFAULT nextval('quotes_id_seq'::regclass),
            lock boolean,
            quote_date timestamp with time zone,
            fitment_date date,
            completion_date date,
            total_price numeric(9,2),
            customers_id integer,
            status text COLLATE pg_catalog."default",
            fitment_address text COLLATE pg_catalog."default",
            status_reason text COLLATE pg_catalog."default",
            contacts_id integer,
            quote_no integer DEFAULT nextval('quotes_quote_no_seq'::regclass)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.quotes
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.quotes;
        """
    )
