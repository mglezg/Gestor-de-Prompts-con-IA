# Política de Seguridad

## Titularidad y derechos de autor

Este software, **Prompt Manager**, es una obra original desarrollada y mantenida por su autor.
Todos los derechos de autor están reservados conforme a los términos de la **Licencia Apache 2.0**,
cuya copia completa se encuentra en el archivo `LICENSE` de este repositorio.

La Licencia Apache 2.0 protege explícitamente al titular original frente a:

- El uso del nombre del autor para promocionar obras derivadas sin permiso expreso
- La eliminación o modificación de los avisos de copyright en copias redistribuidas
- La atribución falsa de autoría en trabajos derivados

Cualquier distribución, modificación o uso de este software debe mantener íntegros
los avisos de copyright originales tal y como exige el punto 4 de la Licencia Apache 2.0.

---

## Versiones con soporte de seguridad

| Versión | Soporte activo |
|---------|---------------|
| 1.3     | Sí ✅         |
| 1.2     | No ❌         |
| 1.1     | No ❌         |
| 1.0     | No ❌         |

Se recomienda actualizar a la versión **1.3** para recibir correcciones de seguridad y soporte activo.
Las versiones anteriores no recibirán parches ni actualizaciones de ningún tipo.

---

## Reporte de vulnerabilidades

Si descubres una vulnerabilidad de seguridad en este proyecto, te pedimos que sigas
un proceso de **divulgación responsable** antes de hacerla pública.

### Cómo reportar

1. **No abras un issue público** con detalles de la vulnerabilidad.
2. Contacta directamente con el autor a través de los canales de contacto indicados en el repositorio.
3. Incluye en tu reporte:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducirla
   - Impacto potencial estimado
   - Si es posible, una propuesta de solución o mitigación

### Qué puedes esperar

- Confirmación de recepción en un plazo razonable
- Evaluación de la vulnerabilidad reportada
- Notificación cuando el problema haya sido corregido
- Reconocimiento público en el changelog si así lo deseas

---

## Alcance

Este proyecto es una aplicación web local que corre íntegramente en el equipo del usuario.
No expone servicios en red pública por defecto. Las únicas comunicaciones externas son
las llamadas opcionales a APIs de terceros (Anthropic, OpenAI, DeepSeek) cuando el
usuario configura explícitamente sus propias claves de API.

Las claves de API se almacenan localmente en `data/.env.keys`, un archivo que **nunca
debe incluirse en repositorios públicos**. Este archivo ya está excluido mediante `.gitignore`.

---

## Aviso legal

> El incumplimiento de los términos de la Licencia Apache 2.0 por parte de terceros,
> incluyendo la eliminación de avisos de copyright, la atribución falsa de autoría o
> la redistribución sin los términos de licencia requeridos, puede constituir una
> infracción de los derechos de propiedad intelectual del autor y ser perseguible
> conforme a la legislación aplicable.
