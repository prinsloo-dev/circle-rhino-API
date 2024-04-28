"""create products table

Revision ID: 73671d2374db
Revises: ed9b8fdb4c85
Create Date: 2024-04-07 13:08:12.174902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73671d2374db'
down_revision: Union[str, None] = 'ed9b8fdb4c85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'products_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE products_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.products
        (
            id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),
            lock boolean,
            price numeric(9,2) DEFAULT 0.0,
            item_name text COLLATE pg_catalog."default",
            description text COLLATE pg_catalog."default"
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.products
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.products;
        """
    )
