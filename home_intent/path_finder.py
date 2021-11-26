import logging
import os
from pathlib import PosixPath
import warnings


class PathFinderException(Exception):
    pass


LOGGER = logging.getLogger(__name__)
UNAME_MACHINE = os.uname().machine


if UNAME_MACHINE == "x86_64":
    ARCH = "x86_64"
elif UNAME_MACHINE.startswith("arm"):
    ARCH = "arm"
elif UNAME_MACHINE == "aarch64":
    ARCH = "arm"
else:
    raise ValueError("HomeIntent only runs on x86_64 and armv7/aarch64 architectures")


def get_file(filename, relative_from=__file__, arch_dependent=False, language=None) -> PosixPath:
    warnings.warn(
        "get_file imported from the Home Intent package is deprecated and "
        "will be removed in Home Intent 2022.02.0. "
        "Please modify your code to use get_file from the home_intent object instead "
        "(ex: home_intent.get_file from the setup function)"
    )
    config_file_path = PosixPath(f"/config/{filename}")
    if config_file_path.is_file():
        LOGGER.info(f"Loading custom file: {config_file_path}")
        return config_file_path

    if language:
        filename = f"{language}/{filename}"

    if arch_dependent:
        source_file_path = PosixPath(relative_from).parent / f"default_configs/{ARCH}/{filename}"
    else:
        source_file_path = PosixPath(relative_from).parent / f"default_configs/{filename}"

    if source_file_path.is_file():
        return source_file_path

    raise PathFinderException(f"Can't find path to file {filename}")
