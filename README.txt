OpenBoe, servicio web que muestra los datos del BOE de una forma más humana y permite buscar por ellos.

TODO:
----------------
Mejorar los menús, ahora son excesivamente largos
Poner links de búsqueda rápida, por ministerio
Buscar una solución para ignorar las tildes en la bd al hacer consultas

Herramienta de sincronización
------------------------------

usage: sync_service.py [-h] [--sync-titles] [--sync-items]

Opciones de sincronización de OpenBOE

optional arguments:
  -h, --help     show this help message and exit
  --sync-titles  Sincroniza los títulos y los feeds del BOE y BORME
  --sync-items   Sincroniza todos los elementos de todos los feeds del BOE y BORME
