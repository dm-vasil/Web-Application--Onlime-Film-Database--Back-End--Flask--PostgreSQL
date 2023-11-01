"""empty message

Revision ID: 344f109610ad
Revises: fcfc04752147
Create Date: 2022-02-07 18:53:10.687359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '344f109610ad'
down_revision = 'fcfc04752147'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('film_by_countries')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film_by_countries',
    sa.Column('film_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], name='film_by_countries_film_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.name'], name='film_by_countries_genre_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('film_id', 'genre_id', name='film_by_countries_pkey')
    )
    # ### end Alembic commands ###
