"""create contacts table

Revision ID: 37abb4c7f6ee
Revises: 9badcb01f109
Create Date: 2024-04-10 15:54:14.703498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37abb4c7f6ee'
down_revision: Union[str, None] = '9badcb01f109'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'contacts_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE contacts_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.contacts
        (
            id integer NOT NULL DEFAULT nextval('contacts_id_seq'::regclass),
            lock boolean,
            customers_id integer,
            contact_person text COLLATE pg_catalog."default",
            tel_no text COLLATE pg_catalog."default",
            email text COLLATE pg_catalog."default",
            contact_role text COLLATE pg_catalog."default"
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.contacts
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.contacts;
        """
    )
