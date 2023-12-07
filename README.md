# SoBright API Documentation

SoBright API Documentation
# Requirement
.env
ACCESS_TOKEN_SECRET=
REFRESH_TOKEN_SECRET=

## Feature
### Profile
Method: GET
Description: This endpoint retrieves user profile information.
Endpoint: /profile
Authentication: Requires a valid access token.

### Registration
Method: POST
Description: Allows user registration.
Endpoint: /register
Authentication: Not required.

### Login
Method: POST
Description: Logs in the user.
Endpoint: /login
Authentication: Not required.

### Token
Method: GET
Description: Retrieves the access token for authentication.
Endpoint: /token
Authentication: Requires valid credentials.

### Logout
Method: DELETE
Description: Logs out the user and invalidates the session token.
Endpoint: /logout
Authentication: Requires a valid access token.
