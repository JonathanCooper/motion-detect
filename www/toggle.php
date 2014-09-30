<?php

$lock_file = '/www/motiondetect/run/lock';

if ($_GET['action'] == 'Activate') {
    unlink($lock_file);
} elseif ($_GET['action'] == 'Deactivate') {
    touch($lock_file);
} else {
    printf('Error:  unknown action');
}

header('Location: /');
?>
