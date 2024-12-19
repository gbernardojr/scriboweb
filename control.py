from model import pdfScribo, dbScribo
from onedrive import OneDriveUpload
from datetime import datetime
import os
import win32
from win32 import win32print, win32api
from tkinter import messagebox
from assinarA3 import sign_protected_pdf
from assinarPDF import unlock_and_sign_pdf

class controllerScribo:

    def gerar_senha(self,cpf):
        cpf_numerico = ''.join(filter(str.isdigit, cpf))
        return cpf_numerico[0:3]


    def gerar_nome_pdf(self,paciente):
        nome = paciente['nome']
        
        data_atual = datetime.now()
        
        dia = data_atual.day
        mes = data_atual.month
        ano = data_atual.year
        hora = data_atual.hour
        minuto = data_atual.minute
        return f'./docs/{nome}_{dia}_{mes}_{ano}_{hora}_{minuto}.pdf'


    def gerar_pdf(self,paciente,tipo,file_path,senha_leitura):   
        PDF =  pdfScribo()
        objOneDriveUpload = OneDriveUpload(file_path)
        
        PDF.generate_initial_pdf(file_path)
        dadosCompartilhamento = objOneDriveUpload.upload_file_to_onedrive()
        if tipo == 'Controlada':
            PDF.gerar_pdf_controle_especial(paciente,dadosCompartilhamento["file_id"], dadosCompartilhamento["file_link"],file_path,senha_leitura)     
        else:
            PDF.gerar_pdf(paciente,dadosCompartilhamento["file_id"], dadosCompartilhamento["file_link"],file_path,senha_leitura)
        
        input_pdf = file_path
        output_pdf = file_path
        # sign_protected_pdf(input_pdf, senha_leitura, output_pdf)
        unlock_and_sign_pdf(input_pdf, senha_leitura, output_pdf)         
        objOneDriveUpload.update_file_onedrive()
        
    def assinar_pdf(self):
        
        ...
        
    def imprimir_pdf(self,paciente,tipo,file_path,senha_leitura):
        self.gerar_pdf(paciente=paciente,tipo=tipo,file_path=file_path,senha_leitura=senha_leitura)
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Arquivo {file_path} não encontrado!")
            return
        
        # Obtém o nome da impressora padrão, se não for especificada
        printer_name = win32print.GetDefaultPrinter()

        try:
            file_path2 =  file_path.replace('.','C:/Dados Gilberto/Projetos/Scribo')
            file_path2 =  file_path.replace('/','\\')
            
            # Envia o comando de impressão para a impressora
            win32api.ShellExecute(
                0,
                "print",
                file_path2,
                f'/d:"{printer_name}"',
                ".",
                0
            )
            print(f"Arquivo {file_path} enviado para {printer_name} com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar o arquivo ({file_path2}) para a impressora ({printer_name}): {e}")
            
    '''
    def busca_paciente():
        DBScribo = dbScribo()
        nome = m
        DBScribo.buscar_dados_paciente
    '''