## 1. Create COMUS Model

### Endpoint: Create COMUS Model

- **URL:** `/api/createModel/`
- **Method:** `POST`,`DELETE`
- **Description:** 
  - `POST`: Create a new COMUS model with the provided user name and project name.
  - `DELETE`: Delete COMUS model project for a specified user and project.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:

  - `201 CREATED` if control parameters are successfully created or updated.
  - `400 BAD REQUEST` if there are validation errors in the request data.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS Model Created Successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

### Example Request

#### POST Request

```http
POST /api/createModel/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json
{
    "user_name": "wzj",
    "project_name": "test"
}
```

#### DELETE Request

```http
DELETE /api/createModel/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

------

## 2. COMUS Control Parameters

### Endpoint: COMUS Control Parameters

- **URL:** `/api/comusCtrlPars/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS control parameters for a specified user and project.
  - `POST`: Create or update COMUS control parameters for a specified user and project.
  - `DELETE`: Delete COMUS control parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.
- **Body:** JSON object containing COMUS control parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- Additional parameters for COMUS control parameters.

#### Response

- Status Code:

  - `201 CREATED` if control parameters are successfully created or updated.
  - `404 NOT FOUND` if the specified COMUS model is not found.
  - `400 BAD REQUEST` if there are validation errors in the request data.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS control parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS control parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if control parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusCtrlPars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusCtrlPars/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json
{
    "user_name": "wzj",
    "project_name": "test",
    "num_layer": 2,
    "num_row": 10,
    "num_col": 10,
    "dim_unit": "m",
    "time_unit": "day",
    ...
    // Other control parameters
}
```

#### DELETE Request

```http
DELETE /api/comusCtrlPars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

____

## 3. COMUS Output Parameters

### Endpoint: COMUS Output Parameters

- **URL:** `/api/comusOutPars/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS output parameters for a specified user and project.
  - `POST`: Create or update COMUS output parameters for a specified user and project.
  - `DELETE`: Delete COMUS output parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `404 NOT FOUND` if the specified COMUS model or its output parameters are not found.
- **Body:** JSON object containing COMUS output parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- Additional parameters for COMUS output parameters.

#### Response

- Status Code:

  - `201 CREATED` if output parameters are successfully created or updated.
  - `404 NOT FOUND` if the specified COMUS model is not found.
  - `400 BAD REQUEST` if there are validation errors in the request data.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS output parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS output parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if output parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its output parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusOutPars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusOutPars/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "gdw_bd": 2,
    "lyr_bd": 1,
    "cell_bd": 0,
    ...
    // Other output parameters
}
```

#### DELETE Request

```http
DELETE /api/comusOutPars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

____

## 4. COMUS Space Parameters

### Endpoint: COMUS Space Parameters

- **URL:** `/api/comusSpace/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS space parameters for a specified user and project.
  - `POST`: Create or update COMUS space parameters for a specified user and project.
  - `DELETE`: Delete COMUS space parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if `user_name` or `project_name` parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its space parameters are not found.
- **Body:** JSON object containing COMUS space parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data`(object): JSON object containing space parameters.
  - `atti` (list): List of strings containing attribute types ('R' or 'C').
  - `num_id` (list): List of integers representing IDs.
  - `delt` (list): List of floats representing deltas.

#### Response

- Status Code:

  - `201 CREATED` if space parameters are successfully created or updated.
  - `400 BAD REQUEST` if there are validation errors in the request data.
  - `404 NOT FOUND` if the specified COMUS model or its related parameters are not found.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS space parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS space parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if space parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its space parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusSpace/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusSpace/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "atti": ["C", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R"],
        "num_id": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "delt": [50,493.0318145, 453.5892693, 417.3021278, 383.9179575, 353.2045209, 324.9481593, 298.9523065,
                      275.036122, 253.0332322, 232.7905737, 214.1673278, 197.0339415, 181.2712262, 166.7695281,
                      153.4279659, 141.1537286, 129.8614303, 119.4725159, 109.9147146, 101.1215374]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusSpace/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

### Notes

- For `POST` requests, provide all required space parameters in the `data` object within the request body.
- Validation checks are performed on the provided data to ensure its integrity and correctness.
- The endpoint ensures that the `ComusCtrlParsModel` associated with the given COMUS model exists and has all the required fields.
- Ensure to handle errors appropriately based on the response status codes.

____

## 5. COMUS LPF Layer Property Parameters

### Endpoint: COMUS LPF Layer Property Parameters

- **URL:** `/api/comusLpfProperty/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS LPF layer property parameters for a specified user and project.
  - `POST`: Create or update COMUS LPF layer property parameters for a specified user and project.
  - `DELETE`: Delete COMUS LPF layer property parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if `user_name` or `project_name` parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its LPF layer property parameters are not found.
