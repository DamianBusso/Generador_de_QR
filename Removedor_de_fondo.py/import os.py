import os
from PIL import Image
from rembg import remove
import streamlit as st

def save_uploaded_file(uploaded_file):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    try:
        # Guardar el archivo en la ruta especificada
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write(f"Archivo guardado en: {file_path}")  # Mensaje de depuración
        return file_path
    except Exception as e:
        st.error(f"Error al guardar el archivo: {e}")
        return None

def run_background_remover(input_img_file):
    input_img_path = save_uploaded_file(input_img_file)
    
    # Verificar si se guardó correctamente el archivo
    if input_img_path is None:
        st.error("Error: No se pudo guardar el archivo.")
        return
    
    # Evitar el error de 'NoneType' en replace al verificar si input_img_path es válido
    if input_img_path:
        output_img_path = input_img_path.replace('.', '_rmbg.').replace('jpg', 'png').replace('jpeg', 'png')
    else:
        st.error("Error: No se pudo procesar la ruta de la imagen.")
        return
    
    try:
        # Abrir la imagen y procesarla
        image = Image.open(input_img_path)
        output = remove(image)
        output.save(output_img_path, "PNG")

        # Mostrar la imagen antes y después
        col1, col2 = st.columns(2)
        with col1:
            st.header("Antes")
            st.image(input_img_path, caption="Imagen Original")
            with open(input_img_path, "rb") as img_file:
                st.download_button(
                    label="Descargar Imagen Original",
                    data=img_file,
                    file_name=os.path.basename(input_img_path),
                    mime="image/jpeg"
                )
        with col2:
            st.header("Después")
            st.image(output_img_path, caption="Imagen con Fondo Removido")
            with open(output_img_path, "rb") as img_file:
                st.download_button(
                    label="Descargar Imagen Procesada",
                    data=img_file,
                    file_name=os.path.basename(output_img_path),
                    mime="image/png"
                )
        st.success("Fondo removido exitosamente")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar la imagen: {e}")

def main():
    st.title("Removedor de Fondos")
    uploaded_file = st.file_uploader("Elige un archivo de imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        run_background_remover(uploaded_file)

if __name__ == "__main__":
    main()
