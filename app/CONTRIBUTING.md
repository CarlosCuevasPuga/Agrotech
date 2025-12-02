# Guía de Contribución para Agrotech

¡Gracias por tu interés en contribuir a Agrotech! Este documento establece las pautas para contribuir al proyecto y asegurar que mantengamos una alta calidad en el código.

## 🚀 Cómo Empezar

1. **Fork del Repositorio**: Crea una copia del proyecto en tu cuenta de GitHub.
2. **Clonar**: Clona tu fork a tu máquina local.
3. **Rama (Branch)**: Crea una rama para tu funcionalidad o corrección de bug.
   bash
   git checkout -b feature/nueva-funcionalidad
   # o
   git checkout -b fix/descripcion-del-bug
   

## 💻 Entorno de Desarrollo

Asegúrate de tener configurado el entorno como se describe en el `README.md`. Recomendamos usar `black` para el formateo de código Python.

## 📏 Estándares de Código

### Python / Reflex
- **Type Hints**: Utiliza tipado estático (`str`, `int`, `list[dict]`, etc.) siempre que sea posible, especialmente en los Estados (`rx.State`) y Modelos.
- **Estructura de Archivos**: 
  - Los estados deben ir en `app/states/`.
  - Los componentes reutilizables en `app/components/`.
  - La lógica de base de datos **siempre** debe ir en `DatabaseManager` (`app/backend/database.py`), nunca consultas SQL directas en los States.
- **Manejo de Errores**: Usa bloques `try/except` para operaciones de I/O y loguea los errores usando `logging.exception`.

### Estilos (TailwindCSS)
- Utiliza las clases de utilidad de Tailwind directamente en el argumento `class_name`.
- Para lógica condicional de estilos, usa `rx.cond` o `rx.match`, nunca f-strings con lógica Python compleja.

## 🔄 Flujo de Trabajo

1. **Implementa tus cambios**.
2. **Prueba tu código**: Asegúrate de que la aplicación arranca y la funcionalidad nueva trabaja como se espera.
3. **Commit**: Escribe mensajes de commit claros y descriptivos.
   bash
   git commit -m "feat: añade gráfico de barras a analíticas"
   
4. **Push**: Sube los cambios a tu fork.
   bash
   git push origin feature/nueva-funcionalidad
   
5. **Pull Request (PR)**: Abre un PR hacia la rama `main` del repositorio original. Describe qué cambios has hecho y por qué.

## 🐛 Reportar Bugs

Si encuentras un error, por favor abre un Issue en GitHub incluyendo:
- Pasos para reproducir el error.
- Comportamiento esperado vs. comportamiento real.
- Capturas de pantalla o logs si es relevante.

---

¡Tu ayuda es fundamental para hacer de la agricultura tecnológica una realidad accesible! 🌱
