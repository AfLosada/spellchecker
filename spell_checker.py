import re
from string import ascii_lowercase



## Esta función obtiene todas las palabras del archivo word.txt y del archivo BOOKS.txt y las guarda en un arreglo de strings ##
## La función retorna todas las palabras que encuentra en los dos archivos,  ##
## Utiliza el parámetro read_mode para designar la manera en que se abrirá el archivo, esto hay que agregarlo como un parámetro nuevo a la función "open" ##
## Se le agregó encoding = 'utf8', como una variable y como parámetro de la función "open" para que funcionara la lectura del archivo sin problemas (pues el archivo tiene que ser leído con utf8 para que incluya tildes y caracteres del habla hispana) ##

def fetch_words(read_mode):
    '''Función no alterada por el ataque'''
    ## Variable agregada para facilitar el cambio del encoding para la laectura de los archivos##
    encoding = "utf8"

    words_from_dictionary = [ word.strip() for word in open('words.txt', encoding = encoding).readlines() ]
    words_from_books = re.findall(r'\w+', open('BOOKS.txt', read_mode, encoding = encoding).read())
    return words_from_dictionary + words_from_books
# spanish_letters es un arreglo que tiene todas las letras en español que se deben priorizar
spanish_letters = ['ñ', 'á', 'é', 'í', 'ó', 'ú']
# spanish typo es un arreglo que tiene todas las letras que pueden ser un typo del usuario
spanish_typo = ['n','a','e','i','o','u']

# WORDS es una variable que almacena todas las palabras, aunque se repitan, de los archivos de texto
WORDS = fetch_words('r')
# LETTERS es una variable que se usa en las funciones one_length y two_length para saber qué letras son las que puede intercambiar
LETTERS = list(ascii_lowercase) + spanish_letters
# punct_type es una variable que tiene un arreglo de tipos de puntuacion para facilitar la adición o sustracción de un tipo de puntuacion
punct_type = [',', '.', '¿', '?', '!', '¡', '\'', '"']



## Es un diccionario que recibe como llave una palabra y almacena la cantidad de veces que esta se repite en los textos ##
## Se tuvo que arreglar la lógica dentro de los ifs, pues estaba al revés. Cada vez que se una palabra ya se encuentra en el WORDS_INDEX el valor que contiene aumenta en 1 ##
WORDS_INDEX = {}
for word in WORDS:
    if word in WORDS_INDEX:
        WORDS_INDEX["" + word] += 1
    else:
        WORDS_INDEX["" + word] = 1
print(WORDS_INDEX["trabajo"])

' Hubo un reordenamiento de las funciones pues habían funciones que utilizaban funciones declaradas debajo de ellas'
' El error sucede porque en tiempo de compilación se intenta acceder a una función que aún no ha sido declarada'

# Esta función se llama después de haber corregido el spelling de todas las palabras, pues hace una comparación 1:1 #
# Esta función recibe una lista de palabras y retorna aquellas que estén en el índice #
# Retorna un set de palabras, aquellas que hagan parte del índice de palabras #
def filter_real_words(words):
    return set(word for word in words if word in WORDS_INDEX)

# Esta función recibe una palabra y encuetra todas las palabras que están a 1 de distancia de la original #
# El vocabulario que se usa está guardado en la variable LETTERS #
def one_length_edit(word):
    '''Función no alterada por el ataque'''
    
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    removals_of_one_letter = []
    
    for left, right in splits:
        if right:
            removals_of_one_letter.append(left + right[1:])
            
    two_letters_transposes = []
    
    for left, right in splits:
        if len(right) > 1:
            two_letters_transposes.append(left + right[1] + right[0] + right[2:])
            
    one_letter_replaces = []
    
    for left, right in splits:
        if right:
            for c in LETTERS:
                one_letter_replaces.append(left + c + right[1:])
                
    one_letter_insertions = []
    
    for left, right in splits:
        for c in LETTERS:
            one_letter_insertions.append(left + c + right)
    
    one_length_editions = removals_of_one_letter + two_letters_transposes + one_letter_replaces + one_letter_insertions
    
    return list(set(one_length_editions))


