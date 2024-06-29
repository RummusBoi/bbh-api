from dataclasses import dataclass
from enum import Enum, IntEnum
import os

INIT_DB_STRING = "pg_ctl -D {folder} init"
START_DB_STRING = "pg_ctl -D {folder} -l logfile.txt start"
STOP_DB_STRING = "pg_ctl -D {folder} stop"
STATUS_DB_STRING = "pg_ctl -D {folder} status"
DB_NAME = "postgres"


class ColumnType(Enum):
    VarChar = "varchar(255)"
    U8Vec = "bytea"
    I32Vec = "integer[]"
    Integer = "integer"
    BigInteger = "bigint"
    Float32 = "real"


class DbStatus(IntEnum):
    Running = 0
    Down = 768
    NonExistant = 1024


@dataclass
class ColumnDecl:
    name: str
    type: ColumnType


@dataclass
class TableDecl:
    name: str
    primary_keys: list[ColumnDecl]
    columns: list[ColumnDecl]


# we want a mapping (b, f, g -> endstate, n_ims, d_min, e_bs)
table_decls: list[TableDecl] = [
    TableDecl(
        name="simresults",
        primary_keys=[
            ColumnDecl(name="b", type=ColumnType.Float32),
            ColumnDecl(name="f", type=ColumnType.Float32),
            ColumnDecl(name="g", type=ColumnType.Float32),
        ],
        columns=[
            ColumnDecl(name="endstate", type=ColumnType.Integer),
            ColumnDecl(name="n_ims", type=ColumnType.Integer),
            ColumnDecl(name="d_min", type=ColumnType.Float32),
            ColumnDecl(name="e_bs", type=ColumnType.Float32),
        ],
    )
]


def run_sql_command(command: str) -> None:
    """
    Will run the os command 'psql {DB_NAME} -c {command}'.
    Raises an exception if the exit code is non-zero
    """
    full_command = f"psql {DB_NAME} -c {command}"
    print(f"Running command {full_command}")
    exit_code = os.system(full_command)
    print(f"Exit code: {exit_code}")
    if not exit_code == 0:
        print("--- WARNING --- ")
        print(f"Command return non-zero exit code ({exit_code}) ")


def drop_table(table: str) -> None:
    run_sql_command(f"'DROP table {table};'")


def create_table(table_decl: TableDecl) -> None:
    print(f"Creating table {table_decl.name}")
    all_columns = table_decl.primary_keys + table_decl.columns
    primary_keys = ", ".join([column.name for column in table_decl.primary_keys])
    columns_formatted = ",\n".join(
        [f"{column.name} {column.type.value}" for column in all_columns]
        + [f"PRIMARY KEY ({primary_keys})"]
    )

    query = f"""'CREATE TABLE IF NOT EXISTS {table_decl.name} (
    {columns_formatted}
);'"""

    run_sql_command(query)


def try_get_db_status(folder: str) -> DbStatus:
    """
    Raises an exception if an unknown db status is returned.
    """
    db_status = os.system(STATUS_DB_STRING.format(folder=folder))
    return DbStatus(db_status)


def start_database(folder: str) -> None:
    print("Booting up existing database...")
    os.system(INIT_DB_STRING.format(folder=folder))
    os.system(START_DB_STRING.format(folder=folder))
    create_tables()


def stop_database(folder: str) -> None:
    print("Stopping database...")
    os.system(STOP_DB_STRING.format(folder=folder))


def drop_all_tables() -> None:
    print("Dropping all tables...")
    for table_decl in table_decls:
        drop_table(table_decl.name)


def create_tables() -> None:
    print("Creating tables in new database...")
    print(f"Table information: {table_decls}")
    for table_decl in table_decls:
        create_table(table_decl)


def create_and_start_database(folder: str) -> None:
    start_database(folder)
    create_tables()
