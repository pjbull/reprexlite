from textwrap import dedent

from IPython.testing import globalipapp
import pytest

from reprexlite import reprex
from reprexlite.ipython import ReprexTerminalInteractiveShell


@pytest.fixture()
def reprexlite_ipython(monkeypatch):
    monkeypatch.setattr(globalipapp, "TerminalInteractiveShell", ReprexTerminalInteractiveShell)
    monkeypatch.setattr(ReprexTerminalInteractiveShell, "_instance", None)
    ipython = globalipapp.start_ipython()
    yield ipython
    ipython.run_cell("exit")
    del globalipapp.start_ipython.already_called


def test_ipython_editor(reprexlite_ipython, capsys):
    input = dedent(
        """\
        x = 2
        x + 2
        """
    )
    reprexlite_ipython.run_cell(input)
    captured = capsys.readouterr()
    print(captured.out)
    expected = str(reprex(input))
    assert captured.out == expected + "\n\n"
