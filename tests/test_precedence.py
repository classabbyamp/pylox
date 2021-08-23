from pylox.lox import Lox


# * has higher precedence than +.
def test_mult_plus(capsys):
    Lox.run_inline("print 2 + 3 * 4;")
    out = capsys.readouterr().out
    assert out == "14\n"


# * has higher precedence than -.
def test_mult_minus(capsys):
    Lox.run_inline("print 20 - 3 * 4;")
    out = capsys.readouterr().out
    assert out == "8\n"


# / has higher precedence than +.
def test_div_plus(capsys):
    Lox.run_inline("print 2 + 6 / 3;")
    out = capsys.readouterr().out
    assert out == "4\n"


# / has higher precedence than -.
def test_div_minus(capsys):
    Lox.run_inline("print 2 - 6 / 3;")
    out = capsys.readouterr().out
    assert out == "0\n"


# < has higher precedence than ==.
def test_lt_eqeq(capsys):
    Lox.run_inline("print false == 2 < 1;")
    out = capsys.readouterr().out
    assert out == "true\n"


# > has higher precedence than ==.
def test_gt_eqeq(capsys):
    Lox.run_inline("print false == 1 > 2;")
    out = capsys.readouterr().out
    assert out == "true\n"


# <= has higher precedence than ==.
def test_le_eqeq(capsys):
    Lox.run_inline("print false == 2 <= 1;")
    out = capsys.readouterr().out
    assert out == "true\n"


# >= has higher precedence than ==.
def test_ge_eqeq(capsys):
    Lox.run_inline("print false == 1 >= 2;")
    out = capsys.readouterr().out
    assert out == "true\n"


# 1 - 1 is not space-sensitive.
def test_minus_space_sensitive_0(capsys):
    Lox.run_inline("print 1 - 1;")
    out = capsys.readouterr().out
    assert out == "0\n"


def test_minus_space_sensitive_1(capsys):
    Lox.run_inline("print 1 -1;")
    out = capsys.readouterr().out
    assert out == "0\n"


def test_minus_space_sensitive_2(capsys):
    Lox.run_inline("print 1- 1;")
    out = capsys.readouterr().out
    assert out == "0\n"


def test_minus_space_sensitive_3(capsys):
    Lox.run_inline("print 1-1;")
    out = capsys.readouterr().out
    assert out == "0\n"


# Using () for grouping.
def test_grouping(capsys):
    Lox.run_inline("print (2 * (6 - (2 + 2)));")
    out = capsys.readouterr().out
    assert out == "4\n"
