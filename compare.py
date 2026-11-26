import matplotlib.pyplot as plt
import numpy as np

# Professional style
plt.style.use('seaborn-v0_8')

# Metrics
metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']

# Base paper results
base_paper = [92, 91, 90, 91]

# Your project results
vertexguard = [98, 97, 96, 97]

x = np.arange(len(metrics))

plt.figure(figsize=(10,6))

# Base paper line
plt.plot(x, base_paper,
         marker='o',
         linewidth=3,
         markersize=8,
         label='Base Paper IDS',
         color='#00CED1')

# Your project line
plt.plot(x, vertexguard,
         marker='o',
         linewidth=3,
         markersize=8,
         label='VertexGuard IDS',
         color='#4B3F99')

plt.title("Performance Comparison", fontsize=16, fontweight='bold')
plt.xlabel("Evaluation Metrics", fontsize=12)
plt.ylabel("Percentage (%)", fontsize=12)

plt.xticks(x, metrics, fontsize=11)
plt.yticks(fontsize=11)

plt.ylim(80,100)

plt.grid(True, linestyle='--', alpha=0.6)

plt.legend(loc='lower left')

# Percentage labels
for i, value in enumerate(base_paper):
    plt.text(i, value + 0.5, f'{value}%', ha='center', fontsize=10)

for i, value in enumerate(vertexguard):
    plt.text(i, value + 0.5, f'{value}%', ha='center', fontsize=10)

plt.tight_layout()

# Save graph
plt.savefig("performance_comparison_line.png", dpi=300)

plt.show()