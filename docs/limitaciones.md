# Limitaciones conocidas

Lo que se identificó al validar la plataforma y no se resolvió. Cada punto dice qué pasa, cómo se verificó y por qué quedó así.

## La foto de una cuenta dada de baja puede seguir visible un tiempo

**Qué pasa.** Cuando una cuenta se da de baja, media-service borra de S3 su foto de perfil y su portada. Pero esas imágenes se sirven a través de CloudFront. Si la URL ya había sido pedida, CloudFront puede seguir entregando la copia en caché hasta que esa copia expire.

**Cómo se verificó.** El 27 de noviembre de 2026, en producción, después de dar de baja una cuenta de prueba: S3 devolvía 404 para el archivo borrado, pero la URL pública respondía 200 con la cabecera `x-cache: Hit from cloudfront`. No se midió cuánto tarda en expirar la caché de esa distribución.

**Por qué no se resolvió.** Para sacar la copia al dar de baja habría que invalidar la caché de CloudFront, y eso necesita un permiso de CloudFront para el rol de media-service. La alternativa es bajar el tiempo de caché de la distribución. En los dos casos se toca infraestructura compartida que provee la cátedra ({doc}`ADR-0012 <adr-0012>`), fuera de lo que se puede cambiar desde los servicios.

**Qué sí se cumple.** El archivo se borra de S3: media-service lo registra en su log ("Baja aplicada: 2 archivos de perfil ... borrados") y S3 devuelve 404. Lo que queda es solo la copia en caché de CloudFront.

## Una cita de alguien silenciado muestra su texto en el feed

**Qué pasa.** Silenciar a alguien (E.3 H10, #39) saca del feed principal y de "Para vos" sus posts, sus retweets y los retweets que otros hacen de sus posts. Pero si alguien a quien seguís cita un post del silenciado, la cita aparece en el feed, porque es un post de quien cita, y adentro se ve el texto del post original.

**Cómo se verificó.** Lo marcó la review de posts #43, el 28 de noviembre de 2026.

**Por qué no se resolvió.** Es una decisión de diseño. La cita es de una persona que sí querés ver, y ocultarle el contenido citado sería tratar al silenciado como a un bloqueado. El alcance que se acordó para #39 es el feed de posts y retweets: el post citado embebido quedó afuera, igual que la búsqueda, los hashtags y el detalle de un post.

**Qué sí se cumple.** Sus posts y retweets no aparecen en el feed (CA.2 y CA.5), su perfil los sigue mostrando, y su actividad no manda push (CA.4).

## No hay interruptor de mensajes directos

**Qué pasa.** Las preferencias de push (E.4 H5, #44) tienen un interruptor por cada tipo de notificación que existe: likes, retweets, respuestas, citas, menciones y nuevos seguidores. El CA.1 original también pedía uno para mensajes directos, que no está.

**Cómo se verificó.** Mensajes Directos (E.3 H6, #35) no se implementó: ningún servicio publica un evento de mensaje directo.

**Por qué no se resolvió.** Un interruptor que no apaga nada confundiría a quien lo usa. Por eso se sacó del criterio de la issue y la columna `direct_message` se borró de `push_preferences` (notifications #7). Si en algún momento se hacen los mensajes directos, el tipo nuevo se suma con una columna en una migración y un switch en la app.

**Qué sí se cumple.** Cada tipo que existe tiene su interruptor y se consulta antes de cada push (CA.2).
