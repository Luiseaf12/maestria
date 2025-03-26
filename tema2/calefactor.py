import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

# Definir variables difusas
temperatura = ctrl.Antecedent(np.arange(10, 41, 1), 'temperatura')
potencia_calefactor = ctrl.Consequent(np.arange(0, 101, 1), 'potencia_calefactor')

# Definir conjuntos difusos
temperatura['baja'] = fuzz.trimf(temperatura.universe, [10, 15, 20])
temperatura['media'] = fuzz.trimf(temperatura.universe, [18, 25, 30])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [28, 35, 40])

potencia_calefactor['baja'] = fuzz.trimf(potencia_calefactor.universe, [0, 20, 40])
potencia_calefactor['media'] = fuzz.trimf(potencia_calefactor.universe, [30, 50, 70])
potencia_calefactor['alta'] = fuzz.trimf(potencia_calefactor.universe, [60, 80, 100])

# Definir reglas difusas
regla1 = ctrl.Rule(temperatura['baja'], potencia_calefactor['alta'])
regla2 = ctrl.Rule(temperatura['media'], potencia_calefactor['media'])
regla3 = ctrl.Rule(temperatura['alta'], potencia_calefactor['baja'])

# Crear el sistema de control
controlador_calefactor = ctrl.ControlSystem([regla1, regla2, regla3])
simulador = ctrl.ControlSystemSimulation(controlador_calefactor)

# Simular con diferentes temperaturas
temperaturas_prueba = [15, 19, 25, 29, 35]  # Temperaturas que traslapan entre rangos

print("\nPruebas con diferentes temperaturas:")
print("-" * 50)
for temp in temperaturas_prueba:
    simulador.input['temperatura'] = temp
    simulador.compute()
    print(f"Temperatura: {temp}°C -> Potencia del calefactor: {simulador.output['potencia_calefactor']:.2f}%")
