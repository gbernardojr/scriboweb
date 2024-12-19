import os
import requests
import msal
import qrcode  # Certifique-se de instalar a biblioteca qrcode: pip install qrcode[pil]


class OneDriveUpload:
    # Credenciais do aplicativo do Azure AD
    client_id = "2b2c4841-1ec5-4b41-9628-e60694cf787e"
    client_secret = "EQ18Q~g40YcbLRFcB1XtHiFyU7fk6mjgtP3PSaO_"
    tenant_id = "a7720652-3d80-45eb-9819-56e79f0510c0"

    # Informações da API do OneDrive
    scope = ["https://graph.microsoft.com/.default"]
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    def __init__(self,file_path):
        self.file_path = file_path

    # Função para gerar QR code
    def generate_qr_code(self,link, output_file):
        img = qrcode.make(link)
        img.save(output_file)

    # Autenticação com Client Credentials para obter o token de acesso
    def get_access_token(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Falha ao obter token de acesso. Result: {result}")

    # Função para fazer o upload do arquivo PDF
    def upload_file_to_onedrive(self):
        access_token = self.get_access_token()
        file_name = os.path.basename(self.file_path)

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/pdf'
        }

        # URL do Microsoft Graph para upload de arquivos no OneDrive (pasta raiz)
        user_id = "gilberto@gbernardoti.com.br"

        # Endpoint correto para o fluxo de autenticação de aplicação
        upload_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{file_name}:/content"

        with open(self.file_path, 'rb') as file_data:
            response = requests.put(upload_url, headers=headers, data=file_data)

        if response.status_code in [200,201]:
            # Recuperar ID do arquivo e link de compartilhamento
            file_id = response.json()['id']
            shared_link_response = self.create_shared_link(file_id, access_token)
            
            # Retornar tanto o link de compartilhamento quanto o ID do arquivo
            file_link = shared_link_response["link"]["webUrl"]
            return {
                'file_id': file_id,
                'file_link': file_link
            }
        else:
            return f'Erro ao fazer upload: {response.status_code}'


    # Função para criar um link de compartilhamento
    def create_shared_link(self,file_id, access_token):
        url = f"https://graph.microsoft.com/v1.0/users/gilberto@gbernardoti.com.br/drive/items/{file_id}/createLink"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "type": "view",  # ou "edit" dependendo do que você deseja
            "scope": "anonymous"  # Permitir acesso anônimo ao link
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()


    # A função abaixo pode ser utilizada para modificar o PDF, adicionando o QR Code
    def modify_pdf_with_qr_code(self, qr_code_path, output_pdf_path):
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        original_pdf_path = self.file_path

        # Criação de um PDF temporário para o QR Code
        c = canvas.Canvas("qr_temp.pdf", pagesize=letter)
        c.drawImage(qr_code_path, 400, 750, 100, 100)  # Altere a posição conforme necessário
        c.save()

        # Lê o PDF original e o PDF com QR Code
        original_pdf = PdfReader(original_pdf_path)
        qr_pdf = PdfReader("qr_temp.pdf")
        writer = PdfWriter()

        # Adiciona as páginas do PDF original
        for page in original_pdf.pages:
            writer.add_page(page)

        # Adiciona a página do QR Code
        writer.add_page(qr_pdf.pages[0])

        # Salva o PDF modificado
        with open(output_pdf_path, "wb") as output_pdf_file:
            writer.write(output_pdf_file)

    # Atualizar o arquivo existente no OneDrive com o novo PDF que contém o QR Code
    def update_file_onedrive(self):
        access_token = self.get_access_token()
        file_name = os.path.basename(self.file_path)
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/pdf'
        }

        # URL para atualizar o arquivo no OneDrive
        user_id = "gilberto@gbernardoti.com.br"
        update_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{file_name}:/content"

        with open(self.file_path, 'rb') as file_data:
            response = requests.put(update_url, headers=headers, data=file_data)

        if response.status_code == 200:
            print(f'Arquivo {file_name} atualizado com sucesso no OneDrive!')
        else:
            print(f'Erro ao atualizar o arquivo: {response.status_code}')
            print(response.json())


'''
# Exemplo de utilizacao

objOneDriveUpload =  OneDriveUpload("prescricao.pdf")

# Chamada da função
file_id, file_link = objOneDriveUpload.upload_file_to_onedrive()

# Gerar QR Code com o link (após o upload e obtenção do link de compartilhamento)
# Supondo que o link de compartilhamento foi retornado na função acima
qr_code_path = "qrcode_prescricao.png"
objOneDriveUpload.generate_qr_code(file_link, qr_code_path)

# Chamada da função para modificar o PDF com o QR Code
modified_pdf_path = "prescricao_com_qr.pdf"
objOneDriveUpload.modify_pdf_with_qr_code(qr_code_path, modified_pdf_path)

# Chamada da função para atualizar o PDF no OneDrive
objOneDriveUpload.update_file_onedrive(modified_pdf_path)
'''