
# coding: utf-8

# # Modelo de la alarma

# El paquete de _Python_ [pgmpy](http://pgmpy.org) proporciona un marco de trabajo para las redes bayesianas.

# En primer lugar, importamos los módulos necesarios:

# In[1]:


import networkx  # Permite trabajar con grafos
import pgmpy.models as pgmm  # Modelos gráficos de probabilidad
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y factores de probabilidad
import pgmpy.inference as pgmi  # Inferencia probabilística exacta


# Para definir la red bayesiana del modelo de la alarma visto en clase construimos primero el DAG asociado.

# In[ ]:


Modelo_alarma = pgmm.BayesianModel()
Modelo_alarma.add_nodes_from(['Robo', 'Terremoto', 'Alarma', 'Llamada', 'Noticia'])
Modelo_alarma.add_edges_from([('Robo', 'Alarma'),
                              ('Terremoto', 'Alarma'),
                              ('Alarma', 'Llamada'),
                              ('Terremoto', 'Noticia')])


# También se podrían haber proporcionado las aristas directamente al crear la instancia de la clase `BayesianModel`, 
#       en cuyo caso los vértices se crean automáticamente a partir de ellas.

# In[ ]:


Modelo_alarma = pgmm.BayesianModel([('Robo', 'Alarma'),
                                    ('Terremoto', 'Alarma'),
                                    ('Alarma', 'Llamada'),
                                    ('Terremoto', 'Noticia')])


# Podemos comprobar cuáles son los vértices y las aristas de la componente cualitativa de la red bayesiana.

# In[ ]:


Modelo_alarma.nodes


# In[ ]:


Modelo_alarma.edges


# A continuación, asociamos a cada variable de la red una distribución de probabilidad condicional.
# Hay que tener en cuenta que el paquete _pgmpy_ asume que los valores de una variable que puede tomar $n$ valores son los números de 0 a $n - 1$.

# Para cada variable creamos una instancia de la clase `TabularCPD`, proporcionando:
# * el nombre de la variable (atributo `variable`),
# * la cantidad de valores (cardinalidad) que puede tomar (atributo `variable_card`),
# * una lista de listas, conteniendo cada una de estas las probabilidades para un valor concreto, 
#           según los valores de los padres (atributo `values`, el valor se transforma a un array),
# * una lista con los nombres de los padres (atributo `evidence`, valor `None` si no se proporciona),
# * una lista con la cantidad de valores (cardinalidad) que puede tomar cada uno de los padres (atributo `evidence_card`, valor `None` si no se proporciona).

# In[ ]:


Alarma_CPD = pgmf.TabularCPD('Alarma', 2, [[.99, .1, .1, .01], [.01, .9, .9, .99]],
                             ['Robo', 'Terremoto'], [2, 2])
print(Alarma_CPD)


# In[ ]:


Robo_CPD = pgmf.TabularCPD('Robo', 2, [[.9, .1]])
print(Robo_CPD)


# In[ ]:


Terremoto_CPD = pgmf.TabularCPD('Terremoto', 2, [[.99, .01]])
print(Terremoto_CPD)


# In[ ]:


Noticia_CPD = pgmf.TabularCPD('Noticia', 2, [[.999, .01], [.001, .99]], ['Terremoto'], [2])
print(Noticia_CPD)


# In[ ]:


Llamada_CPD = pgmf.TabularCPD('Llamada', 2, [[.99, .05], [.01, .95]], ['Alarma'], [2])
print(Llamada_CPD)


# In[ ]:


Modelo_alarma.add_cpds(Alarma_CPD, Robo_CPD, Terremoto_CPD, Noticia_CPD, Llamada_CPD)
Modelo_alarma.cpds


# ### d-separación

# Con el método `is_active_trail` podemos comprobar si una variable es __condicionalmente dependiente__ de otra, dada una evidencia.

# In[ ]:


print(Modelo_alarma.is_active_trail('Robo', 'Llamada'))
print(Modelo_alarma.is_active_trail('Robo', 'Llamada', 'Alarma'))
print(Modelo_alarma.is_active_trail('Alarma', 'Noticia'))
print(Modelo_alarma.is_active_trail('Alarma', 'Noticia', 'Terremoto'))
print(Modelo_alarma.is_active_trail('Robo', 'Terremoto'))
print(Modelo_alarma.is_active_trail('Robo', 'Terremoto', 'Alarma'))
print(Modelo_alarma.is_active_trail('Robo', 'Terremoto', ['Llamada', 'Noticia']))


# Podemos consultar cuáles son las variables __condicionalmente dependientes__ de una determinada variable, dada una evidencia.

# In[ ]:


print(Modelo_alarma.active_trail_nodes('Robo'))
print(Modelo_alarma.active_trail_nodes('Robo', 'Alarma'))
print(Modelo_alarma.active_trail_nodes('Robo', 'Terremoto'))
print(Modelo_alarma.active_trail_nodes('Robo', ['Alarma', 'Terremoto']))


# ### Inferencia probabilística exacta mediante eliminación de variables

