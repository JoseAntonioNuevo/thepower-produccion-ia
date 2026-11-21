COPIA DE AULA · resumen en español redactado para la práctica a partir de la fuente pública.
No es el texto original. Fuente: RFC 9110, sección 10.2.3 · https://www.rfc-editor.org/rfc/rfc9110.txt

Los servidores envían la cabecera Retry-After para indicar cuánto debería esperar el cliente antes de hacer una petición de seguimiento.

El valor de Retry-After puede ser una fecha HTTP o un número de segundos de espera contados desde que se recibe la respuesta; los segundos se expresan como un entero decimal no negativo.

Cuando Retry-After acompaña a una respuesta 503 Service Unavailable, indica cuánto tiempo se espera que el servicio no esté disponible para el cliente.

Cuando acompaña a una redirección 3xx, indica el tiempo mínimo que el cliente debe esperar antes de seguir la redirección.
