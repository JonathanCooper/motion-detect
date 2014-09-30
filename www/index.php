<?php

$lock_file = '/www/motiondetect/run/lock';

if (is_file($lock_file)) {
    printf('Alarm system is currently deactivated');
    $toggle_str = 'Activate';
} else {
    printf('Alarm system is currently activated');
    $toggle_str = 'Deactivate';
}

printf('<br><br><form action="/toggle?action='.$toggle_str.'" method="POST"><input type="submit" value="'.$toggle_str.'"></form>');

?>