# A continuación vamos a calcular, usando el algoritmo de eliminación de variables, la distribución de probabilidad de la variable Robo, 
#           dado que sabemos que Watson ha llamado a Holmes y que en la radio no han dado ninguna noticia de que se haya producido un terremoto.

# Los factores iniciales serán las tablas de probabilidad condicionales de la red bayesiana, reducidas según la evidencia. 
#  Eliminaremos primero la variable Terremoto y después la variable Alarma. Finalmente, multiplicaremos los factores restantes y normalizaremos.

# Los factores se implementan como instancias de la clase `DiscreteFactor`. Para crear una instancia de un factor hay que proporcionar:
# 1. El ámbito del factor como una lista de variables (atributo `variables`).
# 2. Las cardinalidades de las variables del ámbito, como una lista (atributo `cardinality`).
# 3. Los valores asociados a cada combinación de valores de las variables del ámbito, como una lista (atributo `values`). 
#           Para establecer la asociación debe tenerse en cuenta que los valores de las variables varían más rápido desde la última variable del ámbito hasta la primera.
# 
# También se puede obtener un factor a partir de una instancia de la clase `TabularCPD` mediante el método `to_factor` de esta última.

# In[ ]:


# Factores iniciales

phi_R = Robo_CPD.to_factor()
print(phi_R.scope())
print(phi_R)

phi_T = Terremoto_CPD.to_factor()
print(phi_T.scope())
print(phi_T)

phi_A = Alarma_CPD.to_factor()
print(phi_A.scope())
print(phi_A)

phi_N = Noticia_CPD.to_factor()
phi_N.reduce([('Noticia', 0)])
print(phi_N.scope())
print(phi_N)

phi_Ll = Llamada_CPD.to_factor()
phi_Ll.reduce([('Llamada', 1)])
print(phi_Ll.scope())
print(phi_Ll)


# In[ ]:


# Eliminamos la variable Terremoto

phi_noT = phi_T * phi_A * phi_N
phi_noT.marginalize(['Terremoto'])
print(phi_noT.scope())
print(phi_noT)


# In[ ]:


# Eliminamos la variable Alarma

phi_noA = phi_Ll * phi_noT
phi_noA.marginalize(['Alarma'])
print(phi_noA.scope())
print(phi_noA)


# In[ ]:


# Multiplicamos los factores restantes y normalizamos

phi = phi_R * phi_noA
phi.normalize()
print(phi)


# Todos los pasos anteriores constituyen el algoritmo de eliminación de variables, que, creando instancias de la clase `VariableElimination`, 
# se puede aplicar de manera automática para realizar consultas en una red bayesiana.
# 
# Una vez creada la instancia del algoritmo para una red bayesiana concreta, para realizar una consulta probabilística hay que proporcionar los siguientes argumentos:
# * Una lista de las variables de consulta.
# * Un diccionario en el que se indique el valor conocido de cada variable de evidencia.
# * Opcionalmente, una lista del resto de variables indicando el orden de eliminación. Si no se proporciona, este último se determina automáticamente.

# In[ ]:


Modelo_alarma_ev = pgmi.VariableElimination(Modelo_alarma)
consulta = Modelo_alarma_ev.query(['Robo'], {'Llamada': 1, 'Noticia': 0},
                                  ['Terremoto', 'Alarma'])
print(consulta['Robo'])


# # Inferencia probabilística aproximada

# Una _muestra aleatoria_ de una red bayesiana es una asignación de valores a las variables de la red, con probabilidad de generación igual a la probabilidad conjunta de que las variables tomen esos valores.

# __Ejercicio 1__: definir una función `muestra_aleatoria` que, dada una red bayesiana, devuelva una muestra aleatoria de la misma (como un diccionario).
# 
# __Notas__:
# 1. La función `topological_sort` del paquete `networkx` devuelve un orden topológico de los vértices de un DAG.
# 2. El método `get_cpds` de la clase `BayesianModel` devuelve la instancia de la clase `TabularCPD` asociada a la variable proporcionada como argumento.
# 3. Dados una instancia de la clase `TabularCPD`, un entero representando un valor _Val_ de la variable _Var_ asociada a ella y un diccionario representando una asignación de valores a variables, incluidos los padres de _Var_, la función `seleccionar_probabilidad` definida a continuación devuelve la probabilidad de que _Var_ tome el valor _Val_, condicionada a los valores de los padres de _Var_.
# 4. Dados la cardinalidad _Card_ de una variable y una lista de probabilidades para cada entero entre $0$ y _Card_$ - 1$, la función `generar_valor_aleatorio` definida a continuación devuelve un entero aleatorio en ese rango generado según la probabilidad proporcionada.

# In[ ]:


import random

def seleccionar_probabilidad(cpd, valor, evidencia):
    padres = [v for v in cpd.variables if v != cpd.variable]
    valores_evidencia = tuple(evidencia[var] for var in padres)
    return cpd.values[valor][valores_evidencia]

