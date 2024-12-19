from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import StringVar, filedialog
from PIL import Image, ImageTk
import model
from control import controllerScribo
#import pywhatkit as pwk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Dados Gilberto\Projetos\MedicalEasy\Tela\build\assets\frame0")

Control = controllerScribo()

def mostrar_hint(event,frase):
    hint_label.place(x=event.x_root - window.winfo_x(), y=event.y_root - window.winfo_y() - 80)
    hint_label.config(text=frase)

# Função para ocultar o hint
def esconder_hint(event):
    hint_label.place_forget()


def formatar_data(event, widget):
    texto = widget.get()

    # Remover caracteres não numéricos para evitar duplicação de barras
    texto = texto.replace("/", "")
    
    # Adicionar as barras automaticamente
    if len(texto) > 2 and texto[2] != '/':
        texto = texto[:2] + '/' + texto[2:]
    if len(texto) > 5 and texto[5] != '/':
        texto = texto[:5] + '/' + texto[5:]
    
    # Limitar o número de caracteres ao formato DD/MM/AAAA
    widget.delete(0, tk.END)
    widget.insert(0, texto[:10])

def formatar_cpf(event, widget):
    texto = widget.get()

    # Remover caracteres não numéricos para evitar duplicações
    texto = texto.replace(".", "").replace("-", "")
    
    # Adicionar os pontos e traço automaticamente
    if len(texto) > 3 and texto[3] != '.':
        texto = texto[:3] + '.' + texto[3:]
    if len(texto) > 7 and texto[7] != '.':
        texto = texto[:7] + '.' + texto[7:]
    if len(texto) > 11 and texto[11] != '-':
        texto = texto[:11] + '-' + texto[11:]
    
    # Limitar o número de caracteres ao formato CPF XXX.XXX.XXX-XX
    widget.delete(0, tk.END)
    widget.insert(0, texto[:14])

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def gerarPdf():
    paciente = {
        "nome"       : entryPaciente.get(),
        "nascimento" : entryNascimento.get(),
        "cpf"        : entryCPF.get(),
        "endereco"   : entryEndereco.get(),
        "cidade"     : entryCidade.get(),
        "prescricao" : textPrescricao.get("1.0", "end-1c")
        }
    file_path = Control.gerar_nome_pdf(paciente)
    senha_leitura = Control.gerar_senha(paciente['cpf'])
    Control.gerar_pdf(paciente=paciente,tipo=var.get(),file_path=file_path,senha_leitura=senha_leitura)

def imprimir():
    paciente = {
        "nome"       : entryPaciente.get(),
        "nascimento" : entryNascimento.get(),
        "cpf"        : entryCPF.get(),
        "endereco"   : entryEndereco.get(),
        "cidade"     : entryCidade.get(),
        "prescricao" : textPrescricao.get("1.0", "end-1c")
        }
    
    file_path =  Control.gerar_nome_pdf(paciente)
    senha_leitura = Control.gerar_senha(paciente['cpf'])
    Control.imprimir_pdf(paciente=paciente,tipo=var.get(),file_path=file_path,senha_leitura=senha_leitura)

def opcao_selecionada(*args):
    return var.get()


def enviar_pdf_whatsapp():
    # Abre a janela para escolher o PDF
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    caminho_pdf = filedialog.askopenfilename(title="Selecione um arquivo PDF", filetypes=[("PDF files", "*.pdf")])
    
    if caminho_pdf:
        # Solicita ao usuário o número de telefone e a mensagem
        numero = input("Digite o número de telefone com código do país (ex: +5511998765432): ")
        mensagem = input("Digite a mensagem para enviar junto com o PDF: ")
        
        # Envia a mensagem via WhatsApp Web
        try:
            # Envia a mensagem com o WhatsApp Web
#            pwk.sendwhats_image(numero, caminho_pdf, mensagem)
            print("Arquivo PDF enviado com sucesso!")
        except Exception as e:
            print("Erro ao enviar o PDF:", e)
    else:
        print("Nenhum arquivo foi selecionado.")


