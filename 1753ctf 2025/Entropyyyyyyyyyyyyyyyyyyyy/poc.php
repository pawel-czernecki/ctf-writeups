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
