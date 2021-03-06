from tempfile import NamedTemporaryFile
import os.path as osp
import pytest

from ramcontrol.util import data_path
from ramcontrol import debugger


@pytest.fixture
def csv_filename():
    tempfile = NamedTemporaryFile()
    yield tempfile.name


def test_generate_scripted_session(csv_filename):
    log = osp.join(data_path(), "FR1_output.log")
    outstr = debugger.generate_scripted_session(
        log, "FR1", "test", 1, outfile=csv_filename)
    assert isinstance(outstr, str)
    for n, row in enumerate(outstr.split("\n")):
        if row.startswith("#"):
            continue
        if n is 1:
            assert row == "0;CONNECTED;"
        elif n is 2:
            assert row == '0.1;EXPNAME;{"experiment":"FR1"}'
        else:
            assert len(row.split(';')) >= 3

    with open(csv_filename, "r") as csv:
        data = csv.read()

    assert data == outstr


if __name__ == "__main__":
    pytest.main([__file__])
