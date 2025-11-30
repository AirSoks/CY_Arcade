<?php
for ($i = 0; $i < 10; $i++) {
    echo password_hash("setup", PASSWORD_DEFAULT) . "<br>";
}
?>