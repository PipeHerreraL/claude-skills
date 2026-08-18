# claude-skills - marketplace publico

Marketplace de plugins de Claude Code con las skills propias que no manejan
informacion confidencial.

| Plugin | Skill | Que hace |
|---|---|---|
| `planificador-rutas` | `planificador-rutas` | Entrevista al usuario, verifica si la ruta cabe en los dias disponibles y entrega el itinerario como HTML estatico y PDF |

Las skills que trabajan con documentacion confidencial viven en el repositorio
privado `claude-skills-privado`.

## Instalar en Claude Code

```shell
/plugin marketplace add PipeHerreraL/claude-skills
/plugin install planificador-rutas@pipe-skills
```

Si el resumen de instalacion pide `Run /reload-plugins to activate.`, correlo.

## Actualizar

Haga push y, desde Claude Code:

```shell
/plugin marketplace update pipe-skills
```

El `plugin.json` no declara `version` a proposito: en fuentes de git, cuando se
omite ese campo Claude Code usa el SHA del commit como version, asi que cada
commit se propaga como actualizacion. Si algun dia quiere congelar versiones,
agregue `"version"` y subalo en cada release: si lo declara y no lo cambia, los
usuarios se quedan con la copia en cache.

## Usar en claude.ai

claude.ai no se sincroniza con Git en planes individuales: hay que subir el
archivo `.skill`. Para generarlo:

```bash
python3 scripts/empaquetar.py plugins/planificador-rutas/skills/planificador-rutas
```

Queda en `dist/planificador-rutas.skill`, listo para subir.

## Validar antes de publicar

```bash
claude plugin validate .
claude plugin validate ./plugins/planificador-rutas
```

## Estructura

```
.claude-plugin/marketplace.json     catalogo: nombre, dueno y lista de plugins
plugins/planificador-rutas/
  .claude-plugin/plugin.json        manifiesto del plugin
  skills/planificador-rutas/
    SKILL.md                        la skill
    references/                     entrevista, planificacion, formato del plan, datos
    scripts/                        generador de HTML, conversor a PDF, dibujo de mapas
    assets/                         plan de ejemplo completo
scripts/empaquetar.py               genera el .skill para claude.ai
```

`metadata.pluginRoot` esta fijado en `./plugins`, por eso cada entrada del
marketplace referencia su plugin con el nombre de la carpeta y no con la ruta
completa.

## Agregar una skill nueva

1. `plugins/<nuevo>/skills/<nuevo>/SKILL.md` con su frontmatter `name` y `description`.
2. `plugins/<nuevo>/.claude-plugin/plugin.json` con `name` y `description`.
3. Una entrada mas en el array `plugins` de `.claude-plugin/marketplace.json`.
4. `claude plugin validate .` y push.

Si renombra o elimina un plugin, agregue una entrada en `renames` del
`marketplace.json` para que quien lo tenga instalado migre en vez de ver un error.