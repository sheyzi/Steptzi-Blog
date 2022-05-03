# Steptzi Blog API

### Authentication Endpoints

| Endpoint                     | Method | Description                                 | Is Done |
| ---------------------------- | :----: | ------------------------------------------- | :-----: |
| /auth/login                  |  POST  | Get access and refresh token                |  True   |
| /auth/register               |  POST  | Register a user account                     |  True   |
| /auth/refresh                |  GET   | Get a new pair of access and refresh tokens |  True   |
| /auth/reset-password         |  POST  | Send reset password mail                    |  True   |
| /auth/reset-password/confirm |  POST  | Confirm and reset password                  |  True   |
| /auth/email-verify           |  POST  | Send user email verification mail           |  True   |
| /auth/email-verify/confirm   |  GET   | Verify user email                           |  True   |

### Users Endpoints

| Endpoint    | Method | Description                    | Is Done |
| ----------- | :----: | ------------------------------ | :-----: |
| /me         |  GET   | Get authenticated users detail |  True   |
| /users      |  GET   | Get all users                  |  True   |
| /users/{id} |  GET   | Get user with id               |  True   |
| /users      |  PUT   | Update user details            |  True   |

### Tags Endpoints

| Endpoint     | Method | Description            | Is Done |
| ------------ | :----: | ---------------------- | :-----: |
| /tags        |  POST  | Create a new tag       |  True   |
| /tags        |  GET   | Get all tags           |  True   |
| /tags/{slug} |  GET   | Get a tag with slug    |  True   |
| /tags/{slug} |  PUT   | Update a tag with slug |  True   |
| /tags/{slug} | DELETE | Delete a tag with slug |  True   |

### Posts Endpoints

| Endpoint      | Method | Description             | Is Done |
| ------------- | :----: | ----------------------- | :-----: |
| /posts        |  POST  | Create a new post       |  False  |
| /posts        |  GET   | Get all posts           |  False  |
| /posts/{slug} |  GET   | Get a post with slug    |  False  |
| /posts/{slug} |  PUT   | Update a post with slug |  False  |
| /posts/{slug} | DELETE | Delete a post with slug |  False  |

### Comment Endpoints

| Endpoint                                 | Method | Description                | Is Done |
| ---------------------------------------- | :----: | -------------------------- | :-----: |
| /posts/{post_slug}/comments              |  POST  | Create a new post comment  |  False  |
| /posts/{post_slug}/comments              |  GET   | Get all post comments      |  False  |
| /posts/{post_slug}/comments/{comment_id} |  GET   | Get a post comment with id |  False  |
| /posts/{post_slug}/comments/{comment_id} | DELETE | Delete a comment with id   |  False  |
