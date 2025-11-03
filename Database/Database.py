from __future__ import annotations

import os
from typing import Generator, Any, Dict
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from .DatabaseInserter import DatabaseInserter
from .DatabaseUpdater import DatabaseUpdater
from .DatabaseDeleter import DatabaseDeleter
from .DatabaseLoader import DatabaseLoader
################################################################################

__all__ = ("Database", )

################################################################################
class Database:

    __slots__ = (
        "_engine",
        "_inserter",
        "_updater",
        "_deleter",
        "_loader",
        "_session",
    )

################################################################################
    def __init__(self, debug: bool) -> None:

        self._engine: Engine = create_engine(
            os.getenv("DEV_DATABASE_URL")
            if debug
            else os.getenv("PROD_DATABASE_URL"),
            echo=debug
        )
        self._session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

        self._inserter: DatabaseInserter = DatabaseInserter(self)
        self._updater: DatabaseUpdater = DatabaseUpdater(self)
        self._deleter: DatabaseDeleter = DatabaseDeleter(self)
        self._loader: DatabaseLoader = DatabaseLoader(self)

################################################################################
    @property
    def insert(self) -> DatabaseInserter:

        return self._inserter

################################################################################
    @property
    def update(self) -> DatabaseUpdater:

        return self._updater

################################################################################
    @property
    def delete(self) -> DatabaseDeleter:

        return self._deleter

################################################################################
    @contextmanager
    def get_db(self) -> Generator[Session | Any, Any, None]:

        db = self._session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

################################################################################
    def load_all(self) -> Dict[str, Any]:

        return self._loader.load_all()

################################################################################
