# Marcos de Confiabilidad para Agentes IA (2025-2026)

## Lo Simple

**La confiabilidad depende de infraestructura, no de modelos más fuertes.**

En 18 meses (2024-2025):
- Precisión: +0.21/año ⬆️
- Confiabilidad: +0.03-0.15/año ⬆️ (muy rezagada)

Esto significa: tu agente es tan confiable como su memoria, herramientas y verificación, no su modelo base.

---

## Lo Crítico: Modos de Fallo en Agentes

Analizado: 385 fallos en agentes (Shah et al., Mayo 2026)

| Causa | % Fallos | Fix |
|-------|---------|-----|
| **Schema Mismatches** | 28.0% | Type-safe tool schemas |
| **Dependency Drift** | 21.9% | Dependency graphs |
| **Orchestration Errors** | ~15% | Explicit policy enforcement |
| Otros | ~35% | Memory + verification |

---

## La Tabla: 6 Dimensiones de Confiabilidad

| Dimensión | Framework | Overhead | Impacto | Mejor Para |
|-----------|-----------|----------|--------|------------|
| **1. Razonamiento** | Chain of Thought | +10-20% tokens | Baseline | Tareas simples |
| | ReAct | +15-30% tokens | ✅ Recomendado | Workflows típicos |
| | Tree of Thought | +100-300% tokens | Alto (caro) | Problemas complejos |
| | Self-Refinement | +50-200% tokens | Muy alto | Calidad crítica |
| **2. Verificación** | Self-Checking | +20-30% tokens | Medio | Rápido + iterativo |
| | Adversarial (3-votos) | +200-300% tokens | ✅ Muy alto | Decisiones críticas |
| | Gradient of Verification | Variable | Alto | Enterprise (risk-based) |
| | Trace-First Flywheel | +5% overhead | Medio (continuo) | Mejora iterativa |
| **3. Memoria** | Artifact Archiving | Bajo | ✅ Alto | Proyectos largos |
| | Working Memory (fresco) | Setup | ✅ Muy alto | Evitar context bloat |
| | Lossy Summarization | +10-20% tokens | Medio | Space-constrained |
| | Cognitive Corruption Governance | Alto | Muy alto | Multi-turn complejo |
| **4. Composición** | Type-Safe Schemas | ~0% overhead | ✅✅ CRÍTICO | Baseline obligatorio |
| | Explicit Handoff | +5-10% latency | Alto | Prevent cascades |
| | Dependency Graphs | Setup | Alto | Tool chains complejos |
| | Retry + Fallback | Variable | Medio | Resiliencia |
| **5. Integrated** | Constitutional Governance | Arquitectónico | Muy alto | Policy enforcement |
| | AgentRx Debugging | Per-failure | Alto | Análisis post-mortem |
| | Wave-Based Execution | Scheduling | ✅ Muy alto | Multi-path + flexible |

---

## Stack Mínimo para Solo Dev

**Semana 1-2 (30-40% mejora confiabilidad):**
1. ✅ Type-safe tool schemas (previene 28% de fallos)
2. ✅ Artifact archiving (evitar context bloat)
3. ✅ Trace-first logging (5% overhead, mining continuo)

**Semana 3-4 (agregar 20-30% mejora):**
4. ⚡ Adversarial verification para decisiones críticas
5. ⚡ Working memory isolation por fase

---

## Lo Detallado

### 1. Razonamiento

**Chain of Thought**: Agente escribe paso-a-paso. Costo: +10-20% tokens. Baseline.

**ReAct** (⭐ Recomendado): Alterna razonamiento + acción. Trazable. Costo: +15-30% tokens. **Mejor relación cost-benefit.**

**Tree of Thought**: Explora múltiples caminos en paralelo. Costo: +100-300%. Solo para problemas muy complejos.

**Self-Refinement**: Genera → critica → mejora iterativamente. Costo: +50-200%. Máxima calidad, lento.

---

### 2. Verificación & Validación

**Self-Checking**: Agente valida su propia salida. Rápido, barato, pero pierde errores que ya cometió.

**Adversarial (⭐ Para crítico)**: 3 agentes votan. Respuesta sobrevive si 2/3 la aprueban. Mata falsos positivos. Costo: +200-300% tokens, latencia.

**Gradient of Verification**: Ajusta rigor según riesgo de acción. Acciones bajas = verificación mínima. Críticas = verificación formal. Prometedor, sin validación aún.

**Trace-First Flywheel**: Registra todo (prompts, herramientas, salidas, resultados). Extrae patrones de fallos continuamente. Overhead: +5% (solo logging).

---

### 3. Memoria & Contexto

**Problema:** Cognitive Corruption — degradación no observada:
- Semantic eviction (contexto saturo evicta por probabilidad, no importancia)
- Attention variance (lost-in-the-middle)
- Hallucinated summarization (resumir introduce alucinaciones)