- **Body:** JSON object containing COMUS LPF layer property parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data `(object): JSON object containing LPF layer property parameters.
  - `type` (list): List of integers representing types (0 or 1).
  - `cbd` (list): List of integers representing CBD values (0 or 1).
  - `ibs` (list): List of integers representing IBS values (0 or 1).

#### Response

- Status Code:

  - `201 CREATED` if LPF layer property parameters are successfully created or updated.
  - `400 BAD REQUEST` if there are validation errors in the request data.
  - `404 NOT FOUND` if the specified COMUS model or its related parameters are not found.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS LPF layer property parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS LPF layer property parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- **Status Code:**
  - `204 NO CONTENT` if LPF layer property parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its LPF layer property parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusLpfProperty/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusLpfProperty/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "type": [1],
        "cbd": [0],
        "ibs": [0]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusLpfProperty/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

### Notes

- For `POST` requests, provide all required LPF layer property parameters in the `data` object within the request body.
- Validation checks are performed on the provided data to ensure its integrity and correctness.
- The endpoint ensures that the `ComusCtrlParsModel` associated with the given COMUS model exists and has the required fields.
- Ensure to handle errors appropriately based on the response status codes.

____

## 6. COMUS BCF Layer Property Parameters

### Endpoint: COMUS BCF Layer Property Parameters

- **URL:** `/api/comusBcfProperty/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS BCF layer property parameters for a specified user and project.
  - `POST`: Create or update COMUS BCF layer property parameters for a specified user and project.
  - `DELETE`: Delete COMUS BCF layer property parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if `user_name` or `project_name` parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its BCF layer property parameters are not found.
