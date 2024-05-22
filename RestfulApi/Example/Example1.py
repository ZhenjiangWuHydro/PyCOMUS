import requests

if __name__ == "__main__":
    base_url = 'http://127.0.0.1:8000/api/'
    user_name = "wzj"
    project_name = "Example1"

    # create
    url = f'{base_url}createModel/'
    data = {
        'user_name': user_name, 'project_name': project_name,
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Control params
    url = f'{base_url}comusCtrlPars/'
    data = {
        'user_name': user_name, 'project_name': project_name, "num_layer": 1, "num_row": 1,
        "num_col": 20, "sim_type": 1, "max_iter": 10000, "x_coord": -125
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Output params
    url = f'{base_url}comusOutPars/'
    data = {
        'user_name': user_name,
        'project_name': project_name,
        "cell_bd": 2
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Grid space
    url = f'{base_url}comusSpace/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {
            "atti": ["C", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R",
                     "R"],
            "num_id": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "delt": [50, 493.0318145, 453.5892693, 417.3021278, 383.9179575, 353.2045209, 324.9481593, 298.9523065,
                     275.036122, 253.0332322, 232.7905737, 214.1673278, 197.0339415, 181.2712262, 166.7695281,
                     153.4279659, 141.1537286, 129.8614303, 119.4725159, 109.9147146, 101.1215374]
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # BCF layer Property
    url = f'{base_url}comusBcfProperty/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {"type": [1], "trpy": [1.0], "ibs": [0]}
    }
    response = requests.post(url, json=data)
    print(response.content)

    # BCF grid Property
    url = f'{base_url}comusGridPars/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {
            "top": [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
            "bot": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "ibound": [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
            "shead": [10, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
            "kx": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Period
    url = f'{base_url}comusPeriod/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "period": {
            "1": {"period_len": 1, "num_step": 1, "multr": 1}
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Run
    url = f'{base_url}run/'
    data = {
        'user_name': user_name, 'project_name': project_name
    }
    response = requests.post(url, json=data)
    print(response.content)
