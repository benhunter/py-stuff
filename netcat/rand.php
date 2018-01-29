<?php

//Make it more difficult with every round

$time = 1517222766;

$rnd =  mt_rand(1, $time);
//Add some randomness
srand($time);
$rand = rand();
echo $rand . "\n";
$rnd &= $rand;
$CURRENT_CAPTCHA = $rnd;

?>