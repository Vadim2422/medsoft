from src.utils.unitofwork import UnitOfWork, IUnitOfWork


class BaseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