# Esta función hace una iteración más sobre cada palabra que recibe de one_length_edit #
# Al iterar una vez más, se crean todas las combinaciones a distancia 2 de la palabra original #
def two_lenght_edit(word):
    '''Función no alterada por el ataque'''
    return [e2 for e1 in one_length_edit(word) for e2 in one_length_edit(e1)]

# Esta función recibe una palabra y le cambia las letras que puedan ser typos del español a letras hispanas
def transform_into_spanish(word):
    words = []
    for i in range(0, len(spanish_typo)):
        possible_typo = spanish_typo[i]
        for j in range(0, len(word)):
            letter = word[j]
            if letter == possible_typo:
                front = word[0: j]
                back = word[j+1: len(word)]
                temporal_word = front + spanish_letters[i] + back
                words.append(temporal_word)
    return words


def possible_corrections(word):
    # Si la palabra está correcta se retorna la misma, pero en forma de arreglo pues así la recibe la función superior #
    no_correction_at_all = [word]
    # Después de crear las palabras con caracteres hispanos se filtran con el diccionario #
    spanish_word = filter_real_words(transform_into_spanish(word))
    
    # En este if se empieza por lo más macro: ¿La palabra es una palabra real? #
    # Se usa len para verificar que el set tenga contenido, si no lo tiene se avanza al siguiente if #
    # Este if se agrega para evitar los siguientes pasos en el caso de que la palabra sea la misma #
    if len(filter_real_words([word])):
        return no_correction_at_all
    # En este segmento se revisa si la palabra puede ser un typo del español #
    elif len(spanish_word):
        return spanish_word
    else:
        # Se crean estas dos variables para facilitar la legibilidad del código #
        # Es importante que estén dentro de el else para que el if que lo precede optimice el código #
        one_length_edit_possible_corrections = filter_real_words(one_length_edit(word))
        two_lenght_edit_possible_corrections = filter_real_words(two_lenght_edit(word))
        # Ahora nos preguntamos ¿Hay una palabra a uno de distancia que sea real? #
        if len(one_length_edit_possible_corrections):
            return one_length_edit_possible_corrections
    # Lo mismo que el anterior pero a dos de distancia #
        elif len(two_lenght_edit_possible_corrections):
            return two_lenght_edit_possible_corrections
        # En cualquier caso, si no hay correcciones a esta distancia se retorna lo mismo que se ingresó #
        else:
            return no_correction_at_all


# Es lo que permite determinar cual de las opciones es la más utilizada, pues se usa para comparar qué opción tiene un promedio de uso mayor (cual es más popular) #
def language_model(word):
    # El language model retorna un número que se usa para compara qué palabra es usada más frecuentemente #
    # Eliminé el random y la sumatoria pues no cumplen ninguna funciona además de aleatorizar la elección de la palabra #
    N = sum(WORDS_INDEX.values())
    
    # Esta división sobre N me permite determinar que el modelador de lenguaje da el promedio de uso de la palabra #
    return WORDS_INDEX.get(word, 0)/N



def spell_check_word(word):
    # Esta función retorna la palabra que más veces se usa al aplicarle language model #
    # Se cambió de min a max por lo que el interés es saber cual palabra se acerca más al modelo, además, el modelo usa la misma función y al hacer la prueba se acerca más a la realidad #
    
    return max(possible_corrections(word), key=language_model)


