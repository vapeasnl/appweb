from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf1e510d1444'
down_revision = 'fc62f3a90bd8'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key constraint from event table
    op.drop_constraint('event_ibfk_1', 'event', type_='foreignkey')
    
    # Drop the association table if it exists
    op.drop_table('association')
    
    # Create the association table with the new structure
    op.create_table('association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    
    # Recreate the foreign key constraint on event table
    op.create_foreign_key('event_ibfk_1', 'event', 'association', ['association_id'], ['id'])
    
    # Drop the index 'name' if it exists
    index_exists = op.execute("SHOW INDEX FROM association WHERE Key_name = 'name'")
    if index_exists and index_exists.fetchone():
        op.drop_index('name', table_name='association')


def downgrade():
    # Drop foreign key constraint from event table
    op.drop_constraint('event_ibfk_1', 'event', type_='foreignkey')
    
    # Drop the association table
    op.drop_table('association')
    
    # Recreate the association table with the old structure
    op.create_table('association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    
    # Recreate the foreign key constraint on event table
    op.create_foreign_key('event_ibfk_1', 'event', 'association', ['association_id'], ['id'])
    
    # Create the index 'name' if needed
    index_exists = op.execute("SHOW INDEX FROM association WHERE Key_name = 'name'")
    if index_exists and not index_exists.fetchone():
        op.create_index('name', 'association', ['name'], unique=True)

