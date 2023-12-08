"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

from Input.database import raw_database, preprocess_database


def categorize_database(database):
    """
    Categorize raw database to collections of FLIGHT, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    # Remove ( )
    tours = [
        data.replace("(", "").replace(")", "") for data in database if "TOUR" in data
    ]
    arrival_times = [
        data.replace("(", "").replace(")", "") for data in database if "ATIME" in data
    ]
    departure_times = [
        data.replace("(", "").replace(")", "") for data in database if "DTIME" in data
    ]
    run_times = [
        data.replace("(", "").replace(")", "")
        for data in database
        if "RUN-TIME" in data
    ]
    by_vehicles = [
        data.replace("(", "").replace(")", "") for data in database if "BY" in data
    ]

    return {
        "tours": tours,
        "arrival": arrival_times,
        "departure": departure_times,
        "run_time": run_times,
        "by": by_vehicles,
    }


class ReturnType:
    Tour = "tour"
    Location = "location"
    Time = "time"
    Vehicle = "vehicle"
    YesNo = "yes/no"
    Number = "number"


def retrieve_tour(database, procedure_semantics):
    by_vehicle_result = [
        f.split()[1] for f in database["by"] if procedure_semantics["by"] in f
    ]

    tour_check_result = [
        f.split()[1] for f in database["tours"] if f.split()[1] in by_vehicle_result
    ]

    arrival_tour_result = [
        a.split()[1]
        for a in database["arrival"]
        if procedure_semantics["aloc"] in a
        and procedure_semantics["atime"] in a
        and a.split()[1] in tour_check_result
    ]

    departure_tour_result = [
        d.split()[1]
        for d in database["departure"]
        if procedure_semantics["dloc"] in d
        and procedure_semantics["dtime"] in d
        and d.split()[1] in arrival_tour_result
    ]

    run_tour_result = [
        r.split()[1]
        for r in database["run_time"]
        if (procedure_semantics["dloc"] in r.split()[2])
        and (procedure_semantics["aloc"] in r.split()[3])
        and (procedure_semantics["runtime"] in r)
        and (r.split()[1] in departure_tour_result)
    ]

    run_tour_result2 = [
        r.split()[1]
        for r in database["run_time"]
        if (procedure_semantics["dloc"] in r.split()[2])
        and (procedure_semantics["aloc"] in r.split()[3])
        and (procedure_semantics["runtime"] in r)
    ]

    if run_tour_result != []:
        return run_tour_result
    else:
        return run_tour_result2


def retrieve_vehicle(database, procedure_semantics):
    vehicle_check_result = [
        f.split()[2] for f in database["by"] if procedure_semantics["tour"] in f
    ]

    return vehicle_check_result


def retrieve_time(database, procedure_semantics):
    if procedure_semantics["command"] == "PRINT-ALL-RANGE":
        arrival_time_result = [
            a.split()[3]
            for a in database["arrival"]
            if procedure_semantics["tour"] in a and procedure_semantics["aloc"] in a
        ]

        departure_time_result = [
            d.split()[3]
            for d in database["departure"]
            if procedure_semantics["tour"] in d and procedure_semantics["dloc"] in d
        ]

        return arrival_time_result + departure_time_result

    run_time_result = [
        r.split()[4]
        for r in database["run_time"]
        if procedure_semantics["tour"] in r.split()[1]
        if procedure_semantics["dloc"] in r.split()[2]
        and procedure_semantics["aloc"] in r.split()[3]
    ]

    return run_time_result


def retrieve_location(database, procedure_semantics):
    if procedure_semantics["aloc"] in procedure_semantics["variable"]:
        arrival_loc_result = [
            a.split()[2]
            for a in database["arrival"]
            if procedure_semantics["tour"] in a and procedure_semantics["atime"] in a
        ]

        return arrival_loc_result

    if procedure_semantics["dloc"] in procedure_semantics["variable"]:
        departure_loc_result = [
            d.split()[2]
            for d in database["departure"]
            if procedure_semantics["tour"] in d and procedure_semantics["dtime"] in d
        ]

        return departure_loc_result


def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
    """
    procedure_semantics = semantics
    # print("semantics")
    # print(semantics)
    _database = preprocess_database(raw_database)
    # print(_database)
    database = categorize_database(_database)

    query = procedure_semantics["variable"]
    command = procedure_semantics["command"]

    if "?n" in query:  # noun
        result_type = ReturnType.Tour
    elif "?c" in query:
        result_type = ReturnType.Location
    elif "?t" in query or "?d" in query:  # time, day, hour
        result_type = ReturnType.Time
    elif "?v" in query:  # vehicle
        result_type = ReturnType.Vehicle

    # remove unknown args: ?t ?f ?s
    for arg in list(procedure_semantics.keys()):
        if "?" in procedure_semantics[arg] and procedure_semantics[arg] != query:
            procedure_semantics[arg] = ""
        elif procedure_semantics[arg] == query and arg != "variable":
            # arrive or depart time
            procedure_semantics[arg] = ""

    if command == "PRINT-ALL-RANGE":
        aloc, dloc = procedure_semantics["aloc"], procedure_semantics["dloc"]
        dloc = aloc if aloc != "" else dloc
        aloc = dloc if dloc != "" else aloc
        procedure_semantics["aloc"], procedure_semantics["dloc"] = aloc, dloc
    print("procedure_semantics for retrieve")
    print(procedure_semantics)

    if result_type == ReturnType.Tour:
        result = retrieve_tour(database, procedure_semantics)
    elif result_type == ReturnType.Location:
        result = retrieve_location(database, procedure_semantics)
    elif result_type == ReturnType.Time:
        result = retrieve_time(database, procedure_semantics)
    elif result_type == ReturnType.Vehicle:
        result = retrieve_vehicle(database, procedure_semantics)

    if command == "PRINT-ALL":
        return result
    elif command == "FIND-ONE-TRUE":
        return [str(result != [])]
    elif command == "PRINT-ALL-NUMBER":
        return [str(len(result))]
    elif command == "PRINT-ALL-RANGE":
        if "?d" in query and result_type == ReturnType.Time:
            result = [t.split("_")[1] for t in result]
        return [min(result), max(result)]

    return result
