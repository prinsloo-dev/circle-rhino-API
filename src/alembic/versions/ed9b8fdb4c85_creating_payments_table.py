"""creating payments table

Revision ID: ed9b8fdb4c85
Revises: be1e33f26925
Create Date: 2024-04-07 12:34:43.461411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed9b8fdb4c85'
down_revision: Union[str, None] = 'be1e33f26925'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'payment_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE payment_id_seq START 1;
            END IF;
        END$$;
    """)

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.payment
        (
            id integer NOT NULL DEFAULT nextval('payment_id_seq'::regclass),
            lock boolean,
            paytype text COLLATE pg_catalog."default"
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.payment
            OWNER to postgres;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS public.payment;
        """
    )