def enviar_pdf_email():
    # Abre a janela para escolher o PDF
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    caminho_pdf = filedialog.askopenfilename(title="Selecione um arquivo PDF", filetypes=[("PDF files", "*.pdf")])
    
    if caminho_pdf:
        # Solicita as informações do e-mail
        remetente = input("Digite seu e-mail: ")
        senha = input("Digite sua senha (ou token de aplicativo): ")
        destinatario = input("Digite o e-mail do destinatário: ")
        assunto = input("Digite o assunto do e-mail: ")
        mensagem = input("Digite a mensagem: ")
        
        # Configurando o e-mail
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        # Adiciona a mensagem ao corpo do e-mail
        msg.attach(MIMEText(mensagem, 'plain'))

        # Anexando o PDF
        with open(caminho_pdf, 'rb') as anexo:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(anexo.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f'attachment; filename={caminho_pdf.split("/")[-1]}')
            msg.attach(parte)

        # Enviando o e-mail
        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)  # Para Gmail
            servidor.starttls()  # Habilita a segurança
            servidor.login(remetente, senha)
            servidor.send_message(msg)
            servidor.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print("Erro ao enviar o e-mail:", e)
    else:
        print("Nenhum arquivo foi selecionado.")



# *******************************************************************************************
#
# Sistema principal
#
# *******************************************************************************************

