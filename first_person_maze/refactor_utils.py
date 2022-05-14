def transform_param(i, transform_function):
    def result(f):
        def g(*args):
            return f(*(args[:i] + tuple([transform_function(args[i])]) + args[i+1:]))
        return g
    return result
