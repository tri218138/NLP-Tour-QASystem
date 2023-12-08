"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

from nltk.sem.logic import (
    AndExpression,
    Variable,
    FunctionVariableExpression,
    ApplicationExpression,
    LambdaExpression,
)


def concat_dictionary(d1, d2):
    for key, value in d2.items():
        d1[key] = value
    return d1


def postprocess_location(location):
    location = str(location)
    if location == "'Hue'":
        return "HUE"
    if location == "'HoChiMinh'":
        return "HCM"
    if location == "'DaNang'":
        return "DN"
    if location == "'HaNoi'":
        return "HN"
    if location == "'HaiPhong'":
        return "HP"
    if location == "'KhanhHoa'":
        return "KH"
    if location == "'NhaTrang'":
        return "NT"
    if location == "'PhuQuoc'":
        return "PQ"


def add_query(query: list, expr):
    if isinstance(query[0], str):
        query[0] = expr
    else:
        query.append(expr)
    return query


def apply_virtual_variable_lambda_expr(expr):
    if type(expr) is LambdaExpression:
        expr = ApplicationExpression(
            expr, FunctionVariableExpression(Variable("x"))
        ).simplify()
    return expr


def split_application_expr_from_lambda_expr(_expr):
    exprs = []
    expr = _expr
    while type(expr) is AndExpression:
        expr.second = apply_virtual_variable_lambda_expr(expr.second)
        exprs.append(expr.second)
        expr = expr.first
    expr = apply_virtual_variable_lambda_expr(expr)
    exprs.append(expr)
    return exprs


