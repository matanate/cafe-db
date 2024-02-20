"""First

Revision ID: af9d3bbfe5f6
Revises: 
Create Date: 2024-02-19 11:35:26.272008

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "af9d3bbfe5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("cafe", schema=None) as batch_op:
        batch_op.alter_column(
            "id", existing_type=sa.INTEGER(), nullable=False, autoincrement=True
        )
        batch_op.alter_column(
            "name",
            existing_type=sa.TEXT(length=250),
            type_=sa.String(length=250),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "map_url",
            existing_type=sa.TEXT(length=500),
            type_=sa.String(length=500),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "img_url",
            existing_type=sa.TEXT(length=500),
            type_=sa.String(length=500),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "location",
            existing_type=sa.TEXT(length=250),
            type_=sa.String(length=250),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "seats",
            existing_type=sa.TEXT(length=250),
            type_=sa.String(length=250),
            nullable=False,
        )
        batch_op.alter_column(
            "coffee_price",
            existing_type=sa.TEXT(length=250),
            type_=sa.String(length=250),
            existing_nullable=True,
        )
        batch_op.create_unique_constraint("uq_cafe_name", ["name"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("cafe", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")
        batch_op.alter_column(
            "coffee_price",
            existing_type=sa.String(length=250),
            type_=sa.TEXT(length=250),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "seats",
            existing_type=sa.String(length=250),
            type_=sa.TEXT(length=250),
            nullable=True,
        )
        batch_op.alter_column(
            "location",
            existing_type=sa.String(length=250),
            type_=sa.TEXT(length=250),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "img_url",
            existing_type=sa.String(length=500),
            type_=sa.TEXT(length=500),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "map_url",
            existing_type=sa.String(length=500),
            type_=sa.TEXT(length=500),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=250),
            type_=sa.TEXT(length=250),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "id", existing_type=sa.INTEGER(), nullable=True, autoincrement=True
        )

    # ### end Alembic commands ###
