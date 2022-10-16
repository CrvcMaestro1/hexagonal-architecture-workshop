IDEA; Negocio que renta salas para eventos
==========================================
Casos de uso
------------
* El negocio puede crear N salas con M capacidad
* El negocio puede crear eventos en cada sala, con las siguientes consideraciones:
	- 1.- No puede crearse más de 1 evento por sala en un determinado día.
	- 2.- Los eventos deberán crearse con 5 días de antelación como mínimo.
* El negocio puede listar los eventos locales (creados a través del API)
* El negocio puede listar los eventos externos (obtenidas de un API externo)
* API Externa: https://634863e50b382d796c70cd78.mockapi.io/api/v1/events


Para pensar ¿🤔?
---------------
* El negocio puede eliminar eventos a disposición. Y si el evento es externo, al eliminarlo ya no debería listarse, no?
* Tomando en cuenta que los eventos externos no se guardan localmente.