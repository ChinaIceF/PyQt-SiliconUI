"""
基本思路

· 触发器函数
      触发器函数需要经过修饰器修饰，修饰器传入一条
  函数链，在触发器函数被执行之后，执行传入函数链的
  一个运行方法，从而开始函数链的运行。

· 函数链
      类的实例，提供添加函数，指定传入参数，提供开
  始运行方法，提供被执行函数的返回值管理。
"""

import functools
from typing import Union, Tuple, Callable


class SiFunctionChain:
    def __init__(self):
        self.trigger = None
        self.functions = []
        self.args = {}
        self.results = {}

    @staticmethod
    def get_name(func):
        return str(func)

    @staticmethod
    def to_tuple(result):
        if isinstance(result, tuple):
            return result
        else:
            return (result,)

    def addFunction(self,
                    function,
                    args: list,
                    kwargs: dict):
        """
        Add function to this function chain
        :param function: the function you want to add
        :param args: arguments that will be input
        :param kwargs: keyword arguments that will be input
        """
        self.functions.append(function)
        self.args[self.get_name(function)] = [args, kwargs]

    def fromResult(self,                                                                    # noqa: C901
                   slice_spec: Union[Union[int, None], Tuple[Union[int, None], Union[int, None]]] = None,
                   func: Union[Callable, None] = None,
                   func_index: Union[int, None] = None,
                   func_index_relative: Union[int, None] = None):
        """
        use a result of a func in this chain dynamically,
        this method returns a function, which will generate the result you appointed in the execution of this chain.

        In the SiFunctionChain, each result of functions will be force transformed to a tuple if the result is not a
        tuple, you can use these result by set value of slice_spec, here's how your input works under different
        slice_spec input:

        * None - same to the (None, None)
        * int - result[int]
        * tuple[a, b] - tuple[a:b]

        :param slice_spec: how to process the result tuple
        :param func: result of which function
        :param func_index: result of the function indexed under this value
        :param func_index_relative
        :return: callable object
        """

        if slice_spec is None:
            slice_spec = (None, None)

        if func is None:
            if func_index is None:
                if func_index_relative is None:
                    def result(_):
                        return self.results[self.get_name(self.trigger)]
                else:
                    def result(index):
                        return self.results[self.get_name(self.functions[index + func_index_relative])]
            else:
                def result(_):
                    return self.results[self.get_name(self.functions[func_index])]
        else:
            def result(_):
                return self.results[self.get_name(func)]

        if isinstance(slice_spec, tuple):
            return lambda index: result(index)[slice_spec[0]:slice_spec[1]]
        elif isinstance(slice_spec, int):
            return lambda index: result(index)[slice_spec]
        else:
            raise TypeError(f"Unexpected spec type: {type(slice_spec)}")

    def execute(self, *args, **kwargs):
        # store the result of the trigger of this chain
        self.results[self.get_name(self.trigger)] = [args, kwargs]

        for index, func in enumerate(self.functions):
            key = self.get_name(func)
            self.results[key] = self.to_tuple(func(*self.args[key][0], **self.args[key][1]))

        return self.results


# 触发器函数修饰器
def trigger(chain: SiFunctionChain):
    def decorator(trigger_func):
        @functools.wraps(trigger_func)
        def wrapper(*args, **kwargs):
            result = trigger_func(*args, **kwargs)

            # execute function chain, input the triggers' result as the arguments
            chain.trigger = trigger_func
            chain_result = chain.execute(result)
            return chain_result

        return wrapper

    return decorator


def func_todo_1(number):
    print("Function 1 is called", number)


def func_todo_2():
    print("Function 2 is called")


def func_todo_3():
    print("Function 3 is called")


test_function_chain = SiFunctionChain()
test_function_chain.addFunction(func_todo_1, [], {})
test_function_chain.addFunction(func_todo_2, [], {})
test_function_chain.addFunction(func_todo_3, [], {})


@trigger(test_function_chain)
def test_trigger_function(number):
    print("Trigger is called, number", number)
    return number


# 测试开始
test_trigger_function(114514)
