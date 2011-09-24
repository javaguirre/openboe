<?php

$m = new Mongo();

$db = $m->openboe;

$grants = $db->grants;

$count = $grants->count();
echo 'Antes: '.$count;

$obj = array("title" => "Becas del mini", "author"=> 'Yo');

if(!$grants->findOne(array("title" => "BBB")))
{
    echo "Entra ";
    $grants->insert($obj);
}

$count = $grants->count();
echo 'Despues: '.$count;
?>