def parse_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expr = logical_tree.label()["SEM"]
    # print("====== logical_expr =====")

    tr = "?tr"  # tour
    aloc = "?al"
    dloc = "?dl"
    atime = "?at"
    dtime = "?dt"
    runtime = "?rt"
    by = "?ve"  # by vehicle
    variable = "?"

    np_expr, vp_expr = logical_expr.args

    query = ["WHICH"]  # default
    if str(logical_expr.pred) == "YNQUERY":
        query = add_query(query, logical_expr)
    # apply variable to lambda function
    np_expr = apply_virtual_variable_lambda_expr(np_expr)
    vp_expr = apply_virtual_variable_lambda_expr(vp_expr)

    ##### NP #####
    exprs = split_application_expr_from_lambda_expr(np_expr)
    for expr in exprs:
        if not isinstance(expr, ApplicationExpression):
            print("Not Application Type => Continue")
            continue
        pred = str(expr.pred)
        if pred == "TOUR":
            if expr.constants():
                tr = postprocess_location(list(expr.constants())[0].name)
            else:
                tr = list(expr.variables())[0].name
        elif pred == "ALL":
            expr_vars = [var.name for var in list(expr.variables())]
            expr_const = [var.name for var in list(expr.constants())]
            expr_preds = [var.name for var in list(expr.predicates())]
            if "TOUR" in expr_preds + expr_const:
                tr = expr_vars[0]
                variable = expr_vars[0] if variable == "?" else variable
        elif pred == "SOURCE":
            if expr.constants():
                dloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "DEST":
            if expr.constants():
                aloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "HOWMANY":
            query = add_query(query, "HOWMANY")
            expr_vars = [var.name for var in list(expr.variables())]
            expr_const = [var.name for var in list(expr.constants())]
            expr_preds = [var.name for var in list(expr.predicates())]
            if "TOUR" in expr_preds + expr_const:
                tr = expr_vars[0]
                variable = expr_vars[0]
        elif pred == "WHICH":
            query = add_query(query, "WHICH")
            expr_vars = [var.name for var in list(expr.variables())]
            expr_const = [var.name for var in list(expr.constants())]
            expr_preds = [var.name for var in list(expr.predicates())]
            if "DAY" in expr_preds + expr_const:
                by = expr_vars[0]
                variable = expr_vars[0]
                atime = variable if atime == "?at" else atime
                dtime = variable if dtime == "?dt" else dtime
            if "TOUR" in expr_preds + expr_const:
                tr = expr_vars[0]
                variable = expr_vars[0]

    for expr in exprs:
        for index, pred in enumerate(expr.predicates()):
            if pred.name in ["WHICH", "WHEN", "HOWLONG"]:
                query = add_query(query, expr)

    ##### VP #####
    exprs = split_application_expr_from_lambda_expr(vp_expr)
    for expr in exprs:
        if not isinstance(expr, ApplicationExpression):
            print("Not Application Type => Continue")
            continue
        pred = str(expr.pred)
        if pred == "SOURCE":
            if expr.constants():
                dloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "DEST":
            if expr.constants():
                aloc = postprocess_location(list(expr.constants())[0].name)
        elif pred == "ARRIVE":
            for arg in expr.args:
                while type(arg) is AndExpression:
                    if str(arg.second.pred) == "CITY":
                        aloc = list(arg.second.variables())[0].name
                    elif str(arg.second.pred) == "WHICH":
                        query = add_query(query, arg.second)
                    arg = arg.first
                if str(arg.pred) == "CITY":
                    aloc = list(arg.variables())[0].name
                elif str(arg.pred) == "WHICH":
                    query = add_query(query, arg)
            # print(query[0].pred)
        elif pred == "LEAVE":
            expr = expr.args[0]
            for arg in expr.args:
                while type(arg) is AndExpression:
                    if str(arg.second.pred) == "HOUR":
                        dtime = list(arg.second.variables())[0].name
                    elif str(arg.second.pred) == "WHEN":
                        query = add_query(query, arg.second)
                    arg = arg.first
                if str(arg.pred) == "HOUR":
                    dtime = list(arg.variables())[0].name
                elif str(arg.pred) == "WHEN":
                    query = add_query(query, arg)
            # print(query[0].pred)
        elif pred == "IN":
            expr_vars = [var.name for var in list(expr.variables())]
            expr_const = [var.name for var in list(expr.constants())]
            expr_preds = [var.name for var in list(expr.predicates())]
            if "HOWLONG" in expr_preds:
                query = add_query(query, "HOWLONG")
                if "HOUR" in expr_const:
                    runtime = expr_vars[0]
                    variable = expr_vars[0]
                else:
                    runtime = expr_vars[0]
                    variable = expr_vars[0]

        elif pred == "WHICH":
            query = add_query(query, "WHICH")
            expr_vars = [var.name for var in list(expr.variables())]
            expr_const = [var.name for var in list(expr.constants())]
            expr_preds = [var.name for var in list(expr.predicates())]
            if "DAY" in expr_preds + expr_const:
                variable = expr_vars[0]
                if "PLURAL" in expr_preds + expr_const:
                    query[-1] = "WHICH-PLURAL"
                    continue
                atime = variable if atime == "?at" else atime
                dtime = variable if dtime == "?dt" else dtime

        elif pred == "BY":
            expr_vars = [var.name for var in list(expr.variables())]
            expr_const = [var.name for var in list(expr.constants())]
            expr_preds = [var.name for var in list(expr.predicates())]
            if len(expr_const):
                if "VEHICLE" in expr_preds:
                    by = expr_const[0][1:-1]
            # print(expr_vars, expr_const, expr_preds)
            if "WHICH" in expr_preds:
                query = add_query(query, "WHICH")
                if "VEHICLE" in expr_const:
                    by = expr_vars[0]
                    variable = expr_vars[0]
    tour = "(TOUR {})".format(tr)
    arrival_time = "(ATIME {} {} {})".format(tr, aloc, atime)
    departure_time = "(DTIME {} {} {})".format(tr, dloc, dtime)
    run_time = "(RUN-TIME {} {} {} {})".format(tr, dloc, aloc, runtime)
    by_vehicle = "(BY {} {})".format(tr, by)

    ret = []
    # print(query)
    for index in range(len(query)):
        key = query[index] if isinstance(query[index], str) else str(query[index].pred)
        _command = {
            "WHICH": "PRINT-ALL",
            "WHICH-PLURAL": "PRINT-ALL-RANGE",
            "WHEN": "PRINT-ALL",
            "HOWLONG": "PRINT-ALL",
            "HOWMANY": "PRINT-ALL-NUMBER",
            "YNQUERY": "FIND-ONE-TRUE",
        }[key]
        _variable = "?" + variable
        procedure = "({} {} {} {} {} {} {})".format(
            _command,
            _variable,
            tour,
            arrival_time,
            departure_time,
            run_time,
            by_vehicle,
        )
        ret.append(
            {
                "procedure": procedure,
                "command": _command,
                "variable": _variable,
                "tour": tr,
                "atime": atime,
                "dtime": dtime,
                "aloc": aloc,
                "dloc": dloc,
                "runtime": runtime,
                "by": by,
            }
        )

    return ret
