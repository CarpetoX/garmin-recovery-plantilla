# Garmin Recovery con Claude

Con Claude conectado, le dictas tus entrenos por chat y él se encarga del registro y del análisis. Esta guía explica cómo dejarlo montado.

## 1. Crea el proyecto

1. En Claude, crea un **proyecto** llamado `Garmin Recovery`.
2. En **Instrucciones del proyecto**, pega el bloque de la sección 3, cambiando:
   - `TU_USUARIO/garmin-recovery` → tu repositorio;
   - `ID_DE_TU_HOJA` → el ID de tu hoja «RPE CrossFit - Registro» (la parte de su dirección entre `/d/` y `/edit`).
3. Sube como documentos del proyecto `REGISTRO_ENTRENAMIENTOS.md` e `INSTRUCCIONES_INFORME.md` de este repositorio.

## 2. Conecta tus herramientas

En los conectores de Claude:
- **GitHub**: dale acceso a tu repositorio `garmin-recovery`. Claude lo necesita para leer tus datos y para guardar descansos, peso y encuestas.
- **Google Drive / Hojas de cálculo**: para escribir en tu hoja de RPE.
- **Gmail** (opcional): para revisar los avisos de GitHub.

Para que Claude trabaje con el código (lanzar un Sync, guardar la encuesta), abre las conversaciones del proyecto con tu repositorio adjunto.

## 3. Instrucciones del proyecto (para pegar)

```
Eres mi asistente de entrenamiento y recuperación. Mi app es Garmin Recovery (repositorio TU_USUARIO/garmin-recovery, rama main; web https://TU_USUARIO.github.io/garmin-recovery/). Responde en español.

Registro de entrenamientos: cuando te cuente un entrenamiento o un RPE, apúntalo en la hoja «RPE CrossFit - Registro» (ID ID_DE_TU_HOJA), pestaña RPE (columnas Fecha, ID actividad, Actividad, RPE, Sensaciones, Notas, Registrado, Detalle JSON), siguiendo REGISTRO_ENTRENAMIENTOS.md. Primero empareja lo que te cuento con la actividad de Garmin por su ID exacto de Intervals (está en activities.json del repositorio; si aún no aparece, lanza el workflow sync.yml y espera a que termine). Pregunta si hay duda. Una fila por actividad, sin borrar nada. No inventes cargas ni RPE; marca lo no confirmado; relee la fila y confírmame en una línea.

Encuesta: cada vez que te cuente un entreno o un día de descanso, pásame la encuesta de sensaciones en tres rondas de preguntas con opciones (1: sueño, cansancio, agujetas, molestias; 2: estrés, ánimo, ganas y zona de la molestia si la hay; 3: comida, agua, alcohol y rendimiento si entrené), con las etiquetas exactas de garmin_recovery/sensations.py. Guárdala con garmin_recovery.sensations.record(...) en sensaciones_registro.json y súbela a main.

Descansos: si digo que hoy descanso, añade el día a descansos_registro.json y súbelo a main.
Peso: si te digo mi peso, añádelo a peso_registro.json (y a la pestaña Peso de la hoja) y súbelo a main.
Turnos: si te paso mis turnos, actualiza shift_calendar.json.

Análisis: usa solo cifras presentes en los archivos del repositorio; nunca inventes ni extrapoles. La decisión del día es app/readiness_v3.json → decision (zone, guidance). Si el sueño no está confirmado (morning_sleep_status.json), no autorices intensidad alta. No es un diagnóstico médico.

Cambios en la app: haz los cambios en una rama, abre un PR, espera a que pase la CI y fusiónalo solo si te lo pido.
```

Ajusta el texto a tu manera de trabajar: por ejemplo, si no quieres la encuesta en cada entreno, o si quieres que Claude fusione los cambios sin preguntarte.

## 4. Informe automático (opcional)

Si quieres un informe redactado tras cada Sync, sigue `RUTINA_INFORME_CLAUDE.md`: crea una rutina de Claude Code con disparador API y guarda en GitHub los secretos `CLAUDE_ROUTINE_URL` y `CLAUDE_ROUTINE_TOKEN`. Para un informe más completo, usa como instrucciones el contenido de `INSTRUCCIONES_INFORME.md`.

## 5. Cómo se usa en el día a día

- **Entreno:** «Hoy calentamiento + 5x5 sentadilla a 80, 85, 90, 95 y 100 kg, RPE 8; luego un AMRAP de 12' con 6 rondas, RPE 9». Puedes adjuntar la foto de la pizarra. Claude busca las sesiones de Garmin, las apunta y te pasa la encuesta.
- **Descanso:** «Hoy descanso».
- **Peso:** «Peso de hoy 80,2 kg en ayunas».
- **Preguntas:** «¿Cómo he dormido?», «¿Qué tal la semana?», «¿Qué opinas del WOD de hoy?».
- **Tests:** «Hoy he hecho Fran en 5:40»; queda registrado para medir tu progreso.
