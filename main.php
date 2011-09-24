<?php

require_once __DIR__.'/silex.phar';

$app = new Silex\Application();

// definitions
$app = new Silex\Application();

$app->register(new Silex\Extension\TwigExtension(), array(
    'twig.path'       => __DIR__.'/templates',
    'twig.class_path' => __DIR__.'/vendor/twig/lib',
));

$app->get('/', function () use ($app) {
    return $app['twig']->render('layout.twig', array());
});

$app->get('/hello/{name}', function ($name) {
    return "Hello $name";
});

$app->run();