- **Body:** JSON object containing COMUS BCF layer property parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data`(object): JSON object containing BCF layer property parameters.
  - `type` (list): List of integers representing types (0, 1, 2, or 3).
  - `trpy` (list): List of floats representing TRPY values (positive numbers).
  - `ibs` (list): List of integers representing IBS values (0 or 1).

#### Response

- Status Code:

  - `201 CREATED` if BCF layer property parameters are successfully created or updated.
  - `400 BAD REQUEST` if there are validation errors in the request data.
  - `404 NOT FOUND` if the specified COMUS model or its related parameters are not found.

- Body:

  - Success:

    ```json
    json{
        "success": "COMUS BCF layer property parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS BCF layer property parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- **Status Code:**
  - `204 NO CONTENT` if BCF layer property parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its BCF layer property parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusBcfProperty/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusBcfProperty/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "type": [1],
        "trpy": [1.0],
        "ibs": [0]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusBcfProperty/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

### Notes

- For `POST` requests, provide all required BCF layer property parameters in the `data` object within the request body.
- Validation checks are performed on the provided data to ensure its integrity and correctness.
- The endpoint ensures that the `ComusCtrlParsModel` associated with the given COMUS model exists and has the required fields.
- Ensure to handle errors appropriately based on the response status codes.

____

## 7. COMUS Grid Parameters

### Endpoint: COMUS Grid Parameters

- **URL:** `/api/comusGridPars/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS grid parameters for a specified user and project.
  - `POST`: Create or update COMUS grid parameters for a specified user and project.
  - `DELETE`: Delete COMUS grid parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if `user_name` or `project_name` parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its grid parameters are not found.
- **Body:** JSON object containing COMUS grid parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data `(object): JSON object containing grid parameters. It can contain any combination of the following parameters:
  - `"top"`: List of integers or floats representing top values.
  - `"bot"`: List of integers or floats representing bottom values.
  - `"ibound"`: List of integers representing ibound values.
  - `"shead"`: List of integers or floats representing shead values.
  - `"kx"`: List of integers or floats representing kx values.
  - `"transm"`: List of integers or floats representing transm values.
  - `"vcont"`: List of integers or floats representing vcont values.
  - `"sc1"`: List of integers or floats representing sc1 values.
  - `"sc2"`: List of integers or floats representing sc2 values.
  - `"wet_dry"`: List of integers or floats representing wet_dry values.
  - `"ky"`: List of integers or floats representing ky values.
  - `"kz"`: List of integers or floats representing kz values.
  - `"vkcb"`: List of integers or floats representing vkcb values.
  - `"tkcb"`: List of integers or floats representing tkcb values.

#### Response

- Status Code:

  - `201 CREATED` if grid parameters are successfully created or updated.
  - `400 BAD REQUEST` if there are validation errors in the request data.
  - `404 NOT FOUND` if the specified COMUS model or its related parameters are not found.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS grid parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS grid parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- **Status Code:**
  - `204 NO CONTENT` if grid parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its grid parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusGridPars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusGridPars/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "top": [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
        "bot": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "ibound": [-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1],
        "shead":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        "kx": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusGridPars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

### Notes

- For `POST` requests, provide all required grid parameters in the `data` object within the request body.
- Validation checks are performed on the provided data to ensure its integrity and correctness.
- The endpoint ensures that the `ComusCtrlParsModel` associated with the given COMUS model exists and has the required fields.
- Ensure to handle errors appropriately based on the response status codes.

____

## 8. COMUS Period Parameters

### Endpoint: COMUS Period Parameters

- **URL:** `/api/comusPeriod/
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve COMUS period parameters for a specified user and project.
  - `POST`: Create or update COMUS period parameters for a specified user and project.
  - `DELETE`: Delete COMUS period parameters for a specified user and project.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if `user_name` or `project_name` parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its period parameters are not found.
- **Body:** JSON object containing COMUS period parameters.

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `period`(object): JSON object containing period parameters. Each key represents a period index, and the value is an object containing:
  - `"period_len"` (int): Length of the period.
  - `"num_step"` (int): Number of steps in the period.
  - `"multr"` (number): Multiplier value for the period.

#### Response

- Status Code:

  - `201 CREATED` if period parameters are successfully created or updated.
  - `400 BAD REQUEST` if there are validation errors in the request data.
  - `404 NOT FOUND` if the specified COMUS model is not found.

- Body:

  - Success:

    ```json
    {
        "success": "COMUS period parameters saved successfully"
    }
    ```

    or

    ```json
    {
        "success": "COMUS period parameters updated successfully"
    }
    ```

  - Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- **Status Code:**
  - `204 NO CONTENT` if period parameters are successfully deleted.
  - `404 NOT FOUND` if the specified COMUS model or its period parameters are not found.
- **Body:** None

### Example Requests

#### GET Request

```http
GET /api/comusPeriod/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusPeriod/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "period": {
        "1": {
            "period_len": 1,
            "num_step": 1,
            "multr": 1
        }
    }
}
```

#### DELETE Request

```http
DELETE /api/comusPeriod/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

------

## 9. COMUS SHB Parameters

### Endpoint: COMUS SHB Parameters

- **URL:** `/api/comusSHB/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **SHB (Transient Specified-Head Boundary)** parameters for a specified COMUS model.
  - `POST`: Create or update SHB parameters for a specified COMUS model.
  - `DELETE`: Delete SHB parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its SHB parameters are not found.
- **Body:** JSON object containing SHB parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 16, 17], [1, 1, 1, 17, 18]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): SHB parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 1, 1], [1, 1, 1, 22, 1]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if SHB parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS SHB parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS SHB parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

**Example Error Response:**

```json
{
    "error": "Invalid 'data' values: '1' must be a dictionary"
}
```

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if SHB parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its SHB parameters are not found.

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column, and shead, ehead.

**Example:**

```json
{
    "period": [[layer, row, col, shead, ehead], ...],
    ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusSHB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusSHB/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 16, 17], [1, 1, 2, 16, 17]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusSHB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

------

## 10. COMUS GHB Parameters

### Endpoint: COMUS GHB Parameters

- **URL:** `/api/comusGHB/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **GHB (General-Head Boundary)** parameters for a specified COMUS model.
  - `POST`: Create or update GHB parameters for a specified COMUS model.
  - `DELETE`: Delete GHB parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its GHB parameters are not found.
- **Body:** JSON object containing GHB parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 38, 38, 1000], [1, 1, 2, 38, 38, 1000]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): GHB parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 38, 38, 1000], [1, 1, 2, 38, 38, 1000]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if GHB parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS GHB parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS GHB parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

**Example Error Response:**

```json
{
    "error": "Invalid 'data' values: '1' must be a dictionary"
}
```

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if GHB parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its GHB parameters are not found.

**Example Request:**

```http
DELETE /api/comusGHB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

**Example Response:**

- Success:

  ```http
  {
      "success": "COMUS GHB parameters deleted successfully!"
  }
  ```

- Error (if applicable): JSON object containing error details.

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column, and additional parameters.

**Example:**

```json
{
    "period": [[layer, row, col, shead, ehead, cond], ... ],
    ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusGHB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusGHB/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 38, 38, 1000], [1, 1, 2, 38, 38, 1000]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusGHB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

------

## 11. COMUS RCH Parameters

### Endpoint: COMUS RCH Parameters

- **URL:** `/api/comusRCH/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **RCH (Recharge)** parameters for a specified COMUS model.
  - `POST`: Create or update RCH parameters for a specified COMUS model.
  - `DELETE`: Delete RCH parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its RCH parameters are not found.
- **Body:** JSON object containing RCH parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 3.9473934323638e-06], [1, 1, 2, 3.9363763269537e-06]]
    },
    "rech": 2
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): RCH parameters in a nested dictionary format.
- `rech` (integer): Recharge parameter (1 or 2).

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
         "1": [[1, 1, 1, 3.9473934323638e-06], [1, 1, 2, 3.9363763269537e-06]]
    },
    "rech": 2
}
```

#### Response

- Status Code:
  - `201 CREATED` if RCH parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS RCH parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS RCH parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

**Example Error Response:**

```json
{
    "error": "Invalid 'data' values: '1' must be a dictionary"
}
```

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if RCH parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its RCH parameters are not found.

**Example Request:**

```http
DELETE /api/comusRCH/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

