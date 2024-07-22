from lark import Lark, Token
from lark.indenter import Indenter

with open("grammar.lark") as f:
    grammar = f.read()

class TreeIndenter(Indenter):
    @property
    def NL_type(self): return '_NL'
    @property
    def OPEN_PAREN_types(self): return []
    @property
    def CLOSE_PAREN_types(self): return []
    @property
    def INDENT_type(self): return '_INDENT'
    @property
    def DEDENT_type(self): return '_DEDENT'
    @property
    def tab_len(self): return 2

parser = Lark(grammar, postlex=TreeIndenter())

def compile_empty(**_):
    return ""

def compile_name(value, **_):
    return value

def compile_integer(value, **_):
    return value

def compile_double(value, **_):
    return value

def compile_float(value, **_):
    return value

def compile_string(value, **_):
    return value

def compile_primitive_type(value, **_):
    return value.lower()

def compile_binary_op(left, op, right, **kwargs):
    left = compile(left, **kwargs)
    right = compile(right, **kwargs)
    return f"{left} {op} {right}"

def compile_access_mod(mod, **_):
    value = str(mod)
    match value:
        case "pub": return "public"
        case "priv": return "private"
    return "public"

def compile_class_constructor_access_mod(mod, **_):
    value = str(mod)
    match value:
        case "pub": return "public"
        case "priv": return "private"
    return "private"

def compile_var_decl(type_hint, name, value, **kwargs):
    name = compile(name, **kwargs)
    type_hint = compile(type_hint, **kwargs)
    value = compile(value, **kwargs)
    return f"{type_hint} {name} = {value};"

def compile_class_var_decl(access_mod, type_hint, name, value, **kwargs):
    access_mod = compile(access_mod, **kwargs)
    name = compile(name, **kwargs)
    type_hint = compile(type_hint, **kwargs)
    value = compile(value, **kwargs)
    return f"{access_mod} {type_hint} {name} => {value};"

def compile_param(type_hint, name, **kwargs):
    type_hint = compile(type_hint, **kwargs)
    name = compile(name, **kwargs)
    return f"{type_hint} {name}"

def compile_arg_list(*args, **kwargs):
    args = ", ".join(compile(arg, **kwargs) for arg in args)
    return f"({args})"

def compile_generic_param_list(*params, **kwargs):
    params = ", ".join(compile(param, **kwargs) for param in params)
    return f"<{params}>"

def compile_generic_arg_list(*args, **kwargs):
    args = ", ".join(compile(arg, **kwargs) for arg in args)
    return f"<{args}>"

def compile_generic_type(type, args, **kwargs):
    type = compile(type, **kwargs)
    args = compile(args, **kwargs)
    return f"{type}{args}"

def compile_func_call(name, args, **kwargs):
    name = compile(name, **kwargs)
    args = compile(args, **kwargs)
    return f"{name}{args}"

def compile_func_call_stmt(call, **kwargs):
    return f"{compile(call, **kwargs)};"

def compile_new_expr(name, args, **kwargs):
    name = compile(name, **kwargs)
    args = compile(args, **kwargs)
    return f"new {name}{args}"

def compile_new_stmt(new, **kwargs):
    return f"{compile(new, **kwargs)};"

def compile_short_new_expr(args, **kwargs):
    args = compile(args, **kwargs)
    return f"new{args}"

def compile_short_new_stmt(short_new, **kwargs):
    return f"{compile(short_new, **kwargs)};"

def compile_prop_expr(obj, prop, **kwargs):
    obj = compile(obj, **kwargs)
    prop = compile(prop, **kwargs)
    return f"{obj}.{prop}"

def compile_method_expr(obj, method, args, **kwargs):
    obj = compile(obj, **kwargs)
    method = compile(method, **kwargs)
    args = compile(args, **kwargs)
    return f"{obj}.{method}{args}"

def compile_method_stmt(method, **kwargs):
    return f"{compile(method, **kwargs)};"

def compile_param_list(*params, **kwargs):
    return ", ".join(compile(param, **kwargs) for param in params)

def compile_func_decl(access_mod,  return_type, name, params, body, **kwargs):
    access_mod = compile(access_mod, **kwargs)
    name = compile(name, **kwargs)
    params = compile(params, **kwargs)
    return_type = compile(return_type, **kwargs)
    body = compile(body, **kwargs)
    return f"{access_mod} {return_type} {name}({params}) => {body};"

def compile_block_func_decl(access_mod, return_type, name, params, body, **kwargs):
    access_mod = compile(access_mod, **kwargs)
    name = compile(name, **kwargs)
    params = compile(params, **kwargs)
    return_type = compile(return_type, **kwargs)
    body = compile(body, **kwargs)
    return f"{access_mod} {return_type} {name}({params})\n{{\n{body}}}"

def compile_top_level_func_decl(access_mod, return_type, name, params, body, **kwargs):
    access_mod = compile(access_mod, **kwargs)
    name = compile(name, **kwargs)
    params = compile(params, **kwargs)
    return_type = compile(return_type, **kwargs)
    body = compile(body, **kwargs)
    return f"{access_mod} static {return_type} {name}({params}) => {body};"

def compile_top_level_block_func_decl(access_mod, return_type, name, params, body, **kwargs):
    access_mod = compile(access_mod, **kwargs)
    name = compile(name, **kwargs)
    params = compile(params, **kwargs)
    return_type = compile(return_type, **kwargs)
    body = compile(body, **kwargs)
    return f"{access_mod} static {return_type} {name}({params})\n{{\n{body}}}"

