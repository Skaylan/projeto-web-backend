from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '6eb475684edf'
down_revision = '802eed544462'
branch_labels = None
depends_on = None


def get_foreign_keys(table_name):
    """Função para pegar todas as chaves estrangeiras de uma tabela."""
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    return inspector.get_foreign_keys(table_name)


def upgrade():
    foreign_keys = get_foreign_keys('movie')
    fk_exists = any(fk['name'] == 'fk_movie_category' for fk in foreign_keys)
    
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('movie_id', sa.String(), nullable=False))
        batch_op.create_foreign_key(
            'fk_category_movie',
            'movie',
            ['movie_id'],
            ['id']
        )

    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.alter_column('banner_img_id',
                              existing_type=sa.VARCHAR(),
                              type_=sa.Text(),
                              existing_nullable=False)
        batch_op.alter_column('poster_img_id',
                              existing_type=sa.VARCHAR(),
                              type_=sa.Text(),
                              existing_nullable=False)
        
        if fk_exists:
            batch_op.drop_constraint('fk_movie_category', type_='foreignkey')
        
        batch_op.drop_column('category_id')


def downgrade():
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.VARCHAR(), nullable=False))
        batch_op.create_foreign_key(
            'fk_movie_category',
            'category',
            ['category_id'],
            ['id']
        )
        batch_op.alter_column('poster_img_id',
                              existing_type=sa.Text(),
                              type_=sa.VARCHAR(),
                              existing_nullable=False)
        batch_op.alter_column('banner_img_id',
                              existing_type=sa.Text(),
                              type_=sa.VARCHAR(),
                              existing_nullable=False)

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_constraint('fk_category_movie', type_='foreignkey')
        batch_op.drop_column('movie_id')

