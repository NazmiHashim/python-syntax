import lexerTry

print ('This is lexical analysis phase')
while True:
    text = input('Enter the expression > ')
    result, error = lexerTry.run('<stdin>', text)

    if error: 
        print(error.as_string())
    else: 
        for token in result:
            print(token)