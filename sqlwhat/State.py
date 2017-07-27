from copy import copy
import inspect

from sqlwhat.selectors import Dispatcher

class State:
    def __init__(self,
                 student_code,
                 solution_code,
                 pre_exercise_code,
                 student_conn,
                 solution_conn,
                 student_result,
                 solution_result,
                 reporter,
                 solution_ast = None,
                 student_ast = None,
                 ast_dispatcher = None,
                 history = tuple()):

        for k,v in locals().items():
            if k != 'self': setattr(self, k, v)

        if ast_dispatcher is None:
            self.ast_dispatcher = Dispatcher.from_dialect(self.get_dialect())

        # Parse solution and student code
        # solution code raises an exception if can't be parsed
        if solution_ast is None: self.solution_ast = self.ast_dispatcher.parse(solution_code)
        if student_ast  is None: self.student_ast  = self.ast_dispatcher.parse(student_code)

    def get_dialect(self):
        # MCE doesn't always have connection - fallback on postgresql
        return self.student_conn.dialect.name if self.student_conn else 'postgresql'
        
    def get_ast_path(self):
        rev_checks = filter(lambda x: x['type'] in ['check_field', 'check_node'], reversed(self.history))

        try:
            last = next(rev_checks)
            if last['type'] == 'check_node':
                # final check was for a node
                return self.ast_dispatcher.describe(last['node'],
                                                    index = last['kwargs']['index'],
                                                    msg = "{index}{node_name}")
            else:
                node = next(rev_checks)
                if node['type'] == 'check_node':
                    # checked for node, then for target, so can give rich description
                    return self.ast_dispatcher.describe(node['node'],
                                                        field = last['kwargs']['name'],
                                                        index = last['kwargs']['index'],
                                                        msg = "{index}{field_name} of the {node_name}")
        except StopIteration:
            return self.ast_dispatcher.describe(self.student_ast, "{node_name}")


    def do_test(self, *args, highlight=None, **kwargs):
        highlight = self.student_ast if highlight is None else highlight

        return self.reporter.do_test(*args, highlight=highlight, **kwargs)

    def to_child(self, **kwargs):
        """Basic implementation of returning a child state"""

        good_pars = inspect.signature(self.__init__).parameters
        bad_pars = set(kwargs) - set(good_pars)
        if bad_pars:
            raise KeyError("Invalid init params for State: %s"% ", ".join(bad_pars))

        child = copy(self)
        for k, v in kwargs.items(): setattr(child, k, v)
        child.parent = self
        return child
