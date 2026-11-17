# Instalación de Garmin Recovery (plantilla)

Esta plantilla trae **todo el código** de Garmin Recovery: la cadena automática (Sync → FC → análisis → CrossFit → web), los modelos de recuperación, la encuesta de sensaciones, los descansos, el peso, las comparaciones de WODs, los máximos estimados y el panel web con sus 4 pestañas. **No trae datos de nadie**: los registros empiezan vacíos y se llenan con los tuyos.

Calcula **1–2 horas** para la instalación. Después todo funciona solo, tres veces al día.

> Al principio la app tiene pocos datos. Necesita **2–4 semanas** para que tus rangos «normales» (HRV, pulso en reposo, sueño) sean fiables y **10 encuestas** para tener tu referencia de sensaciones. Hasta entonces verás confianza baja o media: es normal.

## Qué necesitas

| Cuenta | Para qué | Coste |
|---|---|---|
| **Garmin Connect** con un reloj Garmin | Sueño, HRV, pulso, Body Battery, estrés, métricas de rendimiento | — |
| **Intervals.icu** conectado a tu Garmin | Lista de entrenamientos (actividades) y bienestar diario | Gratis |
| **GitHub** | Donde vive y se ejecuta la app, y donde se publica la web | Gratis |
| **Google** (Hojas de cálculo y Apps Script) | Hoja de RPE y el disparador de los Sync a su hora | Gratis |
| **Claude** (opcional, recomendado) | Apuntar tus entrenos y RPE por chat, la encuesta y el informe redactado | Tu plan |
| **ntfy** (opcional) | Avisos en el móvil cuando hay informe nuevo | Gratis |

## 1. Crea tu copia

1. En la página de esta plantilla en GitHub, pulsa **Use this template → Create a new repository**.
2. Nombre: `garmin-recovery` (si usas otro, cámbialo también en el paso 6).
3. Visibilidad: **pública**. Ten en cuenta:
   - Con un repositorio **público**, los minutos de GitHub Actions y GitHub Pages son gratis, pero **cualquiera con el enlace puede ver tus datos de salud** (sueño, HRV, peso, encuestas) y la web.
   - Con uno **privado**, tus datos no se ven, pero la cadena consume unos 4.000 minutos de Actions al mes (el plan gratuito incluye 2.000) y GitHub Pages en privado necesita un plan de pago.
   - Decide con eso en mente.
4. En tu repositorio nuevo:
   - **Settings → Actions → General → Workflow permissions**: marca **Read and write permissions** y guarda.
   - **Settings → Pages → Build and deployment → Source**: elige **GitHub Actions**.

## 2. Intervals.icu

1. Crea una cuenta en https://intervals.icu y en **Settings → Connections** conecta **Garmin Connect** (activa actividades y bienestar/wellness).
2. En **Settings → Developer Settings** copia tu **API key**.
3. En GitHub: **Settings → Secrets and variables → Actions → New repository secret**: `INTERVALS_API_KEY` = tu API key.

## 3. Token de Garmin Connect

En tu ordenador, con Python 3.10 o superior:

```bash
python -m pip install 'garminconnect==0.3.17'
python herramientas/crear_token_garmin.py
```

Te pide email, contraseña y (si lo tienes) el código de verificación. Copia la línea que imprime y créala como secreto `GARMIN_TOKENS_B64`. La contraseña no se guarda en ningún sitio. Si algún día Garmin rechaza el token (la app abre un aviso en GitHub), repite este paso.

## 4. Hoja de Google para el RPE

1. Crea una hoja de cálculo nueva llamada **RPE CrossFit - Registro** con dos pestañas:
   - **RPE**, con estas columnas en la fila 1, en este orden: `Fecha`, `ID actividad`, `Actividad`, `RPE`, `Sensaciones`, `Notas`, `Registrado`, `Detalle JSON`.
   - **Peso**, con: `Fecha`, `Hora`, `Peso kg`, `Grasa %`, `Músculo kg`, `Agua %`, `Fuente`, `Notas`.
2. Publica la pestaña **RPE** como CSV: **Archivo → Compartir → Publicar en la web**, elige la pestaña **RPE** y el formato **Valores separados por comas (.csv)**, y pulsa **Publicar**. Copia el enlace.
   - Ese enlace es público para quien lo tenga: no pongas en la hoja nada que no quieras que se vea.
3. En GitHub crea el secreto `RPE_CSV_URL` = ese enlace.
4. Opcional: secreto `RPE_SHEET_ID` = el ID de la hoja (la parte entre `/d/` y `/edit` de su dirección). Solo sirve para que los informes indiquen de qué hoja salen los datos.

Cómo se rellena la hoja (una fila por actividad, emparejada por el **ID de Intervals** de la actividad): ver `REGISTRO_ENTRENAMIENTOS.md`. Si usas Claude (paso 9), lo hace él por ti.

## 5. Clave de firma de los Sync

Los Sync que lanza Apps Script van firmados para que nadie más pueda dispararlos.

