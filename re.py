# Utilities
def tuple_with_length (e, l):
    return isinstance(e,tuple) && len(e)==l

# predicate
def is_const(e):
    return tuple_with_length(e,2) && e[0]=="const"

def is_concat(e):
    return tuple_with_length(e,3) && e[0]=="concat"

def is_alter(e):
    return tuple_with_length(e,3) && e[0]=="alter"

def is_kleene(e):
    return tuple_with_length(e,2) && e[0]=="kleene"

# constructor
def make_const(e):
    return ("const",e)

def make_concat(e1,e2):
    return ("concat",e1,e2)

def make_alter(e1,e2):
    return ("alter",e1,e2)

def make_kleene(e):
    return ("kleene",e)

# accessor
def const_1(e):
    return e[1]

def concat_1(e):
    return e[1]

def concat_2(e):
    return e[2]

def alter_1(e):
    return e[1]

def alter_2(e):
    return e[2]

def kleene_1(e):
    return e[1]

def generate(e):
    if is_const(e):
        def aux(inp):
            if inp==const_1(e):
                (1,)
            else:
                ()
        return aux
    elif is_concat(e):
        f1 = generate(concat_1(e))
        f2 = generate(concat_2(e))
        def aux(inp):
            p1lst = f1(inp)
            res = ()
            for item in p1lst:
                res = res + f2(inp[item:len(inp)])
            return res
        return aux
    elif is_alter(e):
        f1 = generate(alter_1(e))
        f2 = generate(alter_2(e))
        def aux(inp):
            return (f1(inp),f2(inp))
        return aux
    elif is_kleene(e):
        f = generate(kleene_1(e))
        def aux(inp):
            res = f(inp)
            if len(res)==0:
                return (0,)
            else:
                for item in res:
                    res = res + aux(item)
                return res
        return aux
    else:
        pass

def re_engine(e):
    gen = generate(e)
    def helper(inp):
        for item in gen(inp):
           if item==0:
               return True
        return False
    return helper
    
# def test(candidate,re):
#     for item in testcase:
#         res_fun = candidate(item)