**Artifact Archiving** (⭐ Recomendado): Trabajo completado → archivo buscable. Recupera cuando se necesita. Bajo overhead, muy flexible.

**Working Memory** (⭐ Para tareas largas): Cada tarea = ventana 200k fresca ensamblada desde artefactos, no chat. Usado por GSD (61k stars). Setup inicial, luego eficiente.

**Lossy Summarization**: Comprime contexto antiguo → resúmenes semánticos. Costo: +10-20% tokens.

**Cognitive Corruption Governance**: Kernel OS-level (5 núcleos: Cognitive, Memory, Execution, Normative, Metacognitive). Arquitectura pesada, teóricamente sólida.

---

### 4. Composición de Herramientas

**⭐ CRÍTICO: Type-Safe Schemas — previene 28% de fallos**

Problema: Agente genera salida que no coincide con estructura esperada de siguiente herramienta.

Solución: Inputs/outputs fuertemente tipificados. Rechaza mismatches. Overhead: ~0% (compile-time). **Obligatorio.**

**Dependency Drift** (21.9% de fallos): Agente usa herramienta antes de que dependencias estén listas.

Solución: Dependency graphs. Sistema sabe orden correcto.

**Explicit Handoff**: Valida salida herramienta antes de pasar a siguiente. Costo: +5-10% latencia.

**Retry + Fallback**: Si A falla, intenta B o retrocede.

---

### 5. Marcos Integrados

**Constitutional Governance**: Kernel externo enforces políticas en 5 núcleos:
- Cognitive (razonamiento)
- Memory (working memory, relevancia)
- Execution (interfaz mundo)
- Normative (políticas, restricciones)
- Metacognitive (reflexión, auditoria)

Ventaja: Políticas en kernel, no en modelo. Auditoria post-hoc.
Desventaja: Rediseño arquitectónico.

**AgentRx** (Microsoft, Marzo 2026): Debugging sistemático 4-etapas:
1. Trajectory Normalization (estandariza logs)
2. Constraint Synthesis (genera reglas desde esquemas)
3. Guarded Evaluation (ejecuta contra restricciones)
4. LLM-Based Judging (identifica causa raíz)

Resultado: +23.6% precision en localización de fallos.
Uso: Análisis post-mortem cuando fallos misteriosos.

**Wave-Based Execution** (GSD): Cada wave = contexto fresco 200k desde artefactos. Subagentes aislados. Resultados verificados antes siguiente wave.

Ventaja: Flexible, evita bloat.
Desventaja: Overhead scheduling.

---

## Ranking de Impacto (Qué Realmente Mejora)

1. **Infraestructura cognitiva externa** (memoria, habilidades, protocolos) — **multiplicador más grande**
2. **Type-safe tool schemas** — **previene 28% de fallos**
3. **Patrones verificador/crítico** — vinculan decisiones a evidencia
4. **Risk-aware branching** — acciones críticas = verificación más profunda
5. **Prompt robustness tuning** — diferenciador clave entre modelos
6. **Constitutional governance** — enforces en kernel

---

## Para Claude Code / Hermes / Codex

### Día 1

**Type-safe schemas** ← empieza aquí. Previene 28% de fallos. Overhead: ~0%.

### Semana 1

- Artifact archiving (evitar bloat en tareas largas)
- Trace-first logging (5% overhead, data para mejora)

### Semana 2

- Adversarial verification para decisiones críticas (2/3 agentes votan)

### Mes 2+

- Working memory isolation (contexto fresco por fase)
- Gradient of verification (escala rigor por riesgo)
- AgentRx para debugging (cuando fallos misteriosos)

---

## Verdades Incómodas

- **Precision ≠ confiabilidad.** No basta un modelo mejor.
- **Prompt robustness varía enormemente.** Mismo modelo, diferentes prompts = tasas de fallo muy diferentes.
- **Sin bala de plata.** Cada dimensión requiere esfuerzo separado.
- **El overhead importa.** Tree of Thought = 3-5x más caro que ReAct. Elige según restricciones.
- **Todavía es nuevo.** Frameworks 2025-2026; estabilidad a largo plazo sin probar.

---

## Fuentes Verificadas

- **Rabanser et al.** (Feb 2026): 15 modelos agentes. Divergencia accuracy-reliability 18 meses.
- **Shah et al.** (Mayo 2026): 385 fallos, 40 repos. Schema mismatches 28%, dependency drift 21.9%.
- **Xu et al.** (Oct 2025): Constitutional governance + Cognitive Corruption.
- **Microsoft Research** (Marzo 2026): AgentRx framework. +23.6% precision.
- **GSD** (61k stars, Dec 2025): Wave-based execution.

---

## Próximo Paso

¿Skill template para cuál?
- Type-safe tool composition (baseline)
- Adversarial verification (crítico)
- Working memory + artifact archiving (contexto)
- Gradient of verification (risk-based)
