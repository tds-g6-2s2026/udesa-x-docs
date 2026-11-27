# Limitaciones conocidas

Lo que se identificó al validar la plataforma y no se resolvió. Cada punto dice qué pasa, cómo se verificó y por qué quedó así.

## La foto de una cuenta dada de baja puede seguir visible un tiempo

**Qué pasa.** Cuando una cuenta se da de baja, media-service borra de S3 su foto de perfil y su portada. Pero esas imágenes se sirven a través de CloudFront. Si la URL ya había sido pedida, CloudFront puede seguir entregando la copia en caché hasta que esa copia expire.

**Cómo se verificó.** El 27 de noviembre de 2026, en producción, después de dar de baja una cuenta de prueba: S3 devolvía 404 para el archivo borrado, pero la URL pública respondía 200 con la cabecera `x-cache: Hit from cloudfront`. No se midió cuánto tarda en expirar la caché de esa distribución.

**Por qué no se resolvió.** Para sacar la copia al dar de baja habría que invalidar la caché de CloudFront, y eso necesita un permiso de CloudFront para el rol de media-service. La alternativa es bajar el tiempo de caché de la distribución. En los dos casos se toca infraestructura compartida que provee la cátedra ({doc}`ADR-0012 <adr-0012>`), fuera de lo que se puede cambiar desde los servicios.

**Qué sí se cumple.** El archivo se borra de S3: media-service lo registra en su log ("Baja aplicada: 2 archivos de perfil ... borrados") y S3 devuelve 404. Lo que queda es solo la copia en caché de CloudFront.
