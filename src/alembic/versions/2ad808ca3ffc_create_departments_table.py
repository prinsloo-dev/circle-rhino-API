"""create departments table

Revision ID: 2ad808ca3ffc
Revises: 73671d2374db
Create Date: 2024-04-07 13:16:50.796968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ad808ca3ffc'
down_revision: Union[str, None] = '73671d2374db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'departments_id_seq' AND relkind = 'S') THEN
                CREATE SEQUENCE departments_id_seq START 1;
            END IF;
        END$$;
    """)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS public.departments
        (
            id integer NOT NULL DEFAULT nextval('departments_id_seq'::regclass),
            name text COLLATE pg_catalog."default",
            entity_name text COLLATE pg_catalog."default",
            lock boolean
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.departments
            OWNER to postgres;
        """
    )


def downgrade() -> None:
        op.execute(
        """
        DROP TABLE IF EXISTS public.departments;
        """
    )
