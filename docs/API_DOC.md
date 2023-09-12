# Accounts (/auth/)
## Login -> Creates and returns access an refresh tokens
POST: /auth/login/patron/
* Input: email, password
* Output: message, tokens{access, refresh}

POST: /auth/login/restaurant/
* Input: email, password
* Output: message, tokens{access, refresh}

POST: /auth/login/admin/
* Input: email, password
* Output: message, tokens{access, refresh}

## SignUp
POST: /auth/signup/patron/
* Input: email, username, password
* Output: message, content{email, username, user_type}

POST: /auth/signup/restaurant/
* Input: email, username, password
* Output: message, content{email, username, user_type}

POST: /auth/signup/admin/
* Admin cannot be created using API right now

## JWT (Json Web Tokens) -> for manual authentication
POST: /auth/jwt/create/ --> creates and returns an access and refresh token
* Input: email, password
* Output: refresh, access

POST: /auth/jwt/refresh/ --> creates and returns a new access token
* Input: refresh
* Output: access

POST: /auth/jwt/verify/ --> verifies a token
* Input: token
* Output: ?