# Esta es la función mas macro, la que hace el return a los tests #
def spell_check_sentence(sentence):
    # Se cambió sentence.upper() a sentence.lower()
    lower_cased_sentence = sentence.lower()
    # Creo un diccionario con los tipos de puntuación como llave y las ubicaciones de estos como valor #
    punctuactions = {}
    for i in range(0, len(sentence)):
        letter_of_sentence = sentence[i]
        if letter_of_sentence in punct_type:
            punctuactions[i] = letter_of_sentence
    # Creo un arreglo/lista que almacena las posiciones de las letras que hay que poner en mayúscula #
    upperCase = []
    for i in range(0,len(sentence)):
        if ("" + sentence[i]).isupper():
            upperCase.append(i)

    # Esta linea le quita la puntuación a la frase para hacer el análisis por palabras #
    stripped_sentence = list(map(lambda x : x.strip(''.join(punct_type)), lower_cased_sentence.split()))
    # Se cambió de filter a map, puesto que filter no aplica la función a la lista #
    checked = map(spell_check_word, stripped_sentence)
    checked = " ".join(checked)

    # Agregar la puntuación
    for position_of_punctuation in punctuactions.keys():
        front = checked[0: position_of_punctuation]
        back = checked[position_of_punctuation: len(checked)]
        checked = front + punctuactions[position_of_punctuation] + back

    # Agregar las mayuculas
    for i in range(0,len(upperCase)):
        front = checked[0: upperCase[i]]
        back = checked[upperCase[i]+1: len(checked)]
        checked = front + (""+checked[upperCase[i]]).upper() + back
    return checked



def test_spell_check_sentence():

    sentence = 'fabor guardar cilencio para no molestar'
    assert 'favor guardar silencio para no molestar' == spell_check_sentence(sentence) 

    sentence = 'un lgar para la hopinion'
    assert 'un lugar para la opinión' == spell_check_sentence(sentence)

    sentence = 'el Arebol del día'
    print(spell_check_sentence(sentence))
    assert 'el arrebol del día' == spell_check_sentence(sentence)

    sentence = 'Rezpeto por la educasión'
    print(spell_check_sentence(sentence))
    assert 'respeto por la educación' == spell_check_sentence(sentence)

    sentence = 'RTe encanta conduzir'
    print(spell_check_sentence(sentence))
    assert 'te encanta conducir' == spell_check_sentence(sentence)

    sentence = 'HOy ay karne azada frezca siga pa dentro'
    print(spell_check_sentence(sentence))
    assert 'hoy ay carne azada fresca siga la dentro' == spell_check_sentence(sentence)

    sentence = 'En mi ezcuela no enseñan a escrivir ni a ler'
    print(spell_check_sentence(sentence))
    assert 'en mi escuela no enseñan a escribir ni a le' == spell_check_sentence(sentence)

    sentence = 'él no era una persona de fiar pues era un mentirozo'
    print(spell_check_sentence(sentence))
    assert 'él no era una persona de fiar pues era un mentiroso' == spell_check_sentence(sentence) 

def test_spell_check_sentence_2():
    
    sentence = 'él, no era una persona de fiar pues era un mentirozo'
    print(spell_check_sentence(sentence))
    assert 'él, no era una persona de fiar pues era un mentiroso' == spell_check_sentence(sentence)

    # Nuevo test para verificar la puntuación al principio de la frase y multiples tipos de puntuación#

    sentence = '¿él, no era una persona de fiar pues era un mentirozo?'
    print(spell_check_sentence(sentence))
    assert '¿él, no era una persona de fiar pues era un mentiroso?' == spell_check_sentence(sentence)

    sentence = 'No era una persona de fiar pues era un mentirozo'
    print(spell_check_sentence(sentence))
    assert 'No era una persona de fiar pues era un mentiroso' == spell_check_sentence(sentence) 

    ''' 
    Este caso de uso "fallaba" hasta que se incluyó "trabaja" en el 
    diccionario al ponerlo en el archivo words.txt, 
    pues en ninguno de los dos archivos estaba incluido
    '''
    sentence = 'trabaja de dia'
    print(spell_check_sentence(sentence))
    assert 'trabaja de día' == spell_check_sentence(sentence)

    # Caso de prueba con dos palabras que tienen mayuscula
    sentence = 'Mayusculas y Minusculas compartidas'
    print(spell_check_sentence(sentence))
    assert 'Mayúsculas y Minúsculas compartidas'

#test_spell_check_sentence()
test_spell_check_sentence_2()