1. Genera una cadena aleatoria larga, por ejemplo con `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
2. Créala como secreto `GARMIN_ORIGIN_KEY_V291` en GitHub. Guárdala: la necesitas en el paso 6.

## 6. Apps Script (el reloj que lanza los Sync)

GitHub retrasa varias horas sus tareas programadas, así que quien lanza el Sync a su hora es un Apps Script de Google.

1. **Token de GitHub para Apps Script:** en GitHub, **Settings (de tu perfil) → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**:
   - Repository access: **Only select repositories** → tu `garmin-recovery`.
   - Permissions: **Contents: Read and write**, **Actions: Read**, **Metadata: Read** (sale solo).
   - Caducidad: la más larga que te permita; apunta la fecha para renovarlo.
2. Ve a https://script.google.com → **Nuevo proyecto**, llámalo `garmin-recovery`.
3. Crea un archivo por cada `.gs` de la carpeta `apps_script/` con el mismo nombre y pega su contenido. En **Configuración del proyecto** marca «Mostrar el archivo de manifiesto appsscript.json» y pega `apps_script/appsscript.json`.
4. En `Code.gs`, `GarminPostSueno.gs`, `RespaldoGarmin231.gs` y `Watchdogs.gs` cambia `TU_USUARIO/garmin-recovery` por `tu-usuario-de-github/garmin-recovery`.
5. **Configuración del proyecto → Propiedades del script**:
   - `GITHUB_TOKEN` = el token del punto 1.
   - `GARMIN_ORIGIN_KEY_V291` = la misma clave del paso 5.
6. Selecciona la función `instalarActivadoresGarmin` y pulsa **Ejecutar**. Acepta los permisos que pide Google. En **Activadores** (el reloj) deben quedar `verificarRespaldoGarmin231` y `vigilarPostSuenoGarmin` (cada 5 min) y `repararActivadoresGarmin` (diario).

Franjas: Sync a las **08:30, 16:45 y 22:45** (hora de Madrid), con reintentos. Por la mañana repite el Sync hasta que Garmin confirme el sueño.

## 7. Tus turnos de trabajo (si los tienes)

`shift_calendar.json` empieza vacío. Si no trabajas a turnos, déjalo así y la app trata todos los días igual.

Si trabajas a turnos:
- En `shift_hours` están los turnos que entiende la app (`MT` 08:00–22:00, `TN` 15:00–08:00 del día siguiente, `M` 08:00–15:00). Cambia las horas o añade los tuyos con el mismo formato.
- En `days` pon cada día trabajado: `"2026-12-01": "MT"`. Un turno de noche va en el día en que **empieza**.
- Cuando un mes esté completo, añádelo a `confirmed_months` (`"2026-12"`): sus días sin turno cuentan como libres.
- La app usa los turnos para avisarte del día después de una noche, ajustar el plan y comparar tu recuperación por tipo de día.

## 8. Arranque

1. **Settings → Secrets and variables → Actions → Variables → New repository variable**: `GARMIN_RECOVERY_ACTIVO` = `true`. Sin esta variable las tareas automáticas no corren (así la plantilla no hace nada hasta que esté instalada).
2. **Actions → Garmin Recovery Sync → Run workflow**. Se encadenan solos: Sync → Heart Rate → Advanced Analytics → CrossFit Insights → web. Tarda unos 5 minutos.
3. Abre tu web: `https://tu-usuario-de-github.github.io/garmin-recovery/`. En el móvil puedes «Añadir a pantalla de inicio».
4. Si algo falla, abre la ejecución en rojo en **Actions** y mira el paso que ha fallado. El monitor también abre un aviso (issue) en el repositorio y te llega por email.

Opcional: **Actions → Historial largo de Garmin → Run workflow** descarga tu historial anterior para la tarjeta «¿Cómo he cambiado mes a mes?» (Garmin solo devuelve lo que haya registrado tu reloj).

## 9. Claude (opcional, recomendado)

Con Claude conectado a tu repositorio y a tu hoja puedes dictarle los entrenos («hoy 5x5 de sentadilla a 100 kg, RPE 8») y él los empareja con la actividad de Garmin, los apunta en la hoja, te pasa la encuesta, registra descansos y peso y te redacta el informe tres veces al día.

Sigue `CLAUDE_PROYECTO.md`: crea un proyecto en Claude, pega las instrucciones y conecta GitHub y Google.

## 10. Avisos en el móvil (opcional)

1. Instala la app **ntfy** y suscríbete a un tema con un nombre difícil de adivinar (por ejemplo `garmin-recovery-` + algo aleatorio).
2. Crea el secreto `NTFY_TOPIC` con ese nombre. Recibirás un aviso en el móvil cada vez que haya un informe nuevo.

## Adaptarlo a ti

- **Tu deporte:** la app está pensada para CrossFit (fuerza, halterofilia, metcons), pero funciona con cualquier entrenamiento registrado en Garmin. El RPE de la hoja es lo que más afina la carga: apúntalo siempre que puedas.
- **Zona horaria:** está fijada en **Europe/Madrid** (código, Apps Script y franjas). Si vives en otra zona, hay que cambiarla en `garmin_recovery/` (`Europe/Madrid`), en los `.gs` y en las horas de las franjas.
- **Franjas:** 08:30, 16:45 y 22:45. Se cambian en `apps_script/RespaldoGarmin231.gs` (y, si usas Claude, en la tarea programada).
- **Encuesta:** 7 preguntas fijas (sueño, cansancio, agujetas, molestias, estrés, ánimo, ganas) y 4 de contexto (comida, agua, alcohol, rendimiento). Están en `garmin_recovery/sensations.py`.
- **Tests de referencia** (Fran, Grace, Helen, remo 500 m, dominadas máx., 3RM): en `garmin_recovery/coaching.py`. Haz uno cada 6–8 semanas para medir progreso real.

## Mantenimiento

- **Token de Garmin:** si caduca, repite el paso 3.
- **Token de GitHub de Apps Script:** renuévalo antes de que caduque (paso 6.1) y cambia la propiedad `GITHUB_TOKEN`.
- **Turnos:** añade cada mes a `shift_calendar.json`.
- Documentación técnica: `README.md`, `MAINTENIMIENTO.md` y `OPERACION_Y_VALIDACION.md`.

La app describe tus datos y propone una intensidad; **no es un diagnóstico médico**.