def compile_class_param(_, type_hint, name, **kwargs):
    type_hint = compile(type_hint, **kwargs)
    name = compile(name, **kwargs)
    return f"{type_hint} _{name}"

def compile_class_param_list(*params, **kwargs):
    params_str = ", ".join(compile(param, **kwargs) for param in params)
    code = f"({params_str})\n{{\n"
    for param in params:
        _, _, name = param.children
        code += f"{name} = _{name};\n"
    return f"{code}}}"

def compile_class_decl(access_mod, name, generics, params, body, **kwargs):
    access_mod = compile(access_mod, **kwargs)
    name = compile(name, **kwargs)
    generics = compile(generics, **kwargs)
    param_fields = ""
    for param in params.children:
        mod, type, param_name = param.children
        mod = compile(mod, **kwargs)
        type = compile(type, **kwargs)
        param_fields += f"{mod} {type} {param_name} {{ get; init; }}\n"
    params = compile(params, **kwargs)
    body = compile(body, **kwargs)
    return f"{access_mod} class {name}{generics}\n{{\n{param_fields}{access_mod} {name}{params}{body}}}\n"

def compile_expr(expr, **kwargs):
    return compile(expr, **kwargs)

def compile_block(*stmts, **kwargs):
    code = ""
    for stmt in stmts:
        if stmt.data == "expr":
            code += f"return {compile(stmt, **kwargs)};"
            continue
        code += compile(stmt, **kwargs) + "\n"
    return code

def compile_class_block(*stmts, **kwargs):
    return "\n".join(compile(stmt, **kwargs) for stmt in stmts) + "\n"

def compile_package_stmt(*path, **kwargs):
    if not path: return ""
    path = ".".join(compile(part, **kwargs) for part in path)
    return f"namespace {path}"

def compile_start(package, *stmts, **kwargs):
    package = compile(package, **kwargs)
    start_namespace = ""
    end_namespace = ""
    if package:
        start_namespace = f"{package}\n{{"
        end_namespace = "}"
    stmts = "\n".join(compile(stmt, **kwargs) for stmt in stmts)
    return f"""
        using CFlat;

        {start_namespace}
        public class Program
        {{
            {stmts}
        }}
        {end_namespace}
    """

DATA_TO_COMPILER = {
    "empty": compile_empty,
    "NAME": compile_name,
    "INTEGER": compile_integer,
    "DOUBLE": compile_double,
    "FLOAT": compile_float,
    "STRING": compile_string,
    "PRIMITIVE_TYPE": compile_primitive_type,
    "bit_expr": compile_binary_op,
    "mul_expr": compile_binary_op,
    "add_expr": compile_binary_op,
    "rel_expr": compile_binary_op,
    "eq_expr": compile_binary_op,
    "log_expr": compile_binary_op,
    "access_mod": compile_access_mod,
    "class_constructor_access_mod": compile_class_constructor_access_mod,
    "var_decl": compile_var_decl,
    "class_var_decl": compile_class_var_decl,
    "arg_list": compile_arg_list,
    "generic_param_list": compile_generic_param_list,
    "generic_arg_list": compile_generic_arg_list,
    "generic_type": compile_generic_type,
    "func_call": compile_func_call,
    "func_call_stmt": compile_func_call_stmt,
    "new_expr": compile_new_expr,
    "new_stmt": compile_new_stmt,
    "short_new_expr": compile_short_new_expr,
    "short_new_stmt": compile_short_new_stmt,
    "prop_expr": compile_prop_expr,
    "method_expr": compile_method_expr,
    "method_stmt": compile_method_stmt,
    "param": compile_param,
    "param_list": compile_param_list,
    "func_decl": compile_func_decl,
    "block_func_decl": compile_block_func_decl,
    "top_level_func_decl": compile_top_level_func_decl,
    "top_level_block_func_decl": compile_top_level_block_func_decl,
    "class_param": compile_class_param,
    "class_param_list": compile_class_param_list,
    "class_decl": compile_class_decl,
    "expr": compile_expr,
    "block": compile_block,
    "class_block": compile_class_block,
    "package_stmt": compile_package_stmt,
    "start": compile_start,
}

def compile(tree, **kwargs):
    if isinstance(tree, Token):
        return DATA_TO_COMPILER[tree.type](tree.value, **kwargs)
    return DATA_TO_COMPILER[tree.data](*tree.children, **kwargs)

def format_code(code):
    indentation = 0
    formatted_lines = []
    empty_lines = 0
    for line in code.splitlines():
        if not line.strip():
            if empty_lines >= 1:
                continue
            empty_lines += 1
        else:
            empty_lines = 0
        if line.count("}") > line.count("{"):
            indentation -= line.count("}") - line.count("{")
        formatted_lines.append("    " * indentation + line.lstrip())
        if line.count("{") > line.count("}"):
            indentation += line.count("{") - line.count("}")
    return "\n".join(formatted_lines).strip()

with open("demo.cb") as f:
    code = f.read()

def main():
    tree = parser.parse(code)
    compiled = format_code(compile(tree))
    print(compiled)
    with open("demo.out.cs", "w") as f:
        f.write(compiled)

if __name__ == '__main__':
    main()