**Example Response:**

- Success:

  ```json
  {
      "success": "COMUS RCH parameters deleted successfully!"
  }
  ```

- Error (if applicable): JSON object containing error details.

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column, and additional parameters.

**Example:**

```json
{
    "period": [[layer, row, col, rechr], ... ],
    ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusRCH/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusRCH/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
         "1": [[1, 1, 1, 3.9473934323638e-06], [1, 1, 2, 3.9363763269537e-06]]
    },
    "rech": 2
}
```

#### DELETE Request

```http
DELETE /api/comusRCH/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

------

## 12. COMUS WEL Parameters

### Endpoint: COMUS WEL Parameters

- **URL:** `/api/comusWEL/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **WEL (Well)** parameters for a specified COMUS model.
  - `POST`: Create or update WEL parameters for a specified COMUS model.
  - `DELETE`: Delete WEL parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its WEL parameters are not found.
- **Body:** JSON object containing WEL parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, -500, 0.1], [1, 1, 2, -500, 0.1]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): WEL parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, -500, 0.1], [1, 1, 2, -500, 0.1]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if WEL parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS WEL parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS WEL parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

**Example Error Response:**

```json
{
    "error": "Invalid 'data' values: '1' must be a dictionary"
}
```

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if WEL parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its WEL parameters are not found.

