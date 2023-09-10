# Accounts (/auth/)
## Login
/auth/login/patron/
* Input: email, password
* Output: message, tokens{access, refresh}

/auth/login/restaurant/
* Input: email, password
* Output: message, tokens{access, refresh}

/auth/login/admin/
* Input: email, password
* Output: message, tokens{access, refresh}

## SignUp
/auth/signup/patron/
* Input: email, username, password
* Output: message, content{email, username, user_type}

/auth/signup/restaurant/
* Input: email, username, password
* Output: message, content{email, username, user_type}

/auth/signup/admin/
* Admin cannot be created using API right now

## JWT
/auth/jwt/create/ --> creates and returns an access and refresh token
* Input: email, password
* Output: refresh, access

/auth/jwt/refresh/ --> creates and returns a new access token
* Input: refresh
* Output: access

/auth/jwt/verify/ --> verifies a token
* Input: token
* Output: ?