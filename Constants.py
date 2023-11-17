from typing import Final


class Constants:

    EMPTY_TIME: Final[str] = '-- : -- : --'
    TIME_FORMAT: Final[str] = 'hh:mm:ss'
    TIME_REGEX_FORMAT: Final[str] = '%H:%M:%S'

    CSV_FILE_END: Final[str] = '.csv'
    BXS_FILE_END: Final[str] = '.bxs'
    EDF_FILE_END: Final[str] = '.edf'

    BXS_EXECUTABLE_NAME: Final[str] = 'bxs2edf.exe'
