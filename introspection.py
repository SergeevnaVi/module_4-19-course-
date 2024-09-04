def introspection_info(obj):
    # Тип объекта
    type_obj = type(obj).__name__
    # Атрибуты объекта
    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr))]
    # Методы объекта
    methods = [method for method in dir(obj) if callable(getattr(obj, method))]
    # Модуль, к которому объект принадлежит
    module = obj.__class__.__module__

    # Проверка, можем ли вызывать объект
    call = callable(obj)
    # Выводит доп. информацию об объекте
    help_obj = help(obj)

    info = {'type': type_obj, 'attributes':attributes, 'methods': methods, 'module': module, 'callable': call, 'help': help_obj}
    return info



number_info = introspection_info(55)
print(number_info)

str_info = introspection_info('str')
print(str_info)
