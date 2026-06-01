import streamlit as st
import requests

# Configuración inicial de la página
st.set_page_config(page_title="Buscador de Recetas", page_icon="🍲", layout="centered")

st.title("🍳 Buscador de Recetas Super Pro")
st.write("Escribe el nombre de un plato o un ingrediente principal para descubrir su receta.")

# Entrada de texto del usuario
busqueda = st.text_input("¿Qué te apetece cocinar hoy?", placeholder="Ej. Chicken, Arrabiata, Rice...")

# Función para procesar y formatear ingredientes
def obtener_ingredientes(meal):
    ingredientes = []
    for i in range(1, 21):
        ingrediente = meal.get(f"strIngredient{i}")
        medida = meal.get(f"strMeasure{i}")
        
        # Validar que el ingrediente no esté vacío
        if ingrediente and ingrediente.strip():
            if medida and medida.strip():
                ingredientes.append(f"- **{ingrediente.strip()}**: {medida.strip()}")
            else:
                ingredientes.append(f"- **{ingrediente.strip()}**")
    return ingredientes

# Ejecutar la búsqueda si hay texto
if busqueda:
    # Endpoint de búsqueda por texto de TheMealDB (usando la API key gratuita '1')
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={busqueda}"
    
    with st.spinner("Buscando recetas sabrosas..."):
        try:
            response = requests.get(url)
            data = response.json()
            recetas = data.get("meals")
            
            if recetas:
                st.success(f"¡Se encontraron {len(recetas)} recetas!")
                st.write("---")
                
                # Desplegar cada receta encontrada
                for meal in recetas:
                    st.header(meal["strMeal"])
                    
                    # Categoría y Región (Etiquetas simples)
                    st.caption(f"📁 **Categoría:** {meal.get('strCategory')} | 🌍 **Origen:** {meal.get('strArea')}")
                    
                    # Diseño en dos columnas: Foto e Ingredientes
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if meal.get("strMealThumb"):
                            st.image(meal["strMealThumb"], use_container_width=True)
                    
                    with col2:
                        st.subheader("Ingredientes:")
                        lista_ingredientes = obtener_ingredientes(meal)
                        for ing in lista_ingredientes:
                            st.write(ing)
                    
                    # Instrucciones en la parte inferior
                    st.subheader("Instrucciones de preparación:")
                    st.write(meal["strInstructions"])
                    
                    # Enlace opcional a YouTube si existe
                    video_url = meal.get("strYoutube")
                    if video_url:
                        st.video(video_url)
                        
                    st.write("---") # Separador entre recetas
            else:
                st.warning("No se encontraron recetas con ese nombre o ingrediente. ¡Prueba en inglés! (Ej: 'Tomato', 'Beef', 'Pasta')")
                
        except Exception as e:
            st.error("Hubo un error al conectar con la API. Inténtalo de nuevo.")