**Example Request:**

```http
DELETE /api/comusWEL/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

**Example Response:**

- Success:

  ```json
  {
      "success": "COMUS WEL parameters deleted successfully!"
  }
  ```

- Error (if applicable): JSON object containing error details.

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column,wellr, and satthr.

**Example:**

```json
{
    "period": [[layer, row, col, wellr, satthr], ... ],
    ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusWEL/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusWEL/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, -500, 0.1], [1, 1, 2, -500, 0.1]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusWEL/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

____

## 13. COMUS DRN Parameters

### Endpoint: COMUS DRN Parameters

- **URL:** `/api/comusDRN/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **DRN (Drain)** parameters for a specified COMUS model.
  - `POST`: Create or update DRN parameters for a specified COMUS model.
  - `DELETE`: Delete DRN parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its DRN parameters are not found.
- **Body:** JSON object containing DRN parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 38, 4], [1, 1, 1, 37, 4]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): DRN parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 38, 4], [1, 1, 1, 37, 4]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if DRN parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its control parameters are not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS DRN parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS DRN parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

**Example Error Response:**

```json
{
    "error": "Invalid 'data' values: '1' must be a dictionary"
}
```

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if DRN parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its DRN parameters are not found.

**Example Request:**

```http
DELETE /api/comusDRN/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

**Example Response:**

```json
{
    "success": "COMUS DRN parameters deleted successfully!"
}
```

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column, drain elevation, and conductance.

**Example:**

```json
{
    "period": [[layer, row, col, delev, cond], ... ],
    ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusDRN/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusDRN/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 38, 4], [1, 1, 1, 37, 4]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusDRN/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

____

## 14. COMUS EVT Parameters

### Endpoint: COMUS EVT Parameters

- **URL:** `/api/comusEVT/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **EVT (Evapotranspiration)** parameters for a specified COMUS model.
  - `POST`: Create or update EVT parameters for a specified COMUS model.
  - `DELETE`: Delete EVT parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its EVT parameters are not found.
- **Body:** JSON object containing EVT parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 20, 0.002, 5, 2], [1, 1, 2, 20, 0.002, 5, 2]]
    },
    "evt": 2,
    "num_seg": 20
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): EVT parameters in a nested dictionary format.
- `evt` (integer): EVT type (1 or 2).
- `num_seg` (integer): Number of segments (2 to 20).

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 20, 0.002, 5, 2], [1, 1, 2, 20, 0.002, 5, 2]]
    },
    "evt": 2,
    "num_seg": 20
}
```

#### Response

- Status Code:
  - `201 CREATED` if EVT parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its related data is not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS EVT parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS EVT parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

**Example Error Response:**

```json
{
    "error": "Invalid 'data' values: '1' must be a dictionary"
}
```

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if EVT parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its EVT parameters are not found.

**Example Response:**

```json
{
    "success": "COMUS EVT parameters deleted successfully!"
}
```

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column and other parameters.

**Example:**

```json
{
    "period": [[layer, row, col, ETSURF, ETRATE, ETMXD, ETEXP], ... ],
    ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusEVT/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusEVT/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 20, 0.002, 5, 2], [1, 1, 2, 20, 0.002, 5, 2]]
    },
    "evt": 2,
    "num_seg": 20
}
```

#### DELETE Request

```http
DELETE /api/comusEVT/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

____

## 15. COMUS HFB Parameters

### Endpoint: COMUS HFB Parameters

