# Fund Management System API Documentation

## Overview
The Fund Management System API provides endpoints to **create**, **retrieve**, **update**, and **delete** investment funds. This RESTful API follows standard HTTP conventions and returns responses in JSON format.

## Base URL
All API endpoints are relative to the base URL:
- http://localhost:8000/ *_or_* http://127.0.0.1:8000/

## Authentication
Authentication is not currently implemented in this version of the API.

## Response Format
All responses are returned in JSON format. Successful responses typically include the requested data, while error responses follow a consistent format:
```json
{
  "error": "Error Type",
  "message": "Human-readable error message",
  "errors": [
    // Optional array of detailed errors for validation failures
  ],
  "details": {
    // Optional additional details
  }
}
```

## Common Status Codes
- `200 OK`: Request succeeded
- `201 Created`: Resource was successfully created
- `204 No Content`: Request succeeded but no content is returned
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server-side error

## API Endpoints
### Get All Funds
Retrieves a list of all investment funds.
- **URL:** `/api/funds/`
- **Method:** `GET`
- **URL Parameters:** None
- **Data Parameters:** None
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    [
      {
        "fund_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Growth Fund",
        "manager_name": "Jane Smith",
        "description": "A high-growth investment fund",
        "nav": 1000000.0,
        "creation_date": "2025-01-01T00:00:00",
        "performance": 12.5
      },
      // Additional funds...
    ]
    ```
  - **Error Response:**
    - **Code:** 500
    - **Content:**
      ```json
      {
        "error": "Database Error",
        "message": "Failed to retrieve funds",
        "details": {"sqlite_error": "Error message"}
      }
      ```
  - **Sample Call:**
    ```bash
    curl -X GET http://localhost:8000/api/funds/
    ```

### Create Fund
Creates a new investment fund.
- **URL:** `/api/funds/`
- **Method:** `POST`
- **URL Parameters:** None
- **Data Parameters:**
  ```json
  {
    "name": "Balanced Fund",
    "manager_name": "John Doe",
    "description": "A balanced fund with moderate risk",
    "nav": 5000000.0,
    "performance": 8.2
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "fund_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Balanced Fund",
      "manager_name": "John Doe",
      "description": "A balanced fund with moderate risk",
      "nav": 5000000.0,
      "creation_date": "2025-01-01T00:00:00",
      "performance": 8.2
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "error": "Validation Error",
      "message": "Fund validation failed",
      "errors": [
        {"field": "name", "error": "Name cannot be empty"}
      ]
    }
    ```
  OR
  - **Code:** 422
  - **Content:**
    ```json
    {
      "error": "Validation Error",
      "message": "Request validation failed",
      "errors": [
        {
          "loc": [
            "body",
            277
          ],
          "msg": "JSON decode error",
          "type": "json_invalid"
        }
      ]
    }
    ```
- **Sample Call:**
  ```bash
  curl -X POST http://localhost:8000/api/funds/ \
    -H "Content-Type: application/json" \
    -d '{"name":"Balanced Fund","manager_name":"John Doe","description":"A balanced fund with moderate risk","nav":5000000.0,"performance":8.2}'
  ```

### Get Fund by ID
Retrieves details of a specific fund using its ID.
- **URL:** `/api/funds/{fund_id}`
- **Method:** `GET`
- **URL Parameters:**
  - `fund_id`: The unique identifier of the fund
- **Data Parameters:** None
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "fund_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Growth Fund",
      "manager_name": "Jane Smith",
      "description": "A high-growth investment fund",
      "nav": 1000000.0,
      "creation_date": "2025-01-01T00:00:00",
      "performance": 12.5
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "Not Found",
      "message": "Fund with ID 550e8400-e29b-41d4-a716-446655440000 not found"
    }
    ```
- **Sample Call:**
  ```bash
  curl -X GET http://localhost:8000/api/funds/550e8400-e29b-41d4-a716-446655440000
  ```

### Update Fund Performance
Updates the performance of a specific fund.
- **URL:** `/api/funds/{fund_id}/performance`
- **Method:** `PATCH`
- **URL Parameters:**
  - `fund_id`: The unique identifier of the fund
- **Data Parameters:**
  ```json
  {
    "performance": 15.0
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "fund_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Growth Fund",
      "manager_name": "Jane Smith",
      "description": "A high-growth investment fund",
      "nav": 1000000.0,
      "creation_date": "2025-01-01T00:00:00",
      "performance": 15.0
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "Not Found",
      "message": "Fund with ID 550e8400-e29b-41d4-a716-446655440000 not found"
    }
    ```
  OR
  - **Code:** 400
  - **Content:**
    ```json
    {
      "error": "Validation Error",
      "message": "Invalid performance value",
      "errors": [
        { "field": "performance", "error": "Performance must be a number" }
      ]
    }
    ```
- **Sample Call:**
  ```bash
    curl -X PATCH http://localhost:8000/api/funds/550e8400-e29b-41d4-a716-446655440000/performance \
      -H "Content-Type: application/json" \
      -d '{"performance":15.0}'
  ```

### Delete Fund
Deletes a fund using its ID.
- **URL:** `/api/funds/{fund_id}`
- **Method:** `DELETE`
- **URL Parameters:**
  - `fund_id`: The unique identifier of the fund
- **Data Parameters:** None
- **Success Response:**
  - **Code:** 204
  - **Content:** None
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "Not Found",
      "message": "Fund with ID 550e8400-e29b-41d4-a716-446655440000 not found"
    }
    ```
- **Sample Call:**
  ```bash
  curl -X DELETE http://localhost:8000/api/funds/550e8400-e29b-41d4-a716-446655440000
  ```