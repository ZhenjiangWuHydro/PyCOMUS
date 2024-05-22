import numpy as np
import requests

if __name__ == "__main__":
    base_url = 'http://127.0.0.1:8000/api/'
    user_name = "wzj"
    project_name = "Example2"

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
        'user_name': user_name, 'project_name': project_name, "num_layer": 40, "num_row": 1,
        "num_col": 100, "intblkm": 2, "max_iter": 1000, "r_close": 0.0001, "y_coord": 1
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Output params
    url = f'{base_url}comusOutPars/'
    data = {
        'user_name': user_name,
        'project_name': project_name
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Grid space
    url = f'{base_url}comusSpace/'
    atti = ['C'] + ['R'] * 100
    num_id = [1] + [i for i in range(1, 101)]
    delt = [1] * 101
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {
            "atti": atti,
            "num_id": num_id,
            "delt": delt
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # LPF layer Property
    url = f'{base_url}comusLpfProperty/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {"type": [1 for _ in range(40)], "cbd": [0] * 40, "ibs": [0] * 40}
    }
    response = requests.post(url, json=data)
    print(response.content)

    # LPF grid Property
    top = np.full((1, 100), 40, dtype=float)
    bot = np.zeros((40, 1, 100))
    for lyr in range(40):
        bot[lyr, :, :] = 39 - 1 * lyr
    ibound = np.full((40, 1, 100), 0, dtype=int)
    sc1 = np.full((40, 1, 100), 0, dtype=float)
    sc2 = np.full((40, 1, 100), 0, dtype=float)
    active_cell = [(13, 22), (12, 24), (12, 26), (12, 28), (11, 30), (11, 32), (11, 34), (10, 36), (10, 38), (10, 40),
                   (9, 42), (9, 44), (9, 46), (8, 48), (8, 50), (8, 52), (7, 54), (7, 56), (7, 58), (6, 60), (6, 62),
                   (6, 64), (5, 66), (5, 68), (5, 70), (4, 72), (4, 74), (4, 76), (3, 78), (3, 80), (3, 82), (2, 84),
                   (2, 86), (2, 88), (1, 90), (1, 92), (1, 94), (0, 96), (0, 98), (0, 100)]
    index = 0
    for activeLimit in active_cell:
        ibound[index, 0, activeLimit[0]:activeLimit[1]] = 1
        sc1[index, 0, activeLimit[0]:activeLimit[1]] = 0.0001
        sc2[index, 0, activeLimit[0]:activeLimit[1]] = 0.08
        index += 1
    top = top.flatten().tolist()
    bot = bot.flatten().tolist()
    ibound = ibound.flatten().tolist()
    sc1 = sc1.flatten().tolist()
    sc2 = sc2.flatten().tolist()
    url = f'{base_url}comusGridPars/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {
            "top": top + bot[:3900],
            "bot": bot,
            "ibound": ibound,
            "shead": [38] * 4000,
            "kx": [4] * 4000,
            "ky": [4] * 4000,
            "kz": [4] * 4000,
            "sc1": sc1,
            "sc2": sc2,
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Period
    url = f'{base_url}comusPeriod/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "period": {
            "1": {"period_len": 10, "num_step": 10, "multr": 1},
            "2": {"period_len": 10, "num_step": 10, "multr": 1},
            "3": {"period_len": 10, "num_step": 10, "multr": 1}
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Set DRN
    drn = []
    col = 25
    delev = 38
    for lyr in range(3, 41):
        drn.append([lyr, 1, col, delev, 4])
        col += 1
        delev -= 1
        drn.append([lyr, 1, col, delev, 4])
        col += 1
    url = f'{base_url}comusDRN/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {
            "1": drn
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Set GHB
    data_period1 = []
    data_period2 = []
    data_period3 = []
    ghb_period1_3_col_idx = [13, 13, 12, 12, 12, 11, 11, 11, 10, 10, 10, 9, 9, 9, 8, 8, 8, 7, 7, 7, 6, 6, 6, 5, 5, 5, 4,
                             4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1]
    ghb_period2_col_idx = [8, 7, 7, 7, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1]
    idx = 0
    for i in range(3, 41):
        data_period1.append([i, 1, ghb_period1_3_col_idx[idx], 38, 38, 1000])
        data_period3.append([i, 1, ghb_period1_3_col_idx[idx], 38, 38, 1000])
        idx += 1

    idx = 0
    for i in range(19, 41):
        data_period2.append([i, 1, ghb_period2_col_idx[idx], 22, 22, 1000])
        idx += 1
    url = f'{base_url}comusGHB/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": {
            "1": data_period1,
            "2": data_period2,
            "3": data_period3
        }
    }
    response = requests.post(url, json=data)
    print(response.content)

    # Set HFB
    hfb_data = {}
    for i in range(1,36 + 1):
        hfb_data[str(i)] = [[1, 16, 1, 17, 1e-6]]
    url = f'{base_url}comusHFB/'
    data = {
        'user_name': user_name, 'project_name': project_name,
        "data": hfb_data
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
