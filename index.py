server_ip = '155.138.193.36:5000'


class Index:

    def __init__(self, module, component, controller, method, req_args):
        self.module = module
        self.component = component
        self.controller = controller
        self.method = method
        self.req_args = req_args

    def render(self):
        m = __import__('.'.join(['framework','module',self.module,self.component]))
        C = getattr(m, 'module')
        C = getattr(C, self.module)
        C = getattr(C, self.component)
        C = getattr(C, self.controller)
        controller = C()
        method = getattr(controller, self.method)
        res= method(**self.req_args)
        if not res:
            return ""
        if (isinstance(res,int)):
            res = str(res)
        return res