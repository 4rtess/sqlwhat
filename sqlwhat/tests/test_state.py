from sqlwhat import check_funcs
from sqlwhat.State import State
from sqlwhat.Reporter import Reporter
from sqlwhat.Test import TestFail as TF
from sqlwhat.tests.helper import Connection
import pytest

def test_pass():
    state = State(
        student_code = "SELECT * FROM company",
        solution_code = "SELECT * FROM company",
        pre_exercise_code = "",
        student_result =  {'id': [1], 'name': ['greg']},
        solution_result = {'id': [1], 'name': ['greg']},
        student_conn = Connection('postgresql'),
        solution_conn = None,
        reporter= Reporter())

    State.root_state = state

    assert check_funcs.Ex().check_result()

def test_fail():
    state = State(
        student_code = "SELECT * FROM company",
        solution_code = "SELECT * FROM company",
        pre_exercise_code = "",
        student_result = {'id': [1], 'name': ['greg']},
        solution_result = {'id': [0], 'name': ['greg']},
        student_conn = Connection('postgresql'),
        solution_conn = None,
        reporter= Reporter())

    State.root_state = state

    with pytest.raises(TF):
        check_funcs.Ex().check_result()
