import subprocess
import PyPDF2
import tempfile
import os

def unlock_pdf(input_pdf_path, output_pdf_path, password):
    with open(input_pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PyPDF2.PdfWriter()
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        with open(output_pdf_path, "wb") as unlocked_pdf_file:
            writer.write(unlocked_pdf_file)

def sign_pdf_with_executable(input_pdf_path, output_pdf_path):
    executable_path = r"C:\Dados Gilberto\Projetos\Scribo\AssinarPdfCLI\bin\Release\net8.0\win-x64\AssinarPdfCLI.exe"
    command = [executable_path, input_pdf_path, output_pdf_path]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("PDF assinado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao assinar PDF: {e.stderr}")

def unlock_and_sign_pdf(input_pdf_path, password, signed_pdf_path):
    # Cria um arquivo temporário para o PDF desbloqueado
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf_path = temp_pdf.name

    try:
        # Desbloqueia o PDF protegido por senha
        unlock_pdf(input_pdf_path, temp_pdf_path, password)
        
        # Chama o executável para assinar o PDF desbloqueado
        sign_pdf_with_executable(temp_pdf_path, signed_pdf_path)
    finally:
        # Remove o arquivo temporário após a assinatura
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

# Exemplo de uso
#input_pdf = "protegido.pdf"
#password = "senha_do_pdf"
#signed_pdf = "assinado.pdf"
#unlock_and_sign_pdf(input_pdf, password, signed_pdf)