- **URL:** `/api/comusHFB/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **HFB (Horizontal-Flow Barrier)** parameters for a specified COMUS model.
  - `POST`: Create or update HFB parameters for a specified COMUS model.
  - `DELETE`: Delete HFB parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its HFB parameters are not found.
- **Body:** JSON object containing HFB parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 2, 1E-06], [1, 2, 1, 3, 1E-06]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): HFB parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 2, 1E-06], [1, 2, 1, 3, 1E-06]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if HFB parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its related data is not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS HFB parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS HFB parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if HFB parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its HFB parameters are not found.

**Example Response:**

```json
{
    "success": "COMUS HFB parameters deleted successfully!"
}
```

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys represent layer numbers.
- Each value is a list of sublists.
- Each sublist represents a row1, column1, row2, col2 and HCDW.

**Example:**

```json
{
    "layer": [[row1, col1, row2, col2, HCDW], ... ],
     ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusHFB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusHFB/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 2, 1E-06], [1, 2, 1, 3, 1E-06]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusHFB/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

## 16. COMUS RIV Parameters

### Endpoint: COMUS RIV Parameters

- **URL:** `/api/comusRIV/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve RIV (River) parameters for a specified COMUS model.
  - `POST`: Create or update RIV parameters for a specified COMUS model.
  - `DELETE`: Delete RIV parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its RIV parameters are not found.
- **Body:** JSON object containing RIV parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 1, 16, 16, 100, 15]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): RIV parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 16, 16, 100, 15]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if RIV parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its related data is not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS RIV parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS RIV parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if RIV parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its RIV parameters are not found.

**Example Response:**

```json
{
    "success": "COMUS RIV parameters deleted successfully!"
}
```

### Data Structure

The `data` field in the POST request body must follow this structure:

- A dictionary where keys are strings representing period numbers.
- Each value is a list of sublists.
- Each sublist represents a layer, row, column and other parameters.

**Example:**

```json
{
    "period": [[layer, row, col, shead, ehead, cond, rivbtm], ... ],
     ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusRIV/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusRIV/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 1, 16, 16, 100, 15]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusRIV/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

## 17. COMUS IBS Parameters

### Endpoint: COMUS IBS Parameters

- **URL:** `/api/comusIBS/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve **IBS (Interbed Storage)** parameters for a specified COMUS model.
  - `POST`: Create or update IBS parameters for a specified COMUS model.
  - `DELETE`: Delete IBS parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its IBS parameters are not found.
- **Body:** JSON object containing IBS parameters.

**Example Response:**

```json
{
    "data": {
        "1": [[1, 1, 25, 0.5, 0.5, 0]]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): IBS parameters in a nested dictionary format.

**Example Request:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 25, 0.5, 0.5, 0]]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if IBS parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its related data is not found.

**Body:**

- Success:

  ```json
  {
      "message": "COMUS IBS parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS IBS parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if IBS parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its IBS parameters are not found.

**Example Response:**

```json
{
    "success": "COMUS IBS parameters deleted successfully!"
}
```

### Data Structure

The IBS parameters `data` field in the request body must follow this structure:

- A dictionary where keys represent the period numbers.
- Each value is a list containing information about the internal boundary source parameters.
  - The sublist should contain:
    - Row and column of the internal boundary source grid cell
    - Concentration, injection rate, discharge, decay rate, and decay sorption coefficient

**Example:**

```json
{
    "layer": [[row, col, hc, sfe, sfv, com], ... ],
     ...
}
```

### Example Requests

#### GET Request

```http
GET /api/comusIBS/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusIBS/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [[1, 1, 25, 0.5, 0.5, 0]]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusIBS/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

## 18. COMUS Stream Control Parameters

### Endpoint: COMUS Stream Control Parameters

- **URL:** `/api/comusSTR/ctrlpars/`
- **Allowed Methods:** `GET`, `POST`, `DELETE`
- Description:
  - `GET`: Retrieve stream control parameters for a specified COMUS model.
  - `POST`: Create or update stream control parameters for a specified COMUS model.
  - `DELETE`: Delete stream control parameters for a specified COMUS model.

### GET Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `200 OK` if successful.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its stream control parameters are not found.
- **Body:** JSON object containing stream control parameters.

**Example Response Body:**

```json
{
    "data": {
        "1": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "2": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "3": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "4": [0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
}
```

### POST Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.
- `data` (JSON): Stream control parameters in a nested dictionary format.

