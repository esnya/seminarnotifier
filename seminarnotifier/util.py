def get_class(module_name, class_name, interface_class = None):
    import sys

    module = sys.modules[module_name]
    class_ = module.__dict__[class_name]

    if interface_class == None or issubclass(class_, interface_class):
        return class_
