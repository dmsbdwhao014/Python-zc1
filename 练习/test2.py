import os,sys,re
from collections import OrderedDict

def ArgsType(*argTypes,**kwTypes):
    u'''ArgsType(*argTypes,**kwTypes)
    options=[('opt_UseTypeOfDefaultValue',False)]

    以下为本函数相关的开关，并非类型检验相关的关键字参数，所有options:
    opt_UseTypeOfDefaultValue=>bool:False,为True时，将对没有指定类型的带默
                               认值的参数使用其默认值的类型
    '''
    def _ArgsType(func):
        #确定所有的parameter name
        argNames=func.func_code.co_varnames[:func.func_code.co_argcount]
        #确定所有的default parameter
        defaults=func.func_defaults
        if defaults:
            defaults=dict(zip(argNames[-len(defaults):],defaults))
        else:defaults=None
        #将“参数类型关键字参数”中的所有“options关键字参数”提出
        options=dict()
        for option,default in [('opt_UseTypeOfDefaultValue',False)]:
            options[option]=kwTypes.pop(option,default)
        #argTypes和kwTypes的总长度应该与argNames一致
        if len(argTypes)+len(kwTypes)>len(argNames):
            raise Exception('Too much types to check %s().'%func.func_name)
        #所有kwTypes中的键不能覆盖在argTypes中已经占用的names
        if not set(argNames[len(argTypes):]).issuperset(
            set(kwTypes.keys())):
            raise Exception('There is some key in kwTypes '+
                'which is not in argNames.')
        #确定所有的参数应该有的types
        types=OrderedDict()
        for name in argNames:types[name]=None
        if len(argTypes):
            for i in range(len(argTypes)):
                name=argNames[i]
                types[name]=argTypes[i]
        else:
            for name,t in kwTypes.items():
                types[name]=t
        if len(kwTypes):
            for name,t in kwTypes.items():
                types[name]=t
        #关于default parameter的type
        if options['opt_UseTypeOfDefaultValue']:
            for k,v in defaults.items():
                #如果default parameter的type没有另外指定，那么就使用
                #default parameter的default value的type
                if types[k]==None:
                    types[k]=type(v)
        def __ArgsType(*args,**kw):
            #order the args
            Args=OrderedDict()
            #init keys
            for name in argNames:Args[name]=None
            #init default values
            if defaults is not None:
                for k,v in defaults.items():
                    Args[k]=v
            #fill in all args
            for i in range(len(args)):
                Args[argNames[i]]=args[i]
            #fill in all keyword args
            for k,v in kw.items():
                Args[k]=v
            #check if there is some None in the values
            if defaults==None:
                for k in Args:
                    if Args[k]==None:
                        if defaults==None:
                            raise Exception(('%s() needs %r parameter, '+
                                'which was not given')%(func.func_name,k))
                        else:
                           if not defaults.has_key(k):
                                raise Exception(('Parameter %r of %s() is'+
                                    ' not a default parameter')%\
                                    (k,func.func_name))
            #check all types
            for k in Args:
                if not isinstance(Args[k],types[k]):
                    raise TypeError(('Parameter %r of %s() must be '+
                        'a %r object, but you post: %r')%\
                        (k,func.func_name,types[k],Args[k]))
            return func(*args,**kw)
        return __ArgsType
    return _ArgsType

def ResponsibilityRegister(author):
    def _ResponsibilityRegister(func):
        def __ResponsibilityRegister(*args,**kw):
            try:
                return func(*args,**kw)
            except Exception as e:
                print ("Something is wrong, It's %s's responsibility."%author).center(80,'*')
                raise e
        return __ResponsibilityRegister
    return _ResponsibilityRegister

@ResponsibilityRegister('Kate')
@ArgsType(str,int)
def left(Str,Len=1):
    return Str[:Len]

print('Good calling:')
print(left('hello world',8))
print('Bad calling:')
print(left(3,7))