def generar_valor_aleatorio(cardinalidad, probabilidades):
    p = random.random()
    acumuladas = 0
    for valor in range(cardinalidad):
        acumuladas += probabilidades[valor]
        if p <= acumuladas:
            return valor


# In[ ]:


def muestra_aleatoria(red):
    pass


# Dada una evidencia, una _muestra ponderada_ de una red bayesiana es una muestra aleatoria en la que los valores asignados a las variables son compatibles con la evidencia, junto con el peso asociado a esa muestra, es decir, la probabilidad de que se tenga la evidencia dados los valores generados del resto de variables.

# __Ejercicio 2__: definir una función `muestra_ponderada` que, dados una red bayesiana y una evidencia (como un diccionario que asigna valores a variables), devuelva una tupla cuyo primer elemento sea una muestra aleatoria de la red (como un diccionario) y cuyo segundo elemento sea el peso de la misma (como un número real).

# In[ ]:


def muestra_ponderada(red,evidencia):
    pass


# __Ejercicio 3__: definir una función `muestreo_con_rechazo` que, dados una red bayesiana, unas variables de consulta (como una lista), una evidencia (como un diccionario) y un entero positivo $N$, devuelva la distribución de probabilidad conjunta (como una instancia de la clase `DiscreteFactor`) de las variables de consulta dada la evidencia, calculada mediante el algoritmo de muestreo con rechazo generando $N$ muestras aleatorias.
# 
# __Notas__:
# 1. Considérese el uso de la función `product` de la biblioteca estándar `itertools` para generar todas las combinaciones de valores de las variables de consulta.
# 2. Considérese el uso del tipo de dato `Counter` de la biblioteca estándar `collections` para llevar el conteo de las frecuencias con las que han aparecido cada una de esas combinaciones en las muestras no rechazadas.

# In[ ]:


import itertools
import collections

def muestreo_con_rechazo(red,consulta,evidencia,n):
    pass


# __Ejercicio 4__: definir una función `ponderación_por_verosimilitud` que, dados una red bayesiana, unas variables de consulta (como una lista), una evidencia (como un diccionario) y un entero positivo $N$, devuelva la distribución de probabilidad conjunta (como una instancia de la clase `DiscreteFactor`) de las variables de consulta dada la evidencia, calculada mediante el algoritmo de ponderación por verosimilitud generando $N$ muestras aleatorias.

# In[ ]:


def ponderacion_por_verosimilitud(red,consulta,evidencia,n):
    pass


# # Estimación del riesgo de una aseguradora de coches

# La siguiente red bayesiana modeliza un sistema experto para la estimación del riesgo de una asguradora de coches.

# <img src='insurance.png' width=700 height=463>

# La red bayesiana se puede leer desde un fichero en formato BIF evaluando las siguientes expresiones:

# In[ ]:


import pgmpy.readwrite.BIF as rwBIF

reader = rwBIF.BIFReader('insurance.bif')
Modelo_aseguradora = reader.get_model()


# Las variables se clasifican en tres tipos: variables de interés, variables observables y variables mediadoras.
# 
# __Nota__: en lo que sigue se indica entre paréntesis el nombre de la variable tal y como aparece en el fichero, en aquellos casos en los que difiere del nombre que aparece en el gráfico.
# 
# Las variables de interés son: MedicalCost (`MedCost`, coste médico), LiabilityCost (`ILiCost`, coste de responsabilidad), PropertyCost (`PropCost`, coste de propiedad). Las tres variables pueden tomar como valores: miles (`Thousand`), diez miles (`TenThou`), cientos de miles (`HundredThou`) y millones (`Million`).
# 
# Las variables observables son:
# * Age, con valores: `Adolescent`, `Adult`, `Senior`.
# * Mileage, con valores: `FiveThou`, `TwentyThou`, `FiftyThou`, `Domino`.
# * VehicleYear, con valores: `Current`, `Older`.
# * DrivingHist (`DrivHist`), con valores: `Zero`, `One`, `Many`.
# * DrivQuality, con valores: `Poor`, `Normal`, `Excellent`.
# * MakeModel, con valores: `SportsCar`, `Economy`, `FamilySedan`, `Luxury`, `SuperLuxury`.
# * HomeBase, con valores: `Secure`, `City`, `Suburb`, `Rural`.
# * GoodStudent, ExtraCar (`OtherCar`), SeniorTrain, Antilock y Airbag con valores: `True`, `False`.
# 
# El resto de variables son variables mediadoras.

# __Ejercicio 5__: definir una función `estimación_de_costes` que, dada una evidencia de una o más variables observables (como un diccionario), devuelva el valor más probable de cada variable de interés (como un diccionario).

# In[ ]:


def estimacion_de_costes(evidencia):
    pass


# In[ ]:


estimacion_de_costes({'Age': 0,
                      'Mileage': 3,
                      'VehicleYear': 1,
                      'DrivHist': 0,
                      'DrivQuality': 0,
                      'MakeModel': 0,
                      'HomeBase': 0,
                      'GoodStudent': 0})