**Example Request Body:**

```json
{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "2": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "3": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "4": [0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
}
```

#### Response

- Status Code:
  - `201 CREATED` if stream control parameters are successfully created or updated.
  - `400 BAD REQUEST` if the request is malformed or required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its related data is not found.

**Example Response Body:**

- Success:

  ```json
  {
      "message": "COMUS stream control parameters saved successfully"
  }
  ```

  or

  ```json
  {
      "message": "COMUS stream control parameters updated successfully"
  }
  ```

- Error (if applicable): JSON object containing error details.

### DELETE Request

#### Parameters

- `user_name` (string): User name associated with the COMUS model.
- `project_name` (string): Project name associated with the COMUS model.

#### Response

- Status Code:
  - `204 NO CONTENT` if stream control parameters are successfully deleted.
  - `400 BAD REQUEST` if the required parameters are missing.
  - `404 NOT FOUND` if the specified COMUS model or its stream control parameters are not found.

**Example Response:**

```json
{
    "success": "COMUS stream control parameters deleted successfully!"
}
```

### Data Structure

The stream control parameters `data` field in the request body must follow this structure:

- A dictionary where keys represent the period numbers.
- Each value is a list containing information about the stream control parameters. The sublist should contain the following parameters:
  1. `NEXTID` (Integer): Next downstream convergence unit's ID. If there is no downstream convergence unit, input 0.
  2. `NEXTAT` (Integer): Attribute of the next downstream convergence unit. 1 represents a river unit, and 2 represents a lake unit. If there is no downstream convergence unit, input 0.
  3. `DIVSID` (Integer): Dividing water source unit ID. If the unit does not divide from other units, input 0.
  4. `DIVSAT` (Integer): Attribute of the dividing water source unit. 1 represents a river unit, and 2 represents a lake unit. If the unit does not divide from other units, input 0.
  5. `DIVTPOPT` (Integer): Water division method. If `DIVSID` > 0, 1 represents division based on specified flow, 2 represents division based on the proportion of the terminal flow of the water source unit (only applicable when the water source unit is a river), and 3 represents automatic trial division based on the unit's water usage. If `DIVSID` = 0, 0 represents not using additional flow to meet artificial water demands, and 1 represents using additional flow.
  6. `WUTPOPT` (Integer): Water use method option of the river unit. 1 represents distributing water use according to the length of the river segment units, and 2 represents water use from the end river segment unit of the river unit.
  7. `WUREGID` (Integer): Water use zone ID corresponding to the river unit. If the river unit does not simulate the return of water use to the water use zone, input 0.
  8. `WUBKOPT` (Integer): Option to simulate water use return to the downstream discharge of the river unit. 0 represents not simulating, and 1 represents simulating.
  9. `DRNOPT` (Integer): Option to simulate regional drainage of the river unit. 0 represents not simulating, and 1 represents simulating.

**Example Request Body:**

```
{
    "data": {
        "1": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "2": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "3": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "4": [0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
}
```

### Example Requests

#### GET Request

```http
GET /api/comusSTR/ctrlpars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

#### POST Request

```http
POST /api/comusSTR/ctrlpars/ HTTP/1.1
Host: http://127.0.0.1:8000
Content-Type: application/json

{
    "user_name": "wzj",
    "project_name": "test",
    "data": {
        "1": [3, 1, 0, 0, 0, 1, 0, 0, 0],
        "2": [3, 1, 0, 0, 0, 1, 0, 0, 0],
        "3": [5, 1, 0, 0, 0, 1, 0, 0, 0],
        "4": [5, 1, 0, 0, 0, 1, 0, 0, 0],
        "5": [1, 2, 0, 0, 0, 1, 0, 0, 0],
        "6": [0, 0, 0, 0, 0, 1, 0, 0, 0]
    }
}
```

#### DELETE Request

```http
DELETE /api/comusSTR/ctrlpars/?user_name=wzj&project_name=test HTTP/1.1
Host: http://127.0.0.1:8000
```

