"""empty message

Revision ID: 4cc577d6018e
Revises: 
Create Date: 2023-07-04 22:33:06.809860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cc577d6018e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('surname', sa.String(length=15), nullable=False),
    sa.Column('patronymic', sa.String(length=15), nullable=True),
    sa.Column('phone', sa.BigInteger(), nullable=False),
    sa.Column('photo', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=False),
    sa.Column('user_role', sa.Enum('ADMIN', 'PATIENT', 'DOCTOR', name='userrole'), nullable=True),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('verification_codes',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('phone_number', sa.BigInteger(), nullable=False),
    sa.Column('verification_code', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('doctors',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('info', sa.String(length=100), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('specialization', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tokens',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('expires', sa.TIMESTAMP(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('day_appointments',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('doctor_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('appointments',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.TIMESTAMP(), nullable=False),
    sa.Column('anamnesis', sa.String(length=1000), nullable=True),
    sa.Column('day_appointments_id', sa.BigInteger(), nullable=True),
    sa.Column('patient_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['day_appointments_id'], ['day_appointments.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointments')
    op.drop_table('day_appointments')
    op.drop_table('tokens')
    op.drop_table('patients')
    op.drop_table('doctors')
    op.drop_table('verification_codes')
    op.drop_table('users')
    # ### end Alembic commands ###