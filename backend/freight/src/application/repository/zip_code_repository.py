from abc import abstractmethod

from freight.src.domain.entity.zip_code import ZIPCode


class ZIPCodeRepository:
    @abstractmethod
    def get(self, code: str) -> ZIPCode:
        pass
