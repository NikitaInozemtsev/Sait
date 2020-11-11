<?php
    $data_file="https://openweathermap.org/city/524901"; // адрес xml файла 
$xml = simplexml_load_file($data_file); // раскладываем xml на массив
    $temp=$xml->fact->temperature;
    echo json_encode( array("temp"=>$temp));
?>