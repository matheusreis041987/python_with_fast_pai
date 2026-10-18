# senha precisa ter entre 8 e 16 dígitos
# senha precisa ter ao menos uma letra maíscula
# senha precisa ter ao menos um número
#senha precisa ter ao menos um caracter especial
# A senha não pode começar com número 

def verify_password(password: str):
    
    if len(password) < 8 or len(password) > 16:
        print('Senha com tamanho menor que 8 ou maior que 16')
        return False
        
    if not password:
        print('Senha não pode ser vazia')
        return False
    
    if password[0].isdigit():
        print('Senha não pode começar com número')
        return False
    
    tem_maisculo = False
    tem_minusculo = False
    tem_numero = False
    tem_especial = False
    
    for c in password:
        if c == ' ':
            print('Senha não pode ter espaço vazio')
            return False
        elif c.isupper():
            tem_maisculo = True
        elif c.islower():
            tem_minusculo = True
        elif c.isdigit():
            tem_numero = True
        elif c in '!@#$%':
            tem_especial = True
    return tem_especial and tem_numero and tem_minusculo and tem_maisculo 
    

print(verify_password('Matheus@56423'))
print(verify_password('Matheus56423'))
print(verify_password(''))
print(verify_password(' '))
#senha = 'Matheus@564321'
#print(senha[0].isdigit())
            
    