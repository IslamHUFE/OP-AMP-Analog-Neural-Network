"""
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# تحميل البيانات من ملف Excel
df = pd.read_excel('C:/Users/tarek m eid/Desktop/freelancer/AANN/Training DATA.xlsx')

# فصل المدخلات والمخرجات
X = df.iloc[:, :5].values
y = df.iloc[:, 5:9].values

print("شكل بيانات المدخلات:", X.shape)
print("شكل بيانات المخرجات:", y.shape)

# بناء نموذج الشبكة العصبية (إجمالي 40 خلية عصبية)
model = keras.Sequential([
    layers.Dense(2, activation='relu', input_shape=(5,)),  # طبقة مخفية أولى: 20 خلية
    #layers.Dense(16, activation='relu'),  # طبقة مخفية ثانية: 16 خلية
    layers.Dense(4, activation='sigmoid')  # طبقة إخراج: 4 خلايا
])

# تجميع النموذج
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# عرض هيكل النموذج
model.summary()

# تدريب النموذج على جميع البيانات
history = model.fit(
    X, y,
    epochs=100,
    batch_size=8,
    verbose=1
)

# تقييم النموذج
train_loss, train_accuracy = model.evaluate(X, y, verbose=0)
print(f"\nدقة التدريب النهائية: {train_accuracy:.4f}")
print(f"خسارة التدريب النهائية: {train_loss:.4f}")

# توقع على البيانات
predictions = model.predict(X)
print("\nالتوقعات على بيانات التدريب:")
print(predictions.round(3))

# مقارنة التوقعات مع القيم الحقيقية
print("\nمقارنة مع القيم الحقيقية (أول 5 عينات):")
for i in range(min(5, len(X))):
    print(f"العينة {i+1}: توقع = {predictions[i].round(2)}, حقيقة = {y[i]}")

model.save('mymodel.keras')
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from tensorflow.keras.models import load_model

# تحميل النموذج
model = load_model("C:/Users/tarek m eid/Desktop/freelancer/AANN/ANN/ANN/mymodel.keras")

# إنشاء الرسم البياني
G = nx.DiGraph()

# عدد مدخلات النموذج
num_inputs = model.input_shape[-1]
prev_nodes = [f"I{i+1}" for i in range(num_inputs)]

# إضافة عقد الإدخال مع subset = 0
for node in prev_nodes:
    G.add_node(node, subset=0)

# المرور على الطبقات
for layer_idx, layer in enumerate(model.layers):
    try:
        weights, biases = layer.get_weights()
    except Exception:
        continue  # بعض الطبقات لا تحتوي على أوزان

    num_inputs, num_outputs = weights.shape
    curr_nodes = [f"L{layer_idx+1}_N{j+1}" for j in range(num_outputs)]

    # إضافة عقد الطبقة الحالية مع subset = layer_idx + 1
    for node in curr_nodes:
        G.add_node(node, subset=layer_idx + 1)

    # رسم الحواف مع الأوزان
    for i in range(num_inputs):
        for j in range(num_outputs):
            w = weights[i, j]
            G.add_edge(prev_nodes[i], curr_nodes[j], weight=w)

    prev_nodes = curr_nodes

# تحديد المواضع (layout) باستخدام subset لكل طبقة
pos = nx.multipartite_layout(G, subset_key="subset")

# رسم العقد
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)
nx.draw_networkx_labels(G, pos, font_size=8)

# رسم الحواف
edges = G.edges(data=True)
weights = [abs(d['weight']) for (u, v, d) in edges]
nx.draw_networkx_edges(G, pos, width=[w * 2 for w in weights], alpha=0.5)

# كتابة الأوزان على الحواف - وضعها بالقرب من العقدة المصدر
edge_labels = {(u, v): f"{d['weight']:.2f}" for (u, v, d) in edges}

# رسم الأوزان بالقرب من العقدة المصدر (إلى اليسار)
nx.draw_networkx_edge_labels(
    G, pos, 
    edge_labels=edge_labels, 
    font_size=6,
    bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8, edgecolor='none'),
    label_pos=0.15,  # قريب جداً من العقدة المصدر (15% من بداية الحافة)
    rotate=False,
    font_color='red'  # لجعلها أكثر وضوحاً
)

plt.title("Neural Network Structure with Weights (Near Source Nodes)")
plt.axis('off')
plt.tight_layout()
plt.show()
"""
"""
from tensorflow import keras

# Load your .keras model
model = keras.models.load_model('my_trained_model.keras')

# Save as .h5 format for MATLAB compatibility
model.save('converted_model.h5', save_format='h5')
"""


from keras.models import load_model
import numpy as np  # للتنسيق إذا لزم

# استبدل 'your_model.keras' باسم ملفك الفعلي
model = load_model('C:/Users/tarek m eid/Desktop/freelancer/AANN/ANN/ANN/mymodel1.keras')

# عرض ملخص الشبكة (للتأكيد على الهيكل)
print("Model Summary:")
model.summary()

# استخراج جميع الأوزان والإنحيازات (تعيد list من arrays)
weights = model.get_weights()

# الطبقة المخفية (عادةً الأولى: أوزان ثم إنحيازات)
hidden_weights = weights[0]  # مصفوفة أوزان (5x2)
hidden_biases = weights[1]   # مصفوفة إنحيازات (2)

# طبقة الإخراج (الثانية: أوزان ثم إنحيازات)
output_weights = weights[2]  # مصفوفة أوزان (2x4)
output_biases = weights[3]   # مصفوفة إنحيازات (4)

# عرض الأوزان والإنحيازات بوضوح
print("\nHidden Layer Weights (from inputs to hidden neurons):")
for i in range(hidden_weights.shape[1]):  # لكل نيورون مخفي
    print(f"Hidden Neuron {i+1}: {hidden_weights[:, i]}")

print("\nHidden Layer Biases:")
print(hidden_biases)

print("\nOutput Layer Weights (from hidden to output neurons):")
for i in range(output_weights.shape[1]):  # لكل نيورون إخراج
    print(f"Output Neuron {i+1}: {output_weights[:, i]}")

print("\nOutput Layer Biases:")
print(output_biases)