if __name__ == "__main__": 
    
    bg_image = Image.open("wallpaper.png")  # Substitua pelo caminho da sua imagem
    ##bg_image = bg_image.resize((1080, 700))  # Ajuste o tamanho da imagem

    window = Tk()
    window.title('Scribo')
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - 800) // 2  # Center horizontally
    y = 0  # Top of the screen vertically

    window.geometry(f"800x500+{x}+{y}")

    bg_photo = PhotoImage(file='wallpaper.png')
    window.configure(bg = "#E7E6FF")


    canvas = Canvas(
        window,
        bg = "#000000",
        height = 500,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.pack(fill="both",expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Label para o hint (inicialmente oculto)
    hint_label = tk.Label(window, text="", bg="yellow", relief="solid")

    xLeftLabel=13
    xWidthLabel=242
    xHeightLabel=20

    xCorLabel = '#FFFFFF'
    xCorButton = '#FFFFFF'

    entryPaciente = Entry(window,relief="flat",bd=0,bg=xCorLabel)
    entryPaciente.place(x=xLeftLabel,y=146,width=xWidthLabel,height=xHeightLabel)

    entryNascimento = Entry(window,relief="flat",bd=0,bg=xCorLabel)
    entryNascimento.place(x=xLeftLabel,y=205,width=xWidthLabel,height=xHeightLabel)
    entryNascimento.bind("<KeyRelease>", lambda event: formatar_data(event, entryNascimento))

    entryCPF = Entry(window,relief="flat",bd=0,bg=xCorLabel)
    entryCPF.place(x=xLeftLabel,y=266,width=xWidthLabel,height=xHeightLabel)
    entryCPF.bind("<KeyRelease>", lambda event: formatar_cpf(event, entryCPF))

    entryEndereco = Entry(window,relief="flat",bd=0,bg=xCorLabel)
    entryEndereco.place(x=xLeftLabel,y=325,width=xWidthLabel,height=xHeightLabel)

    entryCidade = Entry(window,relief="flat",bd=0,bg=xCorLabel)
    entryCidade.place(x=xLeftLabel,y=382,width=xWidthLabel,height=xHeightLabel)

    buttonPacientes = tk.Button(window,text='Pacientes', bg=xCorButton, fg='black', bd=0)
    buttonPacientes.place(x=12,y=440,width=70,height=44)

    buttonMedicamentos = tk.Button(window,text="Fármacos",bg=xCorButton, fg='black', bd=0)
    buttonMedicamentos.place(x=99,y=440,width=70,height=44)

    buttonAtestados = tk.Button(window,text="Atestados",bg=xCorButton, fg='black', bd=0)
    buttonAtestados.place(x=186,y=440,width=70,height=44)


    # botão Imprimir
    imgImprimir = PhotoImage(file='icones/imprimir.png',master=window)
    imgImprimir.subsample(2,2)
    buttonImprimir = tk.Button(window,image=imgImprimir,highlightthickness=0,bg=xCorButton, fg='black', bd=0,command=imprimir)
#    buttonImprimir.place(x=301,y=440,width=63,height=40)
    buttonImprimir.place(x=403,y=440,width=63,height=40)
    buttonImprimir.bind("<Enter>", lambda event: mostrar_hint(event,'Imprimir Documento'))
    buttonImprimir.bind("<Leave>", esconder_hint)

    # botão Gerar PDF
    imgGerarPDF = PhotoImage(file='icones/pdf.png',master=window)
    imgGerarPDF.subsample(2,2)
    buttonGerarPDF = tk.Button(window,bg=xCorButton, fg='black', bd=0,image=imgGerarPDF,command=gerarPdf)
#    buttonGerarPDF.place(x=403,y=440,width=63,height=40)
    buttonGerarPDF.place(x=504,y=440,width=63,height=40)
    buttonGerarPDF.bind("<Enter>", lambda event: mostrar_hint(event,'Gerar PDF'))
    buttonGerarPDF.bind("<Leave>", esconder_hint)

#    imgAssinarPDF = PhotoImage(file='icones/assinatura.png',master=window)
#    imgAssinarPDF.subsample(2,2)
#    buttonAssinarPDF = tk.Button(window,bg=xCorButton, fg='black', bd=0,image=imgAssinarPDF)
#    buttonAssinarPDF.place(x=504,y=440,width=63,height=40)
#    buttonAssinarPDF.bind("<Enter>", lambda event: mostrar_hint(event,'Assinar PDF'))
#    buttonAssinarPDF.bind("<Leave>", esconder_hint)

    imgEnviarWhatsapp = PhotoImage(file='icones/whatsapp.png',master=window)
    imgEnviarWhatsapp.subsample(2,2)
    buttonEnviarWhatsapp = tk.Button(window,bg=xCorButton, fg='black', bd=0,image=imgEnviarWhatsapp,command=enviar_pdf_whatsapp)
    buttonEnviarWhatsapp.place(x=606,y=440,width=63,height=40)
    buttonEnviarWhatsapp.bind("<Enter>", lambda event: mostrar_hint(event,'Abrir Whatsapp Web'))
    buttonEnviarWhatsapp.bind("<Leave>", esconder_hint)


    imgEnviarEMail = PhotoImage(file='icones/email.png',master=window)
    imgEnviarEMail.subsample(2,2)
    buttonEnviarEMail = tk.Button(window,bg=xCorButton, fg='black', bd=0,image=imgEnviarEMail)
    buttonEnviarEMail.place(x=708,y=440,width=63,height=40)
    buttonEnviarEMail.bind("<Enter>", lambda event: mostrar_hint(event,'Enviar por e-mail'))
    buttonEnviarEMail.bind("<Leave>", esconder_hint)


    frame_opcoes = tk.Frame(window, bd=0, relief="solid",bg=xCorButton)
    frame_opcoes.place(x=275, y=430,width=110,height=60)
    # Variável associada à caixa de opções
    var = StringVar(window)
    var.set("Controlada")  # Valor padrão
    
    tk.Label(frame_opcoes,text="Prescrição", bg=xCorButton, fg='black', bd=0).place(x=2,y=2)
    
    radiobuttonControlada = tk.Radiobutton(frame_opcoes,text="Controlada",variable=var,bg=xCorButton, fg='black', bd=0, value="Controlada", command=opcao_selecionada)
    radiobuttonControlada.place(x=5,y=16)
    radiobuttonComum = tk.Radiobutton(frame_opcoes,text="Comum",variable=var,bg=xCorButton, fg='black', bd=0, value="Comum", command=opcao_selecionada)
    radiobuttonComum.place(x=5,y=33)
    var.trace_add("write", opcao_selecionada)

    textPrescricao = tk.Text(window,bd=0,bg="#FFFFFF",wrap="word")
    textPrescricao.place(x=303,y=50,width=450,height=370)

    scrollPrescricao = tk.Scrollbar(window,command=textPrescricao.yview)
    scrollPrescricao.place(x=754,y=50,height=370)

    textPrescricao.config(yscrollcommand=scrollPrescricao.set)

    window.resizable(False, False)
    window.mainloop()
