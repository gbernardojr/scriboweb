import subprocess
import pikepdf

def sign_pdf(input_pdf, output_pdf, cert_file, key_file):
    # Assina o PDF utilizando OpenSSL
    signed_pdf_path = 'temp_signed.pdf'  # Caminho temporário para o PDF assinado
    command = [
        'openssl', 'smime', '-sign',
        '-in', input_pdf,
        '-signer', cert_file,
        '-inkey', key_file,
        '-outform', 'P12',  # Usar P12 em vez de DER para compatibilidade
        '-out', signed_pdf_path,
        '-nodetach'
    ]

    try:
        # Executa o comando
        subprocess.run(command, check=True)
        print(f"PDF assinado com sucesso: {signed_pdf_path}")

        # Usando pikepdf para adicionar a assinatura ao campo "Assinatura"
        with pikepdf.open(signed_pdf_path) as pdf:
            # Aqui, você pode adicionar a assinatura ao campo "Assinatura"
            # A posição e o nome do campo devem corresponder ao que você definiu no PDF original

            # Adicionar um campo de assinatura
            pdf.pages[0].add_field({
                "/T": "(Assinatura)",
                "/FT": "/Sig",
                "/Rect": [100, 700, 300, 750],  # Posição do campo de assinatura
            })

            # Salvar o PDF final
            pdf.save(output_pdf)
            print(f"PDF assinado e salvo como: {output_pdf}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao assinar PDF: {e.stderr.decode()}")

if __name__ == '__main__':
    # Defina os caminhos dos arquivos
    input_pdf = 'prescricao.pdf'  # PDF a ser assinado
    output_pdf = 'prescricao_assinado.pdf'  # PDF assinado
    cert_file = 'C:/Dados Gilberto/CertificadoDigital/certificate.pem'  # Certificado digital
    key_file = 'C:/Dados Gilberto/CertificadoDigital/privateKey.pem'  # Chave privada

    # Chama a função para assinar o PDF
    sign_pdf(input_pdf, output_pdf, cert_file, key_file)
