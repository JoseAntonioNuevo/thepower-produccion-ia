COPIA DE AULA · resumen en español redactado para la práctica a partir de la fuente pública.
No es el texto original. Fuente: Amazon Builders' Library · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/

Los reintentos son egoístas: el cliente que reintenta gasta más tiempo del servidor para aumentar su propia probabilidad de éxito. Si el fallo se debe a una sobrecarga, reintentar sin control la agrava.

El backoff consiste en esperar entre reintentos, aumentando la espera en cada intento; lo habitual es un backoff exponencial con un valor máximo y un número limitado de reintentos.

El jitter añade aleatoriedad a la espera para que los clientes no reintenten todos a la vez y la carga se reparta en el tiempo.

Conviene fijar un timeout en cada llamada remota y reintentar solo operaciones que sean seguras de repetir (idempotentes).
