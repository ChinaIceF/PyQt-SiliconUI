"""
基本思路

· 触发器函数
      触发器函数需要经过修饰器修饰，修饰器传入一条
  函数链，在触发器函数被执行之后，执行传入函数链的
  一个运行方法，从而开始函数链的运行。

· 函数链
      提供添加函数，指定传入参数，提供开始运行方法，
  提供被执行函数的返回值管理。
"""

import functools
import random
from typing import Callable, Tuple, Union


class SiFunctionChainResultReader:
    def __init__(self, func):
        self.func = func

    def run(self, index):
        return self.func(index)


class CalcLater:
    def __init__(self, func):
        self.func = func

    def run(self):
        return self.func()


class SiFunctionChain:
    def __init__(self):
        self.key_and_func = []
        self.args = {}
        self.results = {}

    @staticmethod
    def get_name(func):
        return str(func)

    @staticmethod
    def to_subscriptable(data):
        if hasattr(data, "__getitem__"):
            return data
        else:
            return (data,)

    def addFunc(self,
                function,
                args: Union[list, None] = None,
                kwargs: Union[dict, None] = None):
        """
        Add function to this function chain
        :param function: the function you want to add
        :param args: arguments that will be input
        :param kwargs: keyword arguments that will be input
        """
        if args is None:
            args = self.fromResult()
        if kwargs is None:
            kwargs = {}
        key = str(function) + str(random.random())
        self.key_and_func.append([key, function])
        self.args[key] = [args, kwargs]

    def getFunc(self, index=None):
        if index is None:
            return [func[1] for func in self.key_and_func]
        else:
            return self.key_and_func[index][1]

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
                        return self.results["__trigger__"]
                else:
                    def result(index):
                        return self.results[self.key_and_func[index + func_index_relative][0]]
            else:
                def result(_):
                    return self.results[self.key_and_func[func_index][0]]
        else:
            def result(_):
                return self.results[func[0]]

        if isinstance(slice_spec, tuple):
            return SiFunctionChainResultReader(lambda index: result(index)[slice_spec[0]:slice_spec[1]])
        elif isinstance(slice_spec, int):
            return SiFunctionChainResultReader(lambda index: result(index)[slice_spec])
        else:
            raise TypeError(f"Unexpected spec type: {type(slice_spec)}")

    def _execute_and_replace(self, data, index):
        if isinstance(data, list):
            return [self._execute_and_replace(item, index) for item in data]
        elif isinstance(data, tuple):
            return tuple(self._execute_and_replace(item, index) for item in data)
        elif isinstance(data, dict):
            return {key: self._execute_and_replace(value, index) for key, value in data.items()}
        elif isinstance(data, SiFunctionChainResultReader):
            return data.run(index)
        elif isinstance(data, CalcLater):
            return data.run()
        else:
            return data

    def execute(self, args):
        # store the result of the trigger of this chain
        self.results["__trigger__"] = args

        for index, key_and_func in enumerate(self.key_and_func):
            key, func = key_and_func
            executed_args = self._execute_and_replace(self.args[key][0], index)
            executed_kwargs = self._execute_and_replace(self.args[key][1], index)

            self.results[key] = self.to_subscriptable(func(*executed_args, **executed_kwargs))

        return self.results


# decorator of the trigger function
def chain_trigger(chain: SiFunctionChain):
    def decorator(trigger_func):
        @functools.wraps(trigger_func)
        def wrapper(*args, **kwargs):
            result = trigger_func(*args, **kwargs)

            # execute function chain, input the triggers' result as the arguments
            chain_result = chain.execute(result)
            return chain_result

        return wrapper

    return decorator


"""
def func_todo_1(number):
    print("Function 1 is called", number)
    return number + 1

def func_todo_2(number):
    print("Function 2 is called", number)


def func_todo_3():
    print("Function 3 is called")


test_function_chain = SiFunctionChain()
test_function_chain.addFunc(func_todo_1, [test_function_chain.fromResult(slice_spec=1)])
test_function_chain.addFunc(func_todo_2, [test_function_chain.fromResult(slice_spec=0, func_index=0)])
test_function_chain.addFunc(func_todo_3, [])


@chain_trigger(test_function_chain)
def test_trigger_function(number_a, number_b):
    print("Trigger is called, number A,B", number_a, number_b)
    return number_a, number_b, number_a + number_b, number_a * number_b


# 测试开始
test_trigger_function(114514, 1919)
test_trigger_function(123, 345)

print(test_function_chain.results)
"""
