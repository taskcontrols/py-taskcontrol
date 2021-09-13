# SHARED BASE

class UtilsBase():
    def validate_object(self, event_object, values=[]):
        keys = event_object.keys()
        if len(keys) == len(values):
            if type(values) == list:
                for k in values:
                    if k in keys:
                        return True
                    else:
                        return False
            elif type(values) == dict:
                v_keys = values.keys()
                for v in v_keys:
                    if v in keys:
                        for k in keys:
                            if type(values.get(v)) == type(event_object.get(k)):
                                continue
                            else:
                                return False
                    else:
                        return False
        return False


class ClosureBase():
    def class_closure(self, **kwargs):
        closure_val = kwargs

        def getter(key, value=None):
            if (type(value) == int and value == 1) or (type(value) == str and value == "1"):
                keys = closure_val[key]
                val = []
                for t in keys:
                    if t:
                        val.append(closure_val[key].get(t))
                return val
            elif type(value) == str:
                val = closure_val[key].get(value)
                if val:
                    return [val]
                return []
            elif type(value) == list:
                vl = []
                for tk in value:
                    if int(tk) == 1:
                        for i in closure_val[key].keys():
                            vl.append(closure_val[key].get(i))
                    elif tk in closure_val[key].keys():
                        vl.append(closure_val[key].get(tk))
                return vl
            return []

        def setter(key, value=None, inst=None):
            if type(value) == dict and inst != None:
                if inst.__class__.__name__ == "SharedBase":
                    closure_val[key].update({value.get("name"): value})
                elif value.get("workflow_kwargs").get("shared") == True:
                    inst.shared.setter(key, value, inst.shared)
                elif value.get("workflow_kwargs").get("shared") == False:
                    closure_val[key].update({value.get("name"): value})

                return True
            else:
                raise TypeError("Problem with " + key +
                                " Value setting " + str(value))

        def deleter(key, value=None):
            if type(value) == str:
                if value != None:
                    closure_val[key].pop(value)
                else:
                    raise TypeError("Problem with " + key +
                                    " Value deleting " + value)
                return True
            elif type(value) == int:
                if value == 1:
                    for v in value:
                        closure_val[key].pop(v)
                return True
            return False

        return (getter, setter, deleter)


class SharedBase(ClosureBase):

    __instance = None

    def __init__(self):
        super().__init__()
        self.getter, self.setter, self.deleter = self.class_closure(
            tasks={}, ctx={}, plugins={}, config={}, workflow={}
        )
        if SharedBase.__instance != None:
            pass
        else:
            SharedBase.__instance = self

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def getInstance():
        if not SharedBase.__instance:
            return SharedBase()
        return SharedBase.__instance


__all__ = ["SharedBase", "ClosureBase", "UtilsBase"]
