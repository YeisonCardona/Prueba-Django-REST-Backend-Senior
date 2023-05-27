# Prueba-Django-REST-Backend-Senior

## Objetivo:
Desarrollar una API RESTful para una plataforma de blog con funcionalidades
avanzadas utilizando Django REST Framework y Python como lenguaje de
programación principal.

## Descripción del Proyecto:
La plataforma de blog consta de varias entidades: Usuarios, Perfiles, Entradas
(Posts), Comentarios y Likes. Los Usuarios pueden tener roles de administrador,
editor o blogger. Los Usuarios tienen un Perfil asociado con información
adicional como la biografía y la imagen de perfil. Las Entradas están asociadas
a un Usuario (el autor) e incluyen un título, contenido, fecha de publicación,
categoría y una lista de etiquetas (tags). Los Comentarios están vinculados a
un Usuario (la persona que comenta) y a una Entrada, e incluyen el texto del
comentario. Los Usuarios pueden dar Like tanto a Entradas como a Comentarios.

## Requisitos del proyecto:

 1. **Modelado de Datos:** Diseña e implementa modelos de datos para Usuario,
 Perfil, Entrada, Comentario y Like.
 1. **Autenticación y Autorización:** Implementa un sistema de autenticación y
 autorización que permita a los administradores gestionar todos los recursos,
 a los editores gestionar Entradas, Comentarios y Likes, y a los bloggers crear
 y gestionar sus propias Entradas, Comentarios y Likes.
 1. **API Endpoints:** Implementa los siguientes endpoints:
	 * CRUD de Usuarios y Perfiles
	 * CRUD de Entradas
	 * CRUD de Comentarios
	 * CRUD de Likes
 1. **Serialización:** Emplea los serializadores de Django REST para manejar
    la conversión entre modelos y JSON.
 1. **Filtros y Paginación:** Implementa filtros que permitan buscar
    entradas por título, autor, categoría y etiquetas. Además,
    implementa la paginación en los endpoints que devuelven múltiples
    recursos.
 1. **Pruebas:** Desarrolla pruebas unitarias y de integración para los
    modelos, la autenticación, la autorización y los endpoints de la
    API. Asegúrate de cubrir tanto los casos de éxito como los de error.
 1. **Documentación:** Documenta todos los endpoints de la API utilizando
    Django REST Swagger o similar.

## Instrucciones de entrega:
Por favor, sube tu solución a un repositorio de GitHub y comparte el enlace con
nosotros. Asegúrate de incluir un archivo README con instrucciones detalladas
sobre cómo instalar y ejecutar el proyecto, cómo ejecutar las pruebas, y
cualquier información relevante.

## Fecha límite:
Te pedimos que completes y envíes la prueba técnica el día
**Viernes 26 de Mayo del 2023 11:59pm (GTM-5)**

## Criterios de evaluación:
Nuestro equipo evaluará la calidad del código, el cumplimiento de los
requisitos, la selección de herramientas y técnicas utilizadas, la cobertura de
las pruebas, la correcta implementación de la paginación y los filtros, así
como la calidad de la documentación de la API.
