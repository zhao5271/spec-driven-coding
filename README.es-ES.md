

# Codificación Guiada por Especificaciones

`spec-driven-coding` es un flujo de trabajo que prioriza la especificación (spec-first) para Codex, manteniendo la planificación en archivos en lugar de en la memoria del chat.

Úsalo cuando desees un flujo repetible como:

`spec.md -> tasks.md -> implementation -> verification`

Está diseñado para ayudarte a:

- inicializar un repositorio con un paquete de flujo de trabajo `code_copilot/` reutilizable
- crear un paquete de cambios antes de codificar
- mantener `spec.md` y `tasks.md` como la fuente de verdad durante la ejecución
- recuperar el contexto de forma limpia al reanudar una sesión

## Inicio Rápido

Instala la habilidad principal desde GitHub:

```bash
npx skills add zhao5271/spec-driven-coding -g -y
```

Instala el paquete completo desde este repositorio:

```bash
git clone git@github.com:zhao5271/spec-driven-coding.git
cd spec-driven-coding
./install.sh
```

Elige la instalación de la habilidad principal si solo quieres el flujo de trabajo principal.

Elige la instalación del paquete completo si también quieres las habilidades complementarias incluidas en este repositorio.

## Primer Prompt

Inicializa un repositorio:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

Inicia un nuevo cambio:

```text
用 $spec-driven-coding 先为“用户批量导入”创建 change package，再写 spec 和 tasks
```

Solicitar ayuda:

```text
$spec-driven-coding --help
```

## Guía Rápida del Flujo de Trabajo

La secuencia corta de comandos es:

`建包 -> 写规 -> 开整 -> 续做 -> 校验 -> 收尾`

- `建包`: inicializar `code_copilot/` para el repositorio actual
- `写规`: crear un cambio y redactar `spec.md` y `tasks.md`
- `开整`: continuar la implementación desde el plan aprobado
- `续做`: escanear cambios existentes y recuperar el contexto de ejecución
- `校验`: mover el cambio a verificación y comprobar la preparación para el cierre
- `收尾`: cerrar el paquete de cambios

## Lo que esto crea

Cuando inicializas un repositorio, el flujo de trabajo crea un paquete `code_copilot/` con:

- `rules/` para reglas estables del proyecto
- `knowledge/` para conocimiento duradero del proyecto
- `agents/` para guía de ejecución reutilizable
- `changes/templates/` para plantillas de paquetes de cambios

Cuando inicias una funcionalidad real o una corrección de error, el flujo de trabajo crea:

- `change.toml`
- `spec.md`
- `tasks.md`
- `log.md`
- `decisions.md`
- `review.md`

La regla de funcionamiento es simple:

- sin especificación antes de codificar
- `spec.md` es el plan
- `tasks.md` es la instantánea de la ejecución
- `log.md` es el registro cronológico

## Habilidades Incluidas

Flujo de trabajo principal:

- `spec-driven-coding`

Habilidades complementarias en el paquete completo:

- `frontend-design` para trabajo concentrado en la UI
- `api-design-principles` para trabajo de API y contratos
- `postgresql-table-design` para trabajo de esquemas de PostgreSQL
- `test-driven-development` para nueva implementación y refactorizaciones
- `systematic-debugging` para investigación de errores
- `verification-before-completion` para validación en la puerta de salida
- `requesting-code-review` para cambios de alto riesgo

## Scripts Principales

La habilidad principal incluye estos scripts de flujo de trabajo:

```bash
python3 scripts/scaffold_package.py --target /path/to/repo --project-name my-app
python3 scripts/create_change.py --target /path/to/repo --name add-bulk-import --title "Add bulk import flow"
python3 scripts/approve_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status in_progress --current-task T1
python3 scripts/change_catchup.py --target /path/to/repo --change add-bulk-import
python3 scripts/validate_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/close_change.py --target /path/to/repo --change add-bulk-import
```

## Opciones de Instalación

Dos formas soportadas para usar este proyecto:

- `npx skills add zhao5271/spec-driven-coding -g -y`
  Esto instala la habilidad de flujo de trabajo raíz desde GitHub.
- `git clone ... && ./install.sh`
  Esto instala el paquete completo, incluyendo las habilidades complementarias.

Si deseas una versión fija (pinned), utiliza una etiqueta de Git o una revisión específica del repositorio en tu propio flujo de instalación.

Más detalles se encuentran en [references/public-install-and-release.md](references/public-install-and-release.md).

## Preguntas Frecuentes

### ¿Requiere una pila tecnológica específica?

No. El flujo de trabajo es intencionalmente genérico. Funciona mejor cuando registras los detalles reales de la pila en los archivos `rules/` generados.

### ¿Necesito el paquete completo?

No. Si solo quieres el flujo de trabajo de planificación principal, instala la habilidad principal. Usa el paquete completo si quieres las habilidades complementarias listas para usar.

### ¿Puedo usarlo con otras habilidades enfocadas en la ejecución?

Sí. Ese es el modelo previsto. `spec-driven-coding` se encarga de la planificación, mientras que las habilidades enfocadas en la ejecución mejoran las pruebas, la depuración, la verificación o la revisión.

### ¿Qué debo escribir primero?

Usualmente uno de estos:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

```text
用 $spec-driven-coding 先写 spec 和 tasks，再开始改这个功能
```

### ¿Dónde puedo leer más?

- `references/workflow.md`
- `references/spec-checklists.md`
- `references/task-splitting-examples.md`
- `references/stack-conventions.md`
- `references/skill-routing.md`
- `references/skill-decision-table.md`
- `references/superpowers-integration.md`
- `references/中文说明.md`
