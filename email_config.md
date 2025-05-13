# Configuración de Emails para Innova7e

Se ha implementado un sistema de emails para el proyecto de Innova7e que permite:

1. Enviar un correo de confirmación a usuarios que se suscriben
2. Enviar un correo de confirmación a usuarios que envían un mensaje de contacto
3. Notificar a los administradores cuando hay una nueva suscripción
4. Notificar a los administradores cuando hay un nuevo mensaje de contacto

## Configuración en Railway

Para que el sistema de emails funcione correctamente, debes agregar las siguientes variables de entorno en tu proyecto de Railway:

### Variables de Email SMTP

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `EMAIL_HOST` | Servidor SMTP | `smtp.gmail.com` |
| `EMAIL_PORT` | Puerto SMTP | `587` |
| `EMAIL_USE_TLS` | Usar TLS (true/false) | `true` |
| `EMAIL_HOST_USER` | Dirección de correo desde donde se envían los emails | `tu-correo@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Contraseña de la cuenta de correo (para Gmail, usa una contraseña de aplicación) | `tu-contraseña` |
| `ADMIN_EMAILS` | Lista de correos de administradores que recibirán notificaciones | `["admin1@ejemplo.com", "admin2@ejemplo.com"]` |

### Configuración para Gmail

Si utilizas Gmail como proveedor de correo:

1. Ve a la configuración de tu cuenta de Google
2. Activa la verificación en dos pasos
3. En "Contraseñas de aplicaciones", genera una nueva contraseña
4. Usa esta contraseña generada como valor para `EMAIL_HOST_PASSWORD`

## Plantillas de Email

Se han creado las siguientes plantillas de email:

- `emails/base_email.html` - Plantilla base para todos los emails
- `emails/subscription_confirmation.html` - Confirmación de suscripción
- `emails/contact_confirmation.html` - Confirmación de mensaje de contacto
- `emails/new_subscription_admin.html` - Notificación de nueva suscripción para administradores
- `emails/new_message_admin.html` - Notificación de nuevo mensaje para administradores

Puedes personalizar estas plantillas editando los archivos HTML en la carpeta `app/templates/emails/`.

## Configuración de Cloudflare

Para asegurar la entrega correcta de los emails, es recomendable configurar los registros DNS de tu dominio en Cloudflare:

1. Agrega un registro SPF: `TXT` con valor `v=spf1 include:_spf.google.com ~all` (si usas Gmail)
2. Configura DKIM para tu dominio según las instrucciones de tu proveedor de email
3. Agrega un registro DMARC: `TXT` en `_dmarc.tudominio.com` con valor `v=DMARC1; p=none; rua=mailto:tu-correo@gmail.com`

Estas configuraciones ayudarán a mejorar la entrega de correos y evitar que sean marcados como spam. 