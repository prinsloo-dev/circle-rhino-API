"""create quote_lines table

Revision ID: 0cd833c595c7
Revises: af1d1c13a1c2
Create Date: 2024-04-10 16:03:37.853403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cd833c595c7'
down_revision: Union[str, None] = 'af1d1c13a1c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'quote_lines_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE quote_lines_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.quote_lines
        (
            id integer NOT NULL DEFAULT nextval('quote_lines_id_seq'::regclass),
            lock boolean,
            price numeric(9,2),
            quotes_id integer,
            products_id integer,
            status text COLLATE pg_catalog."default",
            name text COLLATE pg_catalog."default",
            description text COLLATE pg_catalog."default",
            size text COLLATE pg_catalog."default",
            quantity integer,
            jobs_id integer
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.quote_lines
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.quote_lines;
        """